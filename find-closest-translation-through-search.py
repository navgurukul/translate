import json
from similarity import words_intersection, hindi_sentence_similarity, length_penalty_score
import csv

def get_balanced_subarray(target_sentences, i):
    """
    This function finds a sub-array within target_sentences centered around the index i.

    Args:
        target_sentences: A list of strings representing sentences.
        i: The index around which to find the sub-array (integer).

    Returns:
        A sub-array of target_sentences with maximum size constraints, 
        or None if the conditions are not met.
    """
    # Minimum and maximum valid sub-array sizes based on 10% of target_sentences and 25
    min_size = max(int(0.05 * len(target_sentences)), 25)
    max_size = min(min_size, len(target_sentences))  # Don't exceed sentence length

    # Ensure balanced selection around i (half left, half right)
    left_size = min(i, (max_size - 1) // 2)
    right_size = min(len(target_sentences) - 1 - i, (max_size - 1) // 2)

    # Get the sub-array considering in-bound indices
    start_index = max(0, i - left_size)
    end_index = min(len(target_sentences), i + right_size + 1)

    return target_sentences[start_index:end_index]

def alignment_score(i, pos, len_source_sentences, len_target_sentences):
  """
  Calculates the alignment score for a given point (i, pos) on a line.

  Args:
      i: The index of the source sentence.
      pos: The index of the target sentence.
      len_source_sentences: The length of the source sentences.
      len_target_sentences: The length of the target sentences.

  Returns:
      The alignment score, which is the absolute distance from the point to the line.
  """

  # Calculate the slope and y-intercept of the line.
  slope = (len_target_sentences - 0) / (len_source_sentences - 0)
  y_intercept = 0

  # Calculate the expected position on the line for the given source sentence index.
  expected_pos = slope * i + y_intercept

  # Calculate the absolute distance from the point to the line.
  distance = abs(pos - expected_pos)

  return distance

# # Example usage
# source_sentences = 5
# target_sentences = 3
# i = 2
# pos = 1

# score = alignment_score(i, pos, source_sentences, target_sentences)
# print(score)  # Output: 0.6

# read the json file and print source_sentences, translated_sentences, target_sentences
with open('sentences.json', 'r', encoding="utf-8") as f:
    data = json.load(f)
    source_sentences = data["source_sentences"]
    translated_sentences = data["translated_sentences"]
    target_sentences = data["target_sentences"]

# Open the CSV file in write mode
with open('translation_pairs.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    for i, source_sentence in enumerate(source_sentences):
        closest_target_score = -1
        closest_target_sentence = None
        translated_sentence = translated_sentences[i]

        ntarray = get_balanced_subarray(target_sentences, i)

        for hi_sentence in ntarray:
            score = hindi_sentence_similarity(translated_sentence, hi_sentence)
            if score > closest_target_score:
                closest_target_score = score
                closest_target_sentence = hi_sentence
                lps = length_penalty_score(translated_sentence, hi_sentence)
                # find index of hi_sentence in target_sentences
                pos = target_sentences.index(hi_sentence)
                alignment_s = alignment_score(i, pos, len(source_sentences), len(target_sentences))

        # Write the data to the CSV file
        print(source_sentence)
        writer.writerow([source_sentence, translated_sentence, closest_target_sentence, closest_target_score, lps, words_intersection(translated_sentence, closest_target_sentence), alignment_s])

        # keep flushing the values in the file so that the output can be seen in real time
        csvfile.flush()