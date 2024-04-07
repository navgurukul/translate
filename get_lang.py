import docx
import langid
import csv
import openai
import os
from dotenv import load_dotenv

import enchant

d = enchant.Dict("en_US")
word = "Hello"

# https://tipitaka.org/deva/cscd/vin01m.mul0.xml : Hindi
# https://tipitaka.org/romn/cscd/vin01m.mul0.xml : English

# pali_chars_en = ['व', '८', 'इ', 'र', 'ु', '३', 'म', 'आ', 'य', 'क', 'ा', "'", 'ऐ', 'ट', 'ी', 'ṇ', '`', 'ै', 'ङ', 'द', 'ह', '्', 'उ', '०', '…', 'छ', '\ufeff', 'ि', 'न', 'ñ', 'त', 'ळ', 'झ', '=', 'ṭ', 'ठ', 'ञ', 'ऊ', '"', 'औ', 'च', 'ब', 'घ', 'ं', 'ṃ', 'अ', 'थ', 'ग', 'ण', 'भ', 'प', 'ू', '॰', '१', 'ज', '४', '६', 'ल', 'ध', 'ī', 'ū', 'ख', 'फ', 'े', 'ए', '५', 'ढ', '७', 'ḍ', 'स', 'ओ', '२', 'ṅ', 'ो', '९', '\u200d', 'ḷ', 'ई', 'ः', 'ड', 'ौ', 'ā']
pali_chars_en = {'ः', 'ṅ', 'ḷ', 'ḍ','ṇ', 'ā', 'ū', 'ṭ', 'ऐ', 'ै', 'ī', 'ṃ', 'ñ'}

pali_dict_en_to_hi = {}
pali_dict_hi_to_en = {}
sorted_keys_en = []
sorted_keys_hi = []

def initialise_pali_dicts():
    # first column in pali_pairs.csv file is hindi word, and the second column is english worddef pali_transliterate_en_to_hi(text: str) -> str:
    # read pali_pairs.csv file (first column contains the hindi word, and the second column contains the corresponding english word)
    # for each row in the file, replace the english word with the hindi word
    with open('pali_pairs.csv', 'r', encoding="utf8") as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                hindi_word, english_word = row
            except ValueError as e:
                print(e, row)

            if not english_word in pali_dict_en_to_hi:
                pali_dict_en_to_hi[english_word] = hindi_word
            if not hindi_word in pali_dict_hi_to_en:
                pali_dict_hi_to_en[hindi_word] = english_word
    
    # Sort the keys by length in descending order
    sorted_keys_en[:] = sorted(pali_dict_en_to_hi.keys(), key=len, reverse=True)
    # remove keys less than length 4 from sorted_keys_en
    sorted_keys_en[:] = [key for key in sorted_keys_en if len(key) > 3]
    sorted_keys_hi[:] = sorted(pali_dict_hi_to_en.keys(), key=len, reverse=True)
    sorted_keys_hi[:] = [key for key in sorted_keys_hi if len(key) > 3]

initialise_pali_dicts()

def find_smallest_key(pali_dict, word):
    """Finds the smallest key in the dictionary that contains the word as a substring.

    Args:
    pali_dict: A dictionary where keys are English words and values are their Hindi translations.
    word: The word to search for in the dictionary keys.

    Returns:
    The smallest key in the dictionary that contains the word as a substring, or None if no such key is found.
    """

    smallest_key = None
    print(word.lower())
    for key in pali_dict:
        if word.lower() in key:
            if smallest_key is None or key < smallest_key:
                smallest_key = key
    return smallest_key

# This function takes as input a string, and returns a tuple of three values: # - language: the detected language of the text, either “en” or “hi” # - is_pali: a boolean value indicating whether the text contains more than 3% Pali characters # - pali_percent: the percentage of Pali characters in the text
def pali_transform(text: str) -> tuple: 
    # for all keys in pali_dict_en_to_hi, replace the key with the value in text
    words = text.split()
    for i, word in enumerate(words):
        pmark = ''

        if word.endswith((',', '.', '?', '!', ':', ';')):
            pmark = word[-1]
            word = word.rstrip(pmark)

        if any(char in word for char in pali_chars_en):
            word = word.replace("-","")
            if word.lower() in pali_dict_en_to_hi:
                words[i] = pali_dict_en_to_hi[word.lower()]
                words[i] = '<span class="notranslate">' + words[i] + "</span>"
                print(words[i], " from exact match")
            
            else:
                smallest_key = find_smallest_key(pali_dict_en_to_hi, word.lower())
                if smallest_key != None:
                    # Read the API key from the .env file

                    load_dotenv()
                    api_key = os.getenv("OPENAI_API_KEY")

                    # Set up the OpenAI API client
                    openai.api_key = api_key

                    # Define the prompt for the GPT-3.5 model
                    prompt = f"""
                    Devnagiri transliteration of {smallest_key} is {pali_dict_en_to_hi[smallest_key]}

                    From within this transliteration, find the transliteration of {word.lower()}. Do this from within the transliteration that I provided.

                    Respond the transliterated output in devnagiri script in a single word.
                    """

                    # Generate the response using the GPT-3.5 model
                    response = openai.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": prompt},
                        ],
                        max_tokens=1000,
                        n=1,
                        stop=None,
                        temperature=0.1,
                    )

                    print(response.choices[0].message.content)

                    # Extract the generated response from the API response
                    generated_text = response.choices[0].message.content.strip()

                    words[i] = '<span class="notranslate">' + generated_text + "</span>"

                    # Print the generated response
                    print(generated_text, "from partial match")

        elif not d.check(word):
            try:
                words[i] = pali_dict_en_to_hi[word.lower()]
                words[i] = '<span class="notranslate">' + words[i] + "</span>"
            except:
                pass
        
        words[i] = words[i] + pmark
    text = ' '.join(words)

    print(text)

    return text

def pali_transliterate_en_to_hi(text: str) -> str:
    # read pali_pairs.csv file (first column contains the hindi word, and the second column contains the corresponding english word)
    # for each row in the file, replace the english word with the hindi word
    # return the text
    with open('pali_pairs.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            hindi_word = row[0]
            english_word = row[1]
            text = text.replace(english_word, hindi_word)
    return text