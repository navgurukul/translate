# https://tipitaka.org/ios
import random
import time
import csv

def main():
    txt_file_path = "pali_pairs-4.csv"  # Replace with the path to your .txt file
    unique_special_chars_en = set()
    unique_special_chars_hi = set()

    exclude_chars = ['!','(',')','*','+',',','-','.',':',';','?','[',']','–','‘','’','\n','\t','\r',' ']

    with open('pali_pairs-4.csv', 'r', encoding="utf8") as file:
        reader = csv.reader(file)
        hi_chars = set()
        en_chars = set()

        for row in reader:
            try:
                hindi_word, english_word = row
            except ValueError as e:
                print(e, row)
            
            # update hi_chars with characters from hindi_word
            for char in hindi_word:
                hi_chars.add(char)
            for char in english_word:
                en_chars.add(char)

    for char in en_chars:
        char_code = ord(char)
        # print following randomly one in 50 times
        if random.randint(1, 50) == 1:
            print(char, char_code, ord('0'), ord('9'), ord('a'), ord('z'), ord('A'), ord('Z'))
            # sleep for 100 ms
            time.sleep(0.1)

        if (char_code < ord('0') or char_code > ord('9')) and \
            (char_code < ord('a') or char_code > ord('z')) and \
            (char_code < ord('A') or char_code > ord('Z')) and \
            char not in exclude_chars:
            unique_special_chars_en.add(char)
    
    for char in hi_chars:
        char_code = ord(char)
        # check if char_code is not from hindi unicode range
        if char not in exclude_chars:
            unique_special_chars_hi.add(char)

    print("Unique special characters:")
    print(unique_special_chars_en)
    print(unique_special_chars_hi)

if __name__ == "__main__":
    main()
