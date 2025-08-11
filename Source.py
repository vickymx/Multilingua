from lxml import etree
import qrcode
import os

def parse_leaflet_xml(xml_file):
    if not os.path.exists(xml_file):
        print(f"Error: XML file '{xml_file}' не е намерен!")
        return {}

    tree = etree.parse(xml_file)
    root = tree.getroot()
    indications = root.find(".//section[@id='indications']")

    texts = {}
    for lang in ['bg', 'en', 'fr']:
        content = indications.find(f"content[@lang='{lang}']")
        if content is not None:
            sentences = content.findall("sentence")
            if sentences:
                text = []
                for sent in sentences:
                    words = sent.findall("word")
                    sentence_text = ""
                    for word in words:
                        w = word.text if word.text else ""
                        if w in [".", ",", "!", "?", ":", ";"]:
                            sentence_text += w
                        else:
                            if sentence_text:
                                sentence_text += " " + w
                            else:
                                sentence_text = w
                    text.append(sentence_text)
                texts[lang] = "\n".join(text)
            else:
                texts[lang] = content.text.strip() if content.text else ""
    return texts

def generate_css(output_file="styles.css"):
    css_content = """
body {
    font-family: 'Roboto', sans-serif;
    background-color: #f9f9f9;
    color: #333;
    text-align: center;
    margin: 50px;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.lang {
    display: none;
    margin-top: 20px;
    max-width: 600px;
    text-align: center;
}
button {
    margin: 5px;
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1em;
}
button:hover {
    background-color: #45a049;
}
.lang p {
    font-size: 1.1em;
    line-height: 1.5em;
    margin: 0 auto;
}
"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(css_content)
    print(f"CSS file saved to {output_file}")

def generate_html_multilingual(texts, output_file="index.html"):
    html_start = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Leaflet</title>
    <link rel="stylesheet" href="styles.css">
    <script>
        function showLang(lang) {
            document.querySelectorAll('.lang').forEach(el => el.style.display = 'none');
            document.getElementById(lang).style.display = 'block';
        }
        window.onload = function() {
            showLang('bg');
        }
    </script>
</head>
<body>
    <h1>Избери език / Choose language / Choisissez la langue</h1>
    <div id="buttons">
        <button onclick="showLang('bg')">Български</button>
        <button onclick="showLang('en')">English</button>
        <button onclick="showLang('fr')">Français</button>
    </div>
"""
    html_content = ""
    for lang, content in texts.items():
        content_html = content.replace("\n", "<br>")
        lang_title = {'bg': 'Показания', 'en': 'Indications', 'fr': 'Indications'}.get(lang, lang.upper())
        html_content += f"""
    <div id="{lang}" class="lang">
        <h2>{lang_title}</h2>
        <p>{content_html}</p>
    </div>
"""
    html_end = """
</body>
</html>
"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_start + html_content + html_end)
    print(f"HTML file saved to {output_file}")

def generate_qr(url, output_file="medicine_qr.png"):
    qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_file)
    print(f"QR code saved to {output_file}")

if __name__ == "__main__":
    xml_file = "medicine.xml"
    html_file = "index.html"
    css_file = "styles.css"

    texts = parse_leaflet_xml(xml_file)
    generate_css(css_file)
    generate_html_multilingual(texts, html_file)

    github_url = "https://vickymx.github.io/Multilingua/"  # Смени с твоя URL
    generate_qr(github_url, "medicine_qr.png")
