#import torch 
#from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import nltk
import re
import math
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')

def rank_sentences(document,sentences):

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Calculate TF-IDF scores for each sentence
    tfidf_matrix = vectorizer.fit_transform(sentences)

    # Sum the TF-IDF scores for each sentence
    sentence_scores = tfidf_matrix.sum(axis=1).A1

    # Rank sentences based on scores
    ranked_sentences = sorted(((score, sentence) for score, sentence in zip(sentence_scores, sentences)), reverse=True)
    
    all_sentences = [sentence for score, sentence in ranked_sentences]
    
    return all_sentences

def calculate_n(num_sentences):
    # Adjust these parameters as needed
    base_n = num_sentences
    decay_factor = 0.5  # Exponential decay factor
    
    # Calculate exponentially decreasing n
    n = base_n * math.exp(-decay_factor * (num_sentences / 132))
    
    # Ensure n is at least 1
    n = max(1, round(n))
    
    return n

def group_sentences_into_paragraphs(sentences):
    # Define the desired number of sentences per paragraph
    min_sentences_per_paragraph = 5
    max_sentences_per_paragraph = 7

    # Initialize variables
    paragraphs = []
    current_paragraph = []

    # Iterate through sentences
    for sentence in sentences:
        # Add sentence to the current paragraph
        current_paragraph.append(sentence)

        # Check if the desired number of sentences per paragraph is reached
        if min_sentences_per_paragraph <= len(current_paragraph) <= max_sentences_per_paragraph:
            # Append the current paragraph to the list of paragraphs
            paragraphs.append(" ".join(current_paragraph))
            # Reset the current paragraph
            current_paragraph = []

    # If there are remaining sentences in the last paragraph, add them
    if current_paragraph:
        paragraphs.append(" ".join(current_paragraph))

    return paragraphs

def get_sentences(document):
    sentence_pattern = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')

    # Extract sentences using the pattern
    sentences = re.split(sentence_pattern, document)

    # Remove empty strings from the list
    sentences = [sentence.strip() for sentence in sentences if sentence]
    return sentences

    