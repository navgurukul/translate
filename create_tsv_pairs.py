import csv
import difflib
import PyPDF2
from dotenv import dotenv_values
import os
# Imports the Google Cloud Translation library
from google.cloud import translate

# Initialize Translation client
def translate_paragraph_google(paragraph, target_language='hindi') -> translate.TranslationServiceClient:
    """Translating Text."""

    project_id = "chanakya-259818"

    if target_language == 'hindi':
        target_language = 'hi'

    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    # Translate text from English to French
    # Detail on supported types can be found here:
    # https://cloud.google.com/translate/docs/supported-formats
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [paragraph],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": "en-US",
            "target_language_code": target_language,
        }
    )

    return response.translations[0].translated_text

# Load the environment variables from the .env file
env_vars = dotenv_values('.env')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = env_vars.get('GOOGLE_APPLICATION_CREDENTIALS')

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(min(3, len(pdf_reader.pages))):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text

def create_translation_pairs(source_file, target_file, output_file):
    source_text = extract_text_from_pdf(source_file)
    target_text = extract_text_from_pdf(target_file)

    source_lines = source_text.split('\n')
    target_lines = target_text.split('\n')

    translated_lines = []
    for line in source_lines:
        # translated_lines.append(translate_paragraph_google(line, 'hindi'))
        pass

    print(target_lines)
    print(translated_lines)

    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(['Source', 'Translation'])

        for target_line in target_lines:
            matching_line = difflib.get_close_matches(target_line, translated_lines, n=1, cutoff=0.8)
            if matching_line:
                source_line = matching_line[0]
                index = translated_lines.index(source_line)
                writer.writerow([source_lines[index].strip(), target_line.strip()])

# Usage example
source_file_path = 'source.pdf'
target_file_path = 'target.pdf'
output_file_path = 'translation_pairs.tsv'

create_translation_pairs(source_file_path, target_file_path, output_file_path)