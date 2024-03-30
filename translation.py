import html
# Imports the Google Cloud Translation library
from google.cloud import translate
from get_lang import detect_language_and_pali
import os
import csv
from dotenv import dotenv_values

# Load the environment variables from the .env file
env_vars = dotenv_values('.env')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = env_vars.get('GOOGLE_APPLICATION_CREDENTIALS')

pre_replacements_file = 'pre-phrases.csv'
post_replacements_file = 'post-phrases.csv'

# Read the pre and post replacements from the csv files
with open(pre_replacements_file,'r',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    pre_replacements = {row[0]: row[1] for row in reader}

with open(post_replacements_file,'r',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    post_replacements = {row[0]: row[1] for row in reader}

# Replace the phrases in the text with the pre-defined replacements before translation
def pre_replace_phrases(text):
    for phrase,replacement in pre_replacements.items():
        text = text.replace(phrase,replacement)

    return text

# Replace the phrases in the text with the replacements post automatic translation
def post_replace_phrases(text):
    for phrase,replacement in post_replacements.items():
        text = text.replace(phrase,replacement)

    return text

def translate_text(text,target_language='hindi') -> translate.TranslationServiceClient:
    """Translating Text."""

    if text.strip() == '':
        return ''

    project_id = "chanakya-259818"

    text, lang,is_pali,pali_percent = detect_language_and_pali(text,0.01)

    text = pre_replace_phrases(text)

    if target_language == 'hindi':
        target_language = 'hi'

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    print(text)

    # Translate text from source_language to target_language
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/html", # mime types: text/plain,text/html
            "source_language_code": "en-US",
            "target_language_code": target_language,
        }
    )

    translated_text = response.translations[0].translated_text
    # translated_text = "Translated String: " + text
    translated_text = post_replace_phrases(translated_text).replace('\n','').replace('<span class="notranslate">','').replace('</span>','')
    # replace all occurences of ascii characters like &#39 to the corresponding character
    translated_text = html.unescape(translated_text).replace("ं","")

    return translated_text
