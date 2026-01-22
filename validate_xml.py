# Validate XML against DTD
# Usage: python scripts/validate_xml.py
from lxml import etree
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "texts.xml"
DTD = ROOT / "data" / "texts.dtd"

xml = etree.parse(str(DATA))
dtd = etree.DTD(str(DTD))
ok = dtd.validate(xml)
if ok:
    print("XML is valid against DTD.")
    sys.exit(0)
else:
    print("XML is NOT valid. Errors:")
    print(dtd.error_log)
    sys.exit(1)