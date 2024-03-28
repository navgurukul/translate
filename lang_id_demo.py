import docx
import langid

# https://tipitaka.org/deva/cscd/vin01m.mul0.xml : Hindi
# https://tipitaka.org/romn/cscd/vin01m.mul0.xml : English

def main():
    docx_file_path = "abridged.docx"  # Replace with the path to your DOCX file
    doc = docx.Document(docx_file_path)

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if text:
            first_50_chars = text[:50]
            language, _ = langid.classify(text)
            print(f"Input: {first_50_chars}... | Detected Language: {language}")

if __name__ == "__main__":
    langid.set_languages(['en', 'hi','lv'])
    main()
