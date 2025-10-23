
import io
import re
from typing import Dict, Any, List

try:
    import mammoth   # .docx -> html
except Exception:
    mammoth = None

try:
    from bs4 import BeautifulSoup
except Exception:
    BeautifulSoup = None

try:
    import docx  # python-docx as fallback
except Exception:
    docx = None

try:
    import pdfplumber
except Exception:
    pdfplumber = None

MONTHS = "(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"

def _bytes_to_text(name: str, data: bytes) -> str:
    suf = name.lower().split(".")[-1]
    if suf in ("html","htm"):
        return data.decode("utf-8", errors="ignore")
    if suf == "docx" and mammoth is not None:
        with io.BytesIO(data) as f:
            res = mammoth.convert_to_html(f)
            return res.value
    if suf == "docx" and docx is not None:
        from docx import Document
        with io.BytesIO(data) as f:
            d = Document(f)
            return "<br/>".join(p.text for p in d.paragraphs)
    if suf == "pdf" and pdfplumber is not None:
        out = []
        with io.BytesIO(data) as f:
            with pdfplumber.open(f) as pdf:
                for p in pdf.pages:
                    out.append(p.extract_text() or "")
        return "<br/>".join(out)
    if suf in ("doc",):
        try: return data.decode("utf-8", errors="ignore")
        except Exception: return data.decode("latin-1", errors="ignore")
    try: return data.decode("utf-8", errors="ignore")
    except Exception: return data.decode("latin-1", errors="ignore")

def _html_to_text(html: str) -> str:
    if BeautifulSoup is None:
        return html
    soup = BeautifulSoup(html, "html.parser")
    for br in soup.find_all("br"):
        br.replace_with("\n")
    txt = soup.get_text("\n")
    import re
    txt = re.sub(r"\n{3,}", "\n\n", txt).strip()
    return txt

def _grab(pattern: str, text: str, flags=re.I):
    import re
    m = re.search(pattern, text, flags)
    return m.group(1).strip() if m else ""

def _graball(pattern: str, text: str, flags=re.I|re.S) -> List[str]:
    import re
    return [m.group(1).strip() if m.lastindex else m.group(0).strip() for m in re.finditer(pattern, text, flags)]

def parse_brief(data: bytes, filename: str) -> Dict[str, Any]:
    html_or_text = _bytes_to_text(filename, data)
    text = _html_to_text(html_or_text)

    title = _grab(r"(?:Subject|Headline|Title)\s*[:\-]\s*(.+)", text) or _grab(r"Promotion\s*Name\s*[:\-]\s*(.+)", text)
    if not title:
        import re
        m = re.search(r"\b(Pragmatic .*?Prize Draw|Evolution .*?Prize Draw|Games Global .*?Prize Draw|[\$€£]?\d+\s?K .*?Prize Draw)\b", text, re.I)
        title = m.group(1) if m else "Prize Draw"

    import re
    markets = sorted({m.upper() for m in re.findall(r"\.(COM|EU|UK|ES|PT)\b", text, re.I)}) or ["COM","EU","UK"]

    mechanic = ""
    m = re.search(r"(Stake|Wager|Bet)\s+([€$£]?\d+)\s+.*?(?:on|in)\s+(.+?)\s+(?:to|get|for)\s+.*?(?:ticket|entry)", text, re.I)
    if m:
        amt = m.group(2)
        cat = re.sub(r"[^A-Za-z0-9 &/+-]", "", m.group(3)).strip()
        mechanic = f"Stake {amt} on {cat} to receive 1 Prize Draw ticket."
    if not mechanic:
        m = re.search(r"Earn\s+1\s+RP.*?(?:ticket|entry)", text, re.I)
        if m: mechanic = m.group(0)

    cap = _grab(r"(?:Max(?:imum)?\s*)?(\d{1,4})\s+tickets?\s+per\s+week", text) or "100"

    featured = "Casino games"
    if re.search(r"Pragmatic", text, re.I): featured = "Pragmatic Play Slots"
    elif re.search(r"Evolution", text, re.I): featured = "Evolution live games"
    elif re.search(r"Games\s*Global", text, re.I): featured = "Games Global games"

    weekly_windows = _graball(rf"({MONTHS}\s+\d{{1,2}}.*?(?:{MONTHS}\s+\d{{1,2}}|$))", text)

    start = _grab(r"Start\s*Date.*?(\d{1,2}\s*[A-Za-z]{3,9}\s*\d{2,4})", text)
    end = _grab(r"End\s*Date.*?(\d{1,2}\s*[A-Za-z]{3,9}\s*\d{2,4})", text)

    lines = [ln.strip() for ln in text.splitlines() if re.search(r"([€$£]?\d[\d,]*\s*(Cash|Bonus|Free\s*Spins))\s*[-–]\s*\d+", ln, re.I)]
    prizes = []
    for ln in lines:
        m = re.search(r"([€$£]?\d[\d,]*\s*(?:Cash|Bonus|Free\s*Spins))\s*[-–]\s*(\d+)", ln, re.I)
        if m:
            prizes.append({"prize": m.group(1).strip(), "quantity": int(m.group(2))})

    return {
        "source_filename": filename,
        "title": title or "Prize Draw",
        "markets": markets,
        "mechanic": mechanic or "Complete the weekly Casino challenge to receive 1 Prize Draw ticket.",
        "entry_cap_per_week": cap,
        "featured": featured,
        "weekly_windows_text": weekly_windows[:8],
        "start_date": start,
        "end_date": end,
        "prizes": prizes,
    }
