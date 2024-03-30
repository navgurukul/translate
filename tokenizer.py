import re
import re
import nltk.data

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
punkt_param = PunktParameters()
abbreviation = ['e.g', 'i.e', 'mr', 'mrs', 'dr', 'vs', 'etc', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']
punkt_param.abbrev_types = set(abbreviation)
tokenizer = PunktSentenceTokenizer(punkt_param)

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

def get_sentences(paragraph, lang):
    if lang=='hi':
        return get_sentences_hi(paragraph)
    elif lang=='en':
        return get_sentences_en(paragraph)
    else:
        AssertionError("Language not supported")
