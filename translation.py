import html
# Imports the Google Cloud Translation library
import openai
from google.cloud import translate
from get_lang import pali_transform
import os
import csv
from dotenv import dotenv_values
import random
import time

env_vars = dotenv_values('.env')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = env_vars.get('GOOGLE_APPLICATION_CREDENTIALS')
openai_key = env_vars.get('OPENAI_API_KEY')

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

    if target_language=='hi':
        lang_full = 'Hindi'
    elif target_language=='ta':
        lang_full = 'Tamil'
    elif target_language=='en':
        lang_full = 'English'
    else:
        raise ValueError("Invalid target language")
    
    if source_language=='en':
        source_lang_full = "English"

    if model=='google':
        if target_language=='hi':
            # This one is a custom trained model in Hindi and wouldn't work for other languages.
            location = "us-central1"
            model = f"projects/{project_id}/locations/{location}/models/NM0ef5e2f059b5ad73"
            parent = f"projects/{project_id}/locations/{location}"

            # Translate text from source_language to target_language
            # Generate a random sleep time between 0 and 4 seconds
            sleep_time = random.uniform(0, 3)

            # Sleep for the generated time
            time.sleep(sleep_time)

            # Translate text from source_language to target_language
            try:
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
            except:
                response = {"translations": [{"translated_text": ""}]}
        else:
                location = "global"
                parent = f"projects/{project_id}/locations/{location}"

                # Translate text from source_language to target_language
                # Generate a random sleep time between 0 and 4 seconds
                sleep_time = random.uniform(0, 3)

                # Sleep for the generated time
                time.sleep(sleep_time)

                try:
                    response = client.translate_text(
                        request={
                            "parent": parent,
                            "contents": [text],
                            "mime_type": "text/html", # mime types: text/plain,text/html
                            "source_language_code": "en-US",
                            "target_language_code": target_language,
                        }
                    )
                except:
                    response = {"translations": [{"translated_text": ""}]}

        print(response)
        translated_text = response.translations[0].translated_text

    elif model=='gpt':
            
        # Set up the OpenAI API client
        openai.api_key = openai_key

        # Define the prompt for the GPT-3.5 model
        prompt = f"""{text.replace('<span class="notranslate">','').replace('</span>','')}"""
        message = f"You are a translator for a book on Vipassana on Buddha's teachings. Please translate from {source_lang_full} to {lang_full}. Make the translation sound as natural as possible."

        print(prompt)

        # Generate the response using the GPT-3.5 model
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": message},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
        )

        # print(response.choices[0].message.content)

        # Extract the generated response from the API response
        translated_text = response.choices[0].message.content.strip()

    elif model=='deepl':
        import requests
        import json

        url = "https://api-free.deepl.com/v2/translate"

        payload = {
            "auth_key": "5b7e1f1e-8b0f-6b5f-5c5d-6d3f6d3d6d3d",
            "text": text,
            "target_lang": target_language.upper()
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        translated_text = response.json()['translations'][0]['text']

    else:
        print("Model not supported:", model)
        return

    # translated_text = "Translated String: " + text
    translated_text = post_replace_phrases(translated_text, source_language, target_language).replace('\n','').replace('<span class="notranslate">','').replace('</span>','')
    # replace all occurences of ascii characters like &#39 to the corresponding character

    translated_text = html.unescape(translated_text)

    print('\n'+translated_text+'\n\n')

    return translated_text
