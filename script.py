import sys
import openai
from docx import Document
from dotenv import dotenv_values
import csv
import os
import time
import random
from docx.shared import RGBColor

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
openai.api_key = env_vars.get('OPENAI_API_KEY')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = env_vars.get('GOOGLE_APPLICATION_CREDENTIALS')

pre_replacements_file = 'pre-phrases.csv'
post_replacements_file = 'post-phrases.csv'

def read_secret_key():
    # Load the environment variables from the .env file
    env_vars = dotenv_values('.env')

    # Access the SECRET_KEY variable
    secret_key = env_vars.get('SECRET_KEY')

    return secret_key

with open(pre_replacements_file, 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    pre_replacements = {row[0]: row[1] for row in reader}

with open(post_replacements_file, 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    post_replacements = {row[0]: row[1] for row in reader}

def pre_replace_phrases(text):
    for phrase, replacement in pre_replacements.items():
        text = text.replace(phrase, replacement)

    return text

def post_replace_phrases(text):
    for phrase, replacement in post_replacements.items():
        text = text.replace(phrase, replacement)

    return text

def translate_paragraph_gpt(paragraph, target_language='hindi'):
    # Prepare the system message
    # system_message = {
    #     "role": "system",
    #     "content": "
    # }

    if paragraph.strip() == '':
        return ''

    # Prepare the user message with the paragraph to translate
    user_message = {
        "role": "user",
        "content": "Provide an easy to read translation in  " + target_language + ". Break longer sentences into shorter ones if needed to make it more readable but keep the meaning and key words intact.\n\n" + paragraph
    }

    # Generate translation using ChatGPT
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[user_message],
            max_tokens=3900,
            temperature=0.7,
            n=1,
            stop=None,
        )
    except Ellipsis as e:
        print("An error occured: ", str(e))
        sleep_duration = random.randint(5, 10)
        time.sleep(sleep_duration)
        return translate_paragraph_gpt(paragraph, target_language='hindi')
    # Retrieve the translated text from the API response

    translated_text = response.choices[0].text.strip()
    print(translated_text)
    return translated_text

def output_translation(input_path, output_path, target_language='en'):
    # Load the input document
    doc = Document(input_path)

    # Create a new document for the output
    output_doc = Document()

    # Iterate over paragraphs in the input document
    for paragraph in doc.paragraphs:
        text=paragraph.text.strip()
        if text=='':
            continue

        # Replace phrases in the paragraph before translation
        replaced_paragraph = pre_replace_phrases(text)

        # Break down the paragraph into sub-paragraphs if necessary
        sub_paragraphs = []
        if len(replaced_paragraph) > 2000:
            # TODO: change this paragraph to only break at periods
            sub_paragraphs = [replaced_paragraph[i:i+2000] for i in range(0, len(replaced_paragraph), 2000)]
        else:
            sub_paragraphs.append(replaced_paragraph)

        # Translate each sub-paragraph
        for sub_paragraph in sub_paragraphs:
            # Add the original sub-paragraph to the output document
            output_doc.add_paragraph(sub_paragraph)

            translated_sub_paragraph = translate_paragraph_google(sub_paragraph, target_language)
            translated_sub_paragraph = pre_replace_phrases(translated_sub_paragraph)
            p = output_doc.add_paragraph()
            run = p.add_run()
            run.text = translated_sub_paragraph
            font = run.font
            font.color.rgb = RGBColor(0, 128, 0)

            translated_sub_paragraph = translate_paragraph_gpt(sub_paragraph, target_language).replace('\n', '')
            translated_sub_paragraph = pre_replace_phrases(translated_sub_paragraph)
            # Add the translated sub-paragraph to the output document
            p = output_doc.add_paragraph()
            run = p.add_run()
            run.text = translated_sub_paragraph
            font = run.font
            font.color.rgb = RGBColor(25, 25, 112)

    # Save the output document
    output_doc.save(output_path)

if __name__ == '__main__':
    # Check if the correct number of command line arguments is provided
    if len(sys.argv) < 3:
        print("Usage: python script.py input_file output_file [target_language]")
        sys.exit(1)

    # Extract the input and output file names from command line arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Extract the target language if provided, default to 'en' if not specified
    target_language = sys.argv[3] if len(sys.argv) > 3 else 'hindi'

    # Call the function to output the translation
    output_translation(input_file, output_file, target_language)
