# Import modules
import os
import xml.etree.ElementTree as ET
import csv
from ai4bharat.transliteration import XlitEngine
import random

# Define paths
path1 = "tipitaka-xml/romn"
path2 = "tipitaka-xml/deva"

e = XlitEngine(src_script_type="indic", rescore=False)
out = e.translit_word("नमस्ते", lang_code="hi", topk=1)[0]
pairs = {}

exclude_files = ["abh03m10.mul.xml","s0403a.att.xml","s0403t.tik.xml","s0402a.att.xml","s0402m1.mul.xml","s0402m2.mul.xml","s0402m3.mul.xml","s0402t.tik.xml","s0404a.att.xml","s0404m1.mul.xml","s0404m2.mul.xml","s0404m3.mul.xml","s0404m4.mul.xml","s0404t.tik.xml"]

# Loop through files in path1
for filename in os.listdir(path1):
    flag=False
    # Find corresponding file in path2
    filepath1 = os.path.join(path1, filename)
    filepath2 = os.path.join(path2, filename)

    if filename in exclude_files:
        continue

    # Parse XML files and get root elements
    tree1 = ET.parse(filepath1)
    root1 = tree1.getroot()
    tree2 = ET.parse(filepath2)
    root2 = tree2.getroot()

    # Initialize dictionary
    word_dict = {}

    words1 = []
    words2 = []

    # Loop through <p> elements of root1
    for p1 in root1.findall(".//p"):
        text1 = p1.text
        # remove the starting spaces if text1 is not None
        if text1:
            text1 = text1.replace("॥","").lstrip()

        # n1 = p1.get("n")
        if text1:
            # print('\n\n')
            # map words such that ending commas, periods, etc. are removed
            words1 += map(lambda x: x.rstrip(".,;:!?"), text1.split())

    # Loop through text nodes of root2
    for p2 in root2.findall(".//p"):
        text2 = p2.text
        # remove the starting spaces
        if text2:
            text2 = text2.replace("॥","").lstrip()
        
        # n2 = p2.get("n")
        if text2:
            # Split text into words
            words2 += text2.split()

    if len(words1) != len(words2):
        print("Lengths not equal", filepath1, filepath2)
        flag=True
    # map words from words1 using transliterate using translit function using map function
    # roman_words = map(lambda x: e.translit_word(x, lang_code="hi", topk=1)[0], words2)

    for word1, word2 in zip(words1, words2):
    # , roman_words):
        # if flag and random.randint(0, 20) == 0:
        #     print(word1, word2, filepath1, filepath2)
        if not flag:
            if word2 in pairs.keys():
                pairs[word2].append(word1)
            else:
                pairs[word2] = [word1]

    for key in pairs.keys():
        pairs[key] = list(set(pairs[key]))

# Write dictionary to CSV file
with open("pali_pairs" + ".csv", "w", encoding="utf-8") as csvfile:
    # write pairs in a csv file, with the first column being the key, and the values array across multiple columns
    writer = csv.writer(csvfile)
    for key, value in pairs.items():
        writer.writerow([key] + value)