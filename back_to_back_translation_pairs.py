# Create a script in python to read a docx file with one paragraph after other. paragraphs are alternatively in hindi and english. create a tsv file from this, where the english paragraph is in the first column, and the second column is hindi paragraph. use a simple language detection tool which can be based on the characters used in the text to identify which is hindi and which is english.

import docx
import os
import sys
import re
import langid
import argparse
import nltk.data

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# A function that inputs a paragraph and returns an array of the sentences in the paragraph
def get_sentences_en(paragraph):
    # Split the paragraph into sentences
    sentences = tokenizer.tokenize(paragraph)
    # re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', paragraph)
    return sentences

# A function that inputs a paragraph in Hindi and returns an array of the sentences in the paragraph
def get_sentences_hi(paragraph):
    # Split the paragraph into sentences
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=।|\?)\s', paragraph)
    return sentences

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="input file")
    parser.add_argument("output_file", help="output file")
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    doc = docx.Document(input_file)
    paragraphs = doc.paragraphs
    # map the above paragraphs text to a new variable paragraphs_text
    paragraphs_text = [paragraph.text.strip() for paragraph in paragraphs]
    paragraphs_text = [paragraph.replace('\t','') for paragraph in paragraphs_text]
    
    # map the paragraphs to remove the first character of the paragraphs beginning with — or -
    paragraphs_text = [re.sub(r'^—', '', paragraph) for paragraph in paragraphs_text]
    paragraphs_text = [re.sub(r'^-', '', paragraph) for paragraph in paragraphs_text]

    # filter out the empty paragraphs
    paragraphs_text = list(filter(lambda x: x != '', paragraphs_text))
    paragraphs_text = list(filter(lambda x: x != '—', paragraphs_text))

    langid.set_languages(['en', 'hi'])

    g = open("unmatched.tsv", 'w', encoding='utf-8')

    with open(output_file, 'w', encoding='utf-8') as f:  # Specify encoding as utf-8

        # Initialize a variable i to 0
        i = 0

        # Loop while i is less than max_len
        while i < len(paragraphs_text) - len(paragraphs_text)%2:
            # Do the same operations as in the for loop
            if paragraphs_text[i] == '':
                i += 1
                continue

            if langid.classify(paragraphs_text[i])[0] == 'en':
                en_sentences = get_sentences_en(paragraphs_text[i])
                hi_sentences = get_sentences_hi(paragraphs_text[i+1])

                if len(en_sentences) == len(hi_sentences):
                    for j in range(len(en_sentences)):
                        f.write(en_sentences[j] + '\t' + hi_sentences[j]+'\n')
                else:
                    # write these cases in a unmatched.tsv file
                    for j in range(max(len(en_sentences),len(hi_sentences))):
                        if j < min(len(en_sentences), len(hi_sentences)):
                            g.write(en_sentences[j] + '\t' + hi_sentences[j]+'\n')
                        if j >= len(en_sentences):
                            g.write('\t' + hi_sentences[j]+'\n')
                        if j >= len(hi_sentences):
                            g.write(en_sentences[j] + '\t'+'\n')

                    g.write('\n')

                    # print unmatched strings in terminal as well
                    for j in range(max(len(en_sentences),len(hi_sentences))):
                        if j < min(len(en_sentences), len(hi_sentences)):
                            print(en_sentences[j] + '\t' + hi_sentences[j]+'\n')
                        if j >= len(en_sentences):
                            print('\t' + hi_sentences[j]+'\n')
                        if j >= len(hi_sentences):
                            print(en_sentences[j] + '\t'+'\n')
            else:
                print(paragraphs_text[i] + '\t' + paragraphs_text[i+1] + '\n')
            
            # Increment i by 2
            i += 2
    
    g.close()

if __name__ == '__main__': 
    main()