import sys
import openai
from docx import Document
from dotenv import dotenv_values
import csv

# Load the environment variables from the .env file
env_vars = dotenv_values('.env')
openai.api_key = env_vars.get('OPENAI_API_KEY')
replacements_file = 'pre-phrases.csv'

def read_secret_key():
    # Load the environment variables from the .env file
    env_vars = dotenv_values('.env')

    # Access the SECRET_KEY variable
    secret_key = env_vars.get('SECRET_KEY')

    return secret_key

with open(replacements_file, 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    replacements = {row[0]: row[1] for row in reader}

def replace_phrases(text):
    for phrase, replacement in replacements.items():
        text = text.replace(phrase, replacement)

    return text

def translate_paragraph(paragraph, target_language='hindi'):
    # Prepare the system message
    # system_message = {
    #     "role": "system",
    #     "content": "
    # }

    # Prepare the user message with the paragraph to translate
    user_message = {
        "role": "user",
        "content": "Provide an easy to read translation in  " + target_language + ". Break longer sentences into shorter ones if needed to make it more readable but keep the meaning and key words intact.\n\n" + paragraph
    }

    # Generate translation using ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[user_message],
        max_tokens=3900,
        temperature=0.7,
        n=1,
        stop=None,
    )

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
        replaced_paragraph = replace_phrases(text)

        # Break down the paragraph into sub-paragraphs if necessary
        sub_paragraphs = []
        if len(replaced_paragraph) > 2000:
            sub_paragraphs = [replaced_paragraph[i:i+2000] for i in range(0, len(replaced_paragraph), 2000)]
        else:
            sub_paragraphs.append(replaced_paragraph)

        # Translate each sub-paragraph
        translated_sub_paragraphs = []
        for sub_paragraph in sub_paragraphs:
            translated_sub_paragraph = translate_paragraph(sub_paragraph, target_language)
            translated_sub_paragraphs.append(translated_sub_paragraph)

        # Add the original and translated sub-paragraphs to the output document
        for i in range(len(sub_paragraphs)):
            # Add the original sub-paragraph to the output document
            # output_doc.add_paragraph(sub_paragraphs[i])
            output_doc.add_paragraph(sub_paragraphs[i])

            # Add the translated sub-paragraph to the output document
            output_doc.add_paragraph(translated_sub_paragraphs[i])

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
