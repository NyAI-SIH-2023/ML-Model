import re
import os
import sys
sys.path.append(os.getcwd())

import data.words_and_terms as wt
import simplifier.simplifier_utils as utils
def complexity(sentence):
    complexity_score = 0

    # Rule: Count legal terms
    legal_terms = wt.legal_terms # Example legal terms
    for term in legal_terms:
        if re.search(r'\b{}\b'.format(term), sentence, re.IGNORECASE):
            complexity_score += 1
    
    difficult_words = wt.difficult_words# Example legal terms
    for term in difficult_words:
        if re.search(r'\b{}\b'.format(term), sentence, re.IGNORECASE):
            complexity_score += 1

    # Rule: Check sentence length
    if len(sentence.split()) > 15:  # Example threshold
        complexity_score += 1

    return complexity_score

# Example usage
path = os.path.join(os.getcwd(),'data/raw data/1.txt')
legal_document = utils.load_as_text(path)

sentence_pattern = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')

# Extract sentences using the pattern
sentences = re.split(sentence_pattern, legal_document)

# Remove empty strings from the list
sentences = [sentence.strip() for sentence in sentences if sentence]

# Print the extracted sentences
for i, sentence in enumerate(sentences, 1):
    print(f'Sentence {i}: {sentence}')

# Annotate difficulty for each sentence
difficulty_scores = [(sentence, complexity(sentence)) for sentence in sentences]

# Rank sentences based on difficulty scores
ranked_sentences = sorted(difficulty_scores, key=lambda x: x[1], reverse=True)

# Print the top N difficult sentences
top_difficult_sentences = []
for sentence , score in ranked_sentences:
    if score > 0:
        top_difficult_sentences.append((sentence, score))

print(len(top_difficult_sentences))
for sentence, score in top_difficult_sentences:
    print(f"Difficulty Score: {score}\n{sentence}")