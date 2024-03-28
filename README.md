# Using AI to Universalize Buddha's Teachings

## Description

This project aims to leverage artificial intelligence (AI) to universalize the teachings of Buddha beyond language barriers. By applying AI-based translation and transcription techniques to spiritual texts, the project seeks to make the wisdom and teachings accessible to a broader audience worldwide.

For a detailed project description, please refer to the [project description document](https://navgurukul.notion.site/Using-AI-to-universalize-Buddha-s-teachings-beyond-bf09169955e94213b06809c11848952e?pvs=4).

### Methods:

Translation: AI-powered tools translate spiritual texts into various languages.
Transcription: Converting audio recordings of teachings into text for further translation. 

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/navgurukul/translate.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the environment:

   - Create a `.env` file in the root directory of the project.
   - Add the necessary environment variables, such as API keys and file paths, to the `.env` file.

## Usage

1. Place your input Word document in the specified input directory.

2. Run the script:

   ```bash
   python script.py --input-file path/to/input.docx --output-file path/to/output.docx
   ```

   Replace `path/to/input.docx` and `path/to/output.docx` with the actual file paths.

3. The translated output will be saved to the specified output file.

## Contributing

Contributions to this project are welcome. To contribute, please follow these steps:

1. Fork the repository.

2. Create a new branch for your feature or bug fix.

3. Make your changes and commit them.

4. Push the changes to your forked repository.

5. Open a pull request in the main repository.

## Todo

1. Make this agnostic to language. There are some hard codings in the code to default to English to Hindi translation. Make all of this generic, to support Tamil, and other languages.

2. Write code to generate translation pairs for algorithm training and enhancements. Algorithm can be on the following lines:

## Algorithm to Generate Translation Pairs for Training (Markdown)

This document outlines an algorithm to generate English-Hindi sentence pairs suitable for training a translation algorithm. The approach leverages a provided translation function and a similarity metric to identify the closest Hindi sentence to the translated version of each English sentence.

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
   