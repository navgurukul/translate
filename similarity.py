from sentence_transformers import SentenceTransformer, util
import string
import math

# Load the pre-trained HindSBERT model
model_name = "l3cube-pune/hindi-bert-v2"
model = SentenceTransformer(model_name)

def hindi_sentence_similarity(sentence1, sentence2):
  """
  This function calculates the cosine similarity between two Hindi sentences using HindSBERT.

  Args:
      sentence1: The first Hindi sentence (string).
      sentence2: The second Hindi sentence (string).

  Returns:
      A float between 0 (no similarity) and 1 (identical sentences).
  """
  # Encode the sentences into vectors
  sentence_embeddings = model.encode([sentence1, sentence2])

  # Calculate cosine similarity between the encoded vectors
  cosine_similarity = util.pytorch_cos_sim(sentence_embeddings[0], sentence_embeddings[1]).item()

  return (cosine_similarity-0.95)*20

def length_penalty_score(sentence1, sentence2):
    length_ratio = abs(len(sentence1) - len(sentence2)) / max(len(sentence1), len(sentence2))
    length_penalty_score = 1 - length_ratio
    return length_penalty_score

def char_ngram_similarity(sentence1, sentence2, n=4):
    """
    This function calculates the similarity between two sentences based on the overlap of character n-grams.

    Args:
        sentence1: The first sentence (string).
        sentence2: The second sentence (string).
        n: The size of the n-grams to consider (integer, default=3).

    Returns:
        A float between 0 (no similarity) and 1 (identical sentences).
    """
    # Lowercase and remove spaces for case-insensitivity and handling punctuation
    sentence1 = sentence1.lower().replace(" ", "")
    sentence2 = sentence2.lower().replace(" ", "")

    # Create sets of n-grams for each sentence
    sentence1_ngrams = set(sentence1[i:i+n] for i in range(len(sentence1) - n + 1))
    sentence2_ngrams = set(sentence2[i:i+n] for i in range(len(sentence2) - n + 1))

    # Calculate the intersection and union of n-grams
    intersection = len(sentence1_ngrams.intersection(sentence2_ngrams))
    union = len(sentence1_ngrams.union(sentence2_ngrams))

    # Avoid division by zero
    if union == 0:
        return 0

    # Jaccard similarity coefficient for n-gram overlap
    return float(intersection / union)

def words_intersection(sentence1, sentence2):
    words1 = sentence1.translate(str.maketrans("", "", string.punctuation)).lower().split(" ")
    words2 = sentence2.translate(str.maketrans("", "", string.punctuation)).lower().split(" ")

    prepositions = [
    "के", "से", "का", "को", "में", "पर", "तक", "ही", "है",
    "की", "का", "को", "तक", "तभी", "वही"]

    words1 = [word for word in words1 if word not in prepositions]
    words2 = [word for word in words2 if word not in prepositions]

    words1 = [word for word in words1 if not word.isdigit()]
    words2 = [word for word in words2 if not word.isdigit()]

    return float(len(set(words1).intersection(set(words2)))/max(len(words1), len(words2)))*max(1, (1 + math.log(max(len(words1), len(words2)) / 3)) / 2)