# scripts/generate_qr.py
import sys, pathlib, qrcode

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "qr"
OUT.mkdir(exist_ok=True)

DEFAULT_URL = "https://vickymx.github.io/Multilingua/"  

def main():
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    if not url.endswith("/"):
        url += "/"
    img = qrcode.make(url)
    out = OUT / "qr_multilingual.png"
    img.save(out)
    print("Saved:", out)
    print("Points to:", url)

if __name__ == "__main__":
    main()