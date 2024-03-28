import docx
import langid
import csv

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
    with open('pali_pairs-4.csv', 'r', encoding="utf8") as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                hindi_word, english_word = row
            except ValueError:
                print(row)

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

def main():
    docx_file_path = "Kalyanamitta_talk - Hindi.docx"  # Replace with the path to your DOCX file
    doc = docx.Document(docx_file_path)

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if text:
            otext = text[:50]
            # Use the detect_language_and_pali function to get the results
            text, language, is_pali, pali_percent = detect_language_and_pali(text,0.05)
            first_50_chars = text[:50]
            # Print the results
            print(f"{otext} \n{first_50_chars} \nDetected Language: {language} | Is Pali: {is_pali} | Pali Percent: {pali_percent}\n")

# This function takes as input a string, and returns a tuple of three values: # - language: the detected language of the text, either “en” or “hi” # - is_pali: a boolean value indicating whether the text contains more than 3% Pali characters # - pali_percent: the percentage of Pali characters in the text
def detect_language_and_pali(text: str, threshold: int) -> tuple: 
    # Use langid to classify the language of the text
    language, _ = langid.classify(text)
    # Count the number of Pali characters in the text
    pali_count = sum(1 for c in text if c in pali_chars_en)
    # Calculate the percentage of Pali characters in the text
    pali_percent = pali_count / len(text)
    # Check if the percentage is more than 3%
    is_pali = pali_percent > threshold
    # Return the tuple of results

    # if is_pali:
    # for all keys in pali_dict_en_to_hi, replace the key with the value in text
    if language == 'en':
        words = text.split()
        for i, word in enumerate(words):
            if any(char in word for char in pali_chars_en):
                if word.lower() in pali_dict_en_to_hi:
                    words[i] = pali_dict_en_to_hi[word.lower()]
                    words[i] = '<span class="notranslate">' + words[i] + "</span>"
                    print(words[i])

        text = ' '.join(words)
    
    # elif language == 'hi':
    #     for key in sorted_keys_hi.keys():
    #         if key in text:
    #             print(key, pali_dict_hi_to_en[key])
    #             text = text.replace(key, pali_dict_hi_to_en[key])

    return (text, language, is_pali, pali_percent)

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

if __name__ == "__main__":
    # Set the languages to be detected
    langid.set_languages(['en', 'hi'])
    main()
