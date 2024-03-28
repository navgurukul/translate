"""
This script defines an algorithm to generate English-Hindi sentence pairs 
suitable for training a translation algorithm.

This approach leverages a provided translation function and a similarity metric 
to identify the closest Hindi sentence to the translated version of each English sentence.

**Inputs:**

* `en_file`: Path to the source language (English) file.
* `hi_file`: Path to the target language (Hindi) file.
* `translate_fn`: A function that translates text from source to target language (e.g., English to Hindi).

**Output:**

* A list of English-Hindi sentence pairs suitable for training a translation algorithm.

**Algorithm:**

1. **Load Text Files:**
   * Read the content of `en_file` and store each line (sentence) in a list called `en_sentences`.
   * Read the content of `hi_file` and store each line (sentence) in a list called `hi_sentences`.

2. **Translate English Sentences:**
   * Create a new list called `translated_en_sentences`.
   * For each sentence `en_sentence` in `en_sentences`:
       * Use `translate_fn` to translate `en_sentence` to Hindi.
       * Add the translated sentence to `translated_en_sentences`.

3. **Iterate through English Sentences:**
   * For each sentence `en_sentence` (and its corresponding translation `translated_en_sentence`) in `en_sentences` and `translated_en_sentences`:

       **Find Closest Hindi Match:**
           * Initialize `closest_hi_score` to negative infinity (very low score).
           * Initialize `closest_hi_sentence` to `None`.
           * For each sentence `hi_sentence` in `hi_sentences`:
               * Calculate the similarity score between `translated_en_sentence` and `hi_sentence` using the chosen similarity function (explained later). Let's call this score `score`.
               * If `score` is greater than `closest_hi_score`:
                   * Update `closest_hi_score` with `score`.
                   * Update `closest_hi_sentence` with `hi_sentence`.

       **Add Pair to Output:**
           * Add a tuple containing `en_sentence` and `closest_hi_sentence` to the output list.

**Similarity Function:**

This algorithm relies on a similarity function to compare translated English sentences (`translated_en_sentences`) and Hindi sentences (`hi_sentences`). Here are two options:

* **Simple Word Overlap:** Calculate the number of words that appear in both sentences.
* **More Advanced Techniques:** Use libraries or tools that provide semantic similarity scores between sentences, considering word meaning and context.

**Note:**

This algorithm finds the closest Hindi sentence based on the similarity between the translated English sentence and the original Hindi sentence.
Adjustments might be needed to handle sentences with different lengths.

**Output List:**

The final output will be a list of tuples, where each tuple contains an English sentence and its corresponding closest Hindi sentence based on the chosen similarity metric. This list can be used to train a translation algorithm.
"""

import docx

from docx import Document
from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph
import sys
from tokenizer import get_sentences_en, get_sentences_hi

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


def process_doc(source_filename, translated_filename, output_filename, source_language, translated_language):
    """
    Reads a docx file in order, replacing characters with spaces randomly,
    and creates a new doc with the updated content.
    """

    document = docx.Document(source_filename)
    source_strings = []

    for block in iter_block_items(document):
        if isinstance(block, Paragraph):
            source_strings.append(block.text)

        elif isinstance(block, Table):
            for i,row in enumerate(block.rows):
                for j,cell in enumerate(row.cells):
                    for paragraph in cell.paragraphs:
                        # source_strings.append(cell.paragraphs[0])
                        for run in paragraph.runs:
                            source_strings.append(run.text)


    # source_strings for each source_string use get_sentences_en and append that to the array
    for source_string in source_strings:
        sentences = get_sentences_en(source_string)
        source_strings.extend(sentences)
        print(sentences)
    source_strings = list(filter(lambda x: x != '', source_strings))
    source_strings = list(map(lambda x: x.strip().replace("\xa0",""), source_strings))
    print(source_strings.__len__())
    print(source_strings[:50])

if __name__ == '__main__':
    # Check if the correct number of command line arguments is provided
    if len(sys.argv) < 3:
        print("Usage: python script.py source_file translated_file [output_file] [source_language] [translated_language]")
        sys.exit(1)

    # Extract the input and output file names from command line arguments
    source_file = sys.argv[1]
    translated_file = sys.argv[2]

    # Extract the target language if provided,default to 'en' if not specified
    output_file = sys.argv[3] if len(sys.argv) > 3 else 'translation_pairs.tsv'
    source_language = sys.argv[4] if len(sys.argv) > 4 else 'en'
    translated_language = sys.argv[5] if len(sys.argv) > 3 else 'hi'

    # Call the function to output the translation
    process_doc(source_file, translated_file, output_file, source_language, translated_language)