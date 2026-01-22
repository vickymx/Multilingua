import json
import pathlib
import sys
from lxml import etree

ROOT = pathlib.Path(__file__).resolve().parent

XML_CANDIDATES = [ROOT / "texts.xml", ROOT / "data" / "texts.xml"]
DTD_CANDIDATES = [ROOT / "texts.dtd", ROOT / "data" / "texts.dtd"]
INDEX_CANDIDATES = [ROOT / "index.html", ROOT / "site" / "index.html"]

PLACEHOLDER = "/* DATA_PLACEHOLDER */"
SITE_URL = "https://vickymx.github.io/Multilingua/"

def pick_first_existing(paths, kind):
    for p in paths:
        if p.exists():
            return p
    print(f"ERROR: {kind} not found. Looked in:\n  " + "\n  ".join(str(p) for p in paths))
    sys.exit(1)

DATA = pick_first_existing(XML_CANDIDATES, "texts.xml")
DTD  = pick_first_existing(DTD_CANDIDATES, "texts.dtd")
INDEX = pick_first_existing(INDEX_CANDIDATES, "index.html")

def parse_and_validate():
    xml = etree.parse(str(DATA))
    dtd = etree.DTD(str(DTD))
    if not dtd.validate(xml):
        print("DTD validation failed:\n", dtd.error_log)
        sys.exit(1)
    return xml

def to_js_data(xml):
    out = []
    for entry in xml.xpath("//entry"):
        eid = entry.get("id")
        cat = (entry.findtext("category") or "").strip()
        langs = {}
        for lang in entry.findall("lang"):
            code = lang.get("code")
            title = (lang.findtext("title") or "").strip()
            content = (lang.findtext("content") or "").strip()
            langs[code] = {"title": title, "content": content}
        out.append({"id": eid, "category": cat, "langs": langs})
    return out

def inject_into_index(data):
    html = INDEX.read_text(encoding="utf-8")
    if PLACEHOLDER not in html:
        print(f"ERROR: placeholder {PLACEHOLDER!r} not found in {INDEX}")
        sys.exit(1)
    payload = "window.DATA = " + json.dumps(data, ensure_ascii=False) + ";"
    html = html.replace(PLACEHOLDER, payload)
    INDEX.write_text(html, encoding="utf-8")
    print(f"Injected {len(data)} entries into {INDEX}")

if __name__ == "__main__":
    xml = parse_and_validate()
    data = to_js_data(xml)
    inject_into_index(data)
    print("Done.")
    print(f"Open: {SITE_URL}")
