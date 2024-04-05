import json
import tkinter as tk
from tkinter import Message
from tkinter import ttk
from similarity import hindi_sentence_similarity, words_intersection
source_box, translated_box, target_box, input_box, similarity_score_box = None, None, None, None, None

root = tk.Tk()
root.title("Translation Pairs' Generation")

SIMILARITY_SCORE_THRESHOLD = 0.6
WORDS_INTERSECTION_THRESHOLD = 0.399
NUM_ITEMS_FOR_DISPLAY = 10

def show_notification(text, color="dark blue"):
    msg = Message(root, text=text, foreground=color)
    msg.pack()
    root.after(5000, msg.destroy)

def undo_adding(key=None):
    print("CAME HERE")
    # Remove the last pair from translation_pairs.tsv file
    with open('translation_pairs.tsv', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lin = lines.pop()
    with open('translation_pairs.tsv', 'w', encoding='utf-8') as f:
        f.writelines(lines)

    sen1,sen2 = lin.split('\t')[0], lin.split('\t')[1]

    with open('sentences.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
        source_sentences = data["source_sentences"]
        translated_sentences = data["translated_sentences"]
        target_sentences = data["target_sentences"]

    # Add the first part to source_sentences head
    source_sentences.insert(0, sen1)
    # Add the second part to target_sentences head
    target_sentences.insert(0, sen2)
    # Add an empty value "NA" to the translated_sentences head
    translated_sentences.insert(0, "NA")

    # Flush the changes to sentences.json
    flush_sentences_to_csv(source_sentences, translated_sentences, target_sentences)

    # Call the display function
    display_sentences(source_sentences, translated_sentences, target_sentences)
    
    print ("Undo")

def delete_from_source(key=None):
    input_box.delete(1.0, tk.END)
    # read the json file and print source_sentences, translated_sentences, target_sentences
    with open('sentences.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
        source_sentences = data["source_sentences"]
        translated_sentences = data["translated_sentences"]
        target_sentences = data["target_sentences"]
    # Implement logic to delete selected sentence from source
    flush_sentences_to_csv(source_sentences[1:], translated_sentences[1:], target_sentences)
    pass

def delete_from_translation(key=None):
    input_box.delete(1.0, tk.END)
    # read the json file and print source_sentences, translated_sentences, target_sentences
    with open('sentences.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
        source_sentences = data["source_sentences"]
        translated_sentences = data["translated_sentences"]
        target_sentences = data["target_sentences"]
    
    # Implement logic to delete selected sentence from translation
    flush_sentences_to_csv(source_sentences, translated_sentences, target_sentences[1:])
    pass

def merge_source(key=None):
    input_box.delete(1.0, tk.END)
    # read the json file and print source_sentences, translated_sentences, target_sentences
    with open('sentences.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
        source_sentences = data["source_sentences"]
        translated_sentences = data["translated_sentences"]
        target_sentences = data["target_sentences"]
    
    # Implement logic to merge selected sentence from source into translation
    source_sentences[1] = source_sentences[0] + ' ' + source_sentences[1]
    translated_sentences[1] = translated_sentences[0] + ' ' + translated_sentences[1]
    flush_sentences_to_csv(source_sentences[1:], translated_sentences[1:], target_sentences)
    pass

def merge_translation(key=None):
    input_box.delete(1.0, tk.END)
    # read the json file and print source_sentences, translated_sentences, target_sentences
    with open('sentences.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
        source_sentences = data["source_sentences"]
        translated_sentences = data["translated_sentences"]
        target_sentences = data["target_sentences"]
    
    # Implement logic to merge selected sentence from translation into source
    target_sentences[1] = target_sentences[0] + ' ' + target_sentences[1]
    flush_sentences_to_csv(source_sentences, translated_sentences, target_sentences[1:])
    pass

def remove_from_both(key=None):
    input_box.delete(1.0, tk.END)
    # read the json file and print source_sentences, translated_sentences, target_sentences
    with open('sentences.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
        source_sentences = data["source_sentences"]
        translated_sentences = data["translated_sentences"]
        target_sentences = data["target_sentences"]
    
    # Implement logic to remove selected sentence from both source and translation
    flush_sentences_to_csv(source_sentences[1:], translated_sentences[1:], target_sentences[1:])
    pass

def add_to_translation_pairs(key=None):
    input_box.delete(1.0, tk.END)
    # read the json file and print source_sentences, translated_sentences, target_sentences
    with open('sentences.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
        source_sentences = data["source_sentences"]
        translated_sentences = data["translated_sentences"]
        target_sentences = data["target_sentences"]
    
    # Implement logic to add selected sentence pair to translation pairs
    add_to_tsv(source_sentences[0], target_sentences[0])
    flush_sentences_to_csv(source_sentences[1:], translated_sentences[1:], target_sentences[1:])
    pass

def flush_sentences_to_csv(source_sentences, translated_sentences, target_sentences):
    # dump source_sentences, translated_sentences, target_sentences in a json file
    data = {
        "source_sentences": source_sentences,
        "translated_sentences": translated_sentences,
        "target_sentences": target_sentences
    }

    # add encoding to open file syntax below

    with open('sentences.json', 'w', encoding='utf-8') as f:
        json.dump(data, f,  ensure_ascii=False)

    display_sentences(source_sentences, translated_sentences, target_sentences)

# open translation_pairs.tsv and append to that sen1 and sen2
def add_to_tsv(sen1, sen2):
    # open translation_pairs.tsv and append sen1 and sen2
    with open('translation_pairs.tsv', 'a', encoding='utf-8') as f:
        # Handle edge cases
        sen1 = sen1.replace('\n', ' ').replace('\r', '')  # Remove new line characters
        sen2 = sen2.replace('\n', ' ').replace('\r', '')  # Remove new line characters
        sen1 = sen1.replace('"', '\\"')  # Escape double quotes
        sen2 = sen2.replace('"', '\\"')  # Escape double quotes
        f.write(f'"{sen1}"\t"{sen2}"\n')


def display_sentences(source_sentences, translated_sentences, target_sentences):
    source_text = "\n\n\n".join(source_sentences[:NUM_ITEMS_FOR_DISPLAY])
    translated_text = "\n\n\n".join(translated_sentences[:NUM_ITEMS_FOR_DISPLAY])
    target_text = "\n\n\n".join(target_sentences[:NUM_ITEMS_FOR_DISPLAY])

    similarity_scores = []
    words_intersection_scores = []

    for i in range(min(NUM_ITEMS_FOR_DISPLAY, len(source_sentences), len(translated_sentences), len(target_sentences))):
        similarity_score = hindi_sentence_similarity(translated_sentences[i], target_sentences[i])
        words_intersection_score = words_intersection(translated_sentences[i], target_sentences[i])
        similarity_scores.append(similarity_score)
        words_intersection_scores.append(words_intersection_score)

        if i==0:
            if (similarity_score> SIMILARITY_SCORE_THRESHOLD and words_intersection_score > 0.1 and words_intersection_score < WORDS_INTERSECTION_THRESHOLD):
                print("Merging Possibility")
                print(words_intersection(translated_sentences[i]+translated_sentences[i+1], target_sentences[i]), words_intersection(translated_sentences[i], target_sentences[i]+target_sentences[i+1]))
                if (words_intersection(translated_sentences[i]+translated_sentences[i+1], target_sentences[i]) > WORDS_INTERSECTION_THRESHOLD):
                    notification_text = "Automatically merging source."
                    merge_source()
                    show_notification(notification_text, "dark green")
                    return
                elif (words_intersection(translated_sentences[i], target_sentences[i]+target_sentences[i+1]) > WORDS_INTERSECTION_THRESHOLD):
                    notification_text = "Automatically merging target."
                    merge_translation()
                    show_notification(notification_text, "dark green")
                    return

            if ((similarity_score > SIMILARITY_SCORE_THRESHOLD and words_intersection_score > WORDS_INTERSECTION_THRESHOLD) or (similarity_score>0.55 and words_intersection_score>0.45)):
                add_to_translation_pairs()
                notification_text = "Automatically adding to translation."
                show_notification(notification_text, "dark blue")
                return
            
            if hindi_sentence_similarity(translated_sentences[i+1], target_sentences[i]) > SIMILARITY_SCORE_THRESHOLD and words_intersection(translated_sentences[i+1], target_sentences[i])>WORDS_INTERSECTION_THRESHOLD:
                delete_from_source()
                notification_text = "Found a better match. Automatically deleting from source."
                show_notification(notification_text, "dark red")
                return
            
            if hindi_sentence_similarity(translated_sentences[i], target_sentences[i+1]) > SIMILARITY_SCORE_THRESHOLD and words_intersection(translated_sentences[i], target_sentences[i+1])>WORDS_INTERSECTION_THRESHOLD:
                delete_from_translation()
                notification_text = "Found a better match. Automatically deleting from translation."
                show_notification(notification_text, "dark red")
                return


    similarity_words_scores = [f"{similarity_score:.2%} Similarity, {words_intersection_score:.2%} Words Overlap" for similarity_score, words_intersection_score in zip(similarity_scores, words_intersection_scores)]
    similarity_score_text = "\n\n\n".join(similarity_words_scores)

    source_box.delete(1.0, tk.END)
    source_box.insert(tk.END, source_text)

    translated_box.delete(1.0, tk.END)
    translated_box.insert(tk.END, translated_text)

    target_box.delete(1.0, tk.END)
    target_box.insert(tk.END, target_text)

    similarity_score_box.delete(1.0, tk.END)
    similarity_score_box.insert(tk.END, similarity_score_text )
     
# Create frames for layout
left_frame = tk.Frame(root, width=0.3 * root.winfo_screenwidth())
center_frame = tk.Frame(root, width=0.3 * root.winfo_screenwidth())
right_frame = tk.Frame(root, width=0.3 * root.winfo_screenwidth())
fourth_frame = tk.Frame(root, width=0.3 * root.winfo_screenwidth())
input_frame = tk.Frame(root, width=0.3 * root.winfo_screenwidth())

# Create text boxes
source_box = tk.Text(left_frame, width=30, height=10, wrap=tk.WORD)
translated_box = tk.Text(center_frame, width=30, height=10, wrap=tk.WORD)
target_box = tk.Text(right_frame, width=30, height=10, wrap=tk.WORD)
similarity_score_box = tk.Text(fourth_frame, width=30, height=10, wrap=tk.WORD)

input_box = tk.Text(input_frame, width=30, height=2, wrap=tk.WORD)

# Display initial sentences
# read the json file and print source_sentences, translated_sentences, target_sentences
with open('sentences.json', 'r', encoding="utf-8") as f:
    data = json.load(f)
    display_sentences(data["source_sentences"], data["translated_sentences"], data["target_sentences"])

# Pack frames
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
fourth_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
input_frame.pack()

# Pack text boxes
source_box.pack(fill=tk.BOTH, expand=True)
translated_box.pack(fill=tk.BOTH, expand=True)
target_box.pack(fill=tk.BOTH, expand=True)
similarity_score_box.pack(fill=tk.BOTH, expand=True)
input_box.pack()

# Create labels
tk.Label(left_frame, text="Source Sentences").pack()
tk.Label(center_frame, text="Translated Sentences").pack()
tk.Label(right_frame, text="Target Sentences").pack()
tk.Label(fourth_frame, text="Similarity").pack()


# Input box for adding new sentences
input_box.bind("<Return>", add_to_translation_pairs)  # Bind Enter key press event
input_box.bind("a", delete_from_source)  # Bind 'a' key press event
input_box.bind("s", merge_source)  # Bind 's' key press event
input_box.bind("j", delete_from_translation)  # Bind 'a' key press event
input_box.bind("k", merge_translation)  # Bind 's' key press event
input_box.bind("<space>", remove_from_both)  # Bind space bar key press event
input_box.bind("<Delete>", undo_adding)  # Bind delete key press event

# tk.Button(input_frame, text="Text Input", command=on_submit).pack(pady=10)

# Additional buttons
tk.Button(root, text="Delete from Source (a)", command=delete_from_source).pack(pady=(20, 5))
tk.Button(root, text="Merge Source (s)", command=merge_source).pack(pady=5)

tk.Button(root, text="Delete from Translation (j)", command=delete_from_translation).pack(pady=(20,5))
tk.Button(root, text="Merge Translation (k)", command=merge_translation).pack(pady=5)

ttk.Button(root, text="Add to Pairs (enter)", command=add_to_translation_pairs, style='Accent.TButton').pack(pady=(20,5))

tk.Button(root, text="Remove from both ( )", command=remove_from_both).pack(pady=(20,5))
tk.Button(root, text="Undo Adding (Del)", command=undo_adding).pack(pady=5)

root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "light")

root.mainloop()
