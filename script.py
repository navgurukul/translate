#!/usr/bin/env python
# encoding: utf-8

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import docx
import random

from docx import Document
from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph

import html
import sys
import openai
from docx import Document
from dotenv import dotenv_values
import csv
import os
import time
import random
from docx.shared import RGBColor
from tqdm import tqdm

from get_lang import detect_language_and_pali

# Imports the Google Cloud Translation library
from google.cloud import translate

# Load the environment variables from the .env file
env_vars = dotenv_values('.env')
openai.api_key = env_vars.get('OPENAI_API_KEY')
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

def iter_block_items(parent):
    """
    Generate a reference to each paragraph and table child within *parent*,
    in document order. Each returned value is an instance of either Table or
    Paragraph. *parent* would most commonly be a reference to a main
    Document object, but also works for a _Cell object, which itself can
    contain paragraphs and tables.
    """
    if isinstance(parent, _Document):
        parent_elm = parent.element.body
        # print(parent_elm.xml)
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("something's not right")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def process_doc(input_filename, output_filename, target_language):
    """
    Reads a docx file in order, replacing characters with spaces randomly,
    and creates a new doc with the updated content.
    """

    document = docx.Document(input_filename)
    new_document = docx.Document()
    pbar = tqdm(total=len(document.paragraphs))

    for block in iter_block_items(document):
        if isinstance(block, Paragraph):
            new_paragraph = new_document.add_paragraph()
            
            for run in block.runs:
                new_run = new_paragraph.add_run(run.text)
                new_run.font.name = run.font.name  # Preserve font
                new_run.font.size = run.font.size  # Preserve font size
                new_run.bold = run.bold  # Preserve bold formatting
                new_run.italic = run.italic  # Preserve italic formatting

            new_run = new_paragraph.add_run(translate_paragraph("google", block.text, target_language))
            new_run.font.name = run.font.name  # Preserve font
            new_run.font.color.rgb = RGBColor(0,128,0)
            new_run.font.size = run.font.size  # Preserve font size
            new_run.bold = run.bold  # Preserve bold formatting
            new_run.italic = run.italic  # Preserve italic formatting
            font = run.font

        elif isinstance(block, Table):
            new_table = new_document.add_table(rows=len(block.rows)*2, cols=len(block.columns))
            new_table.style = "Table Grid"

            # make a 2d array with len(block.rows) len(block.columns) dimensions and save some values in it
            table_values = [[None for _ in range(len(block.columns))] for _ in range(len(block.rows))]

            for i,row in enumerate(block.rows):
                for j,cell in enumerate(row.cells):
                    for paragraph in cell.paragraphs:
                        new_paragraph = cell.paragraphs[0]  # Access existing paragraph
                        for run in paragraph.runs:
                            if table_values[i][j] is None:
                                table_values[i][j] = [run.text + "\n", run.font.name, run.font.size, run.bold, run.italic]
                            table_values[i][j][0] = table_values[i][j][0]+run.text+"\n"

                    table_values[i][j][0]=table_values[i][j][0].strip()

            for i,row in enumerate(new_table.rows):
                for j, cell in enumerate(row.cells):
                    new_i = i/2
                    # convert new_i to int
                    new_i = int(new_i)
                    if i%2==0:
                        cell.text = table_values[new_i][j][0]
                    else:
                        cell.text = translate_paragraph("google", table_values[new_i][j][0], target_language)

        pbar.update(1)
        

    pbar.close()
    new_document.save(output_filename)

# Read the secret key from the .env file
def read_secret_key():
    # Load the environment variables from the .env file
    env_vars = dotenv_values('.env')
    # Access the SECRET_KEY variable
    secret_key = env_vars.get('SECRET_KEY')
    return secret_key

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

# Initialize Translation client
def translate_paragraph_google(paragraph,target_language='hindi') -> translate.TranslationServiceClient:
    """Translating Text."""

    project_id = "chanakya-259818"

    paragraph, lang,is_pali,pali_percent = detect_language_and_pali(paragraph,0.01)

    paragraph = pre_replace_phrases(paragraph)

    if target_language == 'hindi':
        target_language = 'hi'

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    print(paragraph)

    # Translate text from source_language to target_language
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [paragraph],
            "mime_type": "text/html", # mime types: text/plain,text/html
            "source_language_code": "en-US",
            "target_language_code": target_language,
        }
    )

    translated_text = response.translations[0].translated_text
    # translated_text = "Translated String: " + paragraph
    translated_text = post_replace_phrases(translated_text).replace('\n','').replace('<span class="notranslate">','').replace('</span>','')
    # replace all occurences of ascii characters like &#39 to the corresponding character
    translated_text = html.unescape(translated_text).replace("ं","")

    return '\n'+translated_text

def translate_paragraph_gpt(paragraph,target_language='hindi'):
    if paragraph.strip() == '':
        return ''
    
    PROMPT = env_vars.get('GPT_PROMPT').replace('TARGET_LANGUAGE',target_language)

    # Prepare the user message with the paragraph to translate
    user_message = {
        "role": "user",
        "content": PROMPT + paragraph
    }

    # Generate translation using ChatGPT
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            # model="gpt-3.5-turbo-16k",
            messages=[user_message],
            max_tokens=3900,
            temperature=0.7,
            n=1,
            stop=None,
        )
    except Exception as e:
        print("An error occured: ",str(e))
        sleep_duration = random.randint(5,15)
        time.sleep(sleep_duration)
        return translate_paragraph_gpt(paragraph,target_language='hindi')
    # Retrieve the translated text from the API response

    print(response.choices[0].message.content)

    translated_text = response.choices[0].message.content.strip()
    return translated_text

def translate_paragraph(model,text,target_language):
    if text.strip() == '':
        return ''
    # Translate the sub-paragraph based on the model
    if model=='gpt':
        return translate_paragraph_gpt(text,target_language)
    elif model=='google':
        return translate_paragraph_google(text,target_language)
    else:
        raise Exception('Invalid model')

if __name__ == '__main__':
    # Check if the correct number of command line arguments is provided
    if len(sys.argv) < 3:
        print("Usage: python script.py input_file output_file [target_language]")
        sys.exit(1)

    # Extract the input and output file names from command line arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Extract the target language if provided,default to 'en' if not specified
    target_language = sys.argv[3] if len(sys.argv) > 3 else 'hindi'

    # Call the function to output the translation
    process_doc(input_file, output_file, target_language)