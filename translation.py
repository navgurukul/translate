import html
# Imports the Google Cloud Translation library
from google.cloud import translate
from get_lang import pali_transform
import os
import csv
from dotenv import dotenv_values

# Load the environment variables from the .env file
env_vars = dotenv_values('.env')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = env_vars.get('GOOGLE_APPLICATION_CREDENTIALS')

pre_replacements_file = 'pre-phrases'
post_replacements_file = 'post-phrases.csv'
pre_replacements = {}
post_replacements = {}

# Replace the phrases in the text with the pre-defined replacements before translation
def pre_replace_phrases(text, source_language, target_language):
    # Read the pre and post replacements from the csv files
    global pre_replacements
    if len(pre_replacements.keys()) == 0:
        with open('pre-phrases-'+source_language+'-'+target_language+'.csv', 'r',encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            pre_replacements = {row[0]: row[1] for row in reader}

    for phrase,replacement in pre_replacements.items():
        text = text.replace(phrase,replacement)

    return text

# Replace the phrases in the text with the replacements post automatic translation
def post_replace_phrases(text, source_language, target_language):
    global post_replacements
    if len(post_replacements.keys()) == 0:
        with open('post-phrases-'+source_language+'-'+target_language+'.csv','r',encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            post_replacements = {row[0]: row[1] for row in reader}

    for phrase,replacement in post_replacements.items():
        text = text.replace(phrase,replacement)

    return text

def translate_text_wrapper(text, source_language='en',target_language='hi', model='google') -> translate.TranslationServiceClient:
    """Translating Text."""

    if text.strip() == '':
        return ''

    project_id = "34917283366"


    text = pali_transform(text, source_language, target_language)

    text = pre_replace_phrases(text, source_language, target_language)

    client = translate.TranslationServiceClient()

    if model=='google':
        if target_language=='hi':
            # This one is a custom trained model in Hindi and wouldn't work for other languages.
            location = "us-central1"
            model = f"projects/{project_id}/locations/{location}/models/NM0ef5e2f059b5ad73"
            parent = f"projects/{project_id}/locations/{location}"

            # Translate text from source_language to target_language
            response = client.translate_text(
                request={
                    "parent": parent,
                    "contents": [text],
                    "model": model,
                    "mime_type": "text/html", # mime types: text/plain,text/html
                    "source_language_code": "en",
                    "target_language_code": target_language,
                }
            )
        else:
                location = "global"
                parent = f"projects/{project_id}/locations/{location}"

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
    else:
        print("Model not supported:", model)
        return

    translated_text = response.translations[0].translated_text
    # translated_text = "Translated String: " + text
    translated_text = post_replace_phrases(translated_text, source_language, target_language).replace('\n','').replace('<span class="notranslate">','').replace('</span>','')
    # replace all occurences of ascii characters like &#39 to the corresponding character

    translated_text = html.unescape(translated_text)

    print('\n'+translated_text+'\n\n')

    return translated_text
