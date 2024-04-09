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

## Key Files
(Documentation Inside)

script.py (every time)
To translate an existing docx file

generate_pali_dictionary.py (one time)
To generate Pali feels from tipitaka-xml

generate-translation-pairs-from-two-different-texts.py
Generate translation pairs from two different Word files, and then align them using tkinter library (To generate pairs for further training of the algorithm)