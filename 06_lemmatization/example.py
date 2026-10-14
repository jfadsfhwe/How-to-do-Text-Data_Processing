"""
Lemmatization Example
"""

import pandas as pd
from implementation import apply_lemmatization_to_tokens, SimpleLemmatizer
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '05_stemming'))
from implementation import apply_stemming_to_tokens

# Sample data (already tokenized)
sample_data = [
    ["studies", "computers", "running", "better"],
    ["geese", "analyses", "phenomena", "women"],
    ["programs", "programming", "programmed", "programmer"],
    ["beautiful", "beauty", "beautifully", "beautify"],
    ["corpora", "data", "criteria", "theses"]
]

# Create DataFrame
df = pd.DataFrame({'original_tokens': sample_data})

# Apply lemmatization
df['lemmatized_tokens'] = df['original_tokens'].apply(apply_lemmatization_to_tokens)

# Apply stemming for comparison
df['stemmed_tokens'] = df['original_tokens'].apply(
    lambda x: apply_stemming_to_tokens(x, 'porter')
)

print("=== Lemmatization vs Stemming Comparison ===")
print(df[['original_tokens', 'lemmatized_tokens', 'stemmed_tokens']])
print()

# Detailed comparison for specific words
comparison_words = [
    "studies", "geese", "better", "running", "computers",
    "analyses", "phenomena", "corpora", "programs", "beautiful"
]

lemmatizer = SimpleLemmatizer()
from implementation import PorterStemmer
stemmer = PorterStemmer()

print("=== Detailed Word Comparison ===")
print(f"{'Original':<15} {'Lemmatized':<12} {'Stemmed':<12}")
print("-" * 45)
for word in comparison_words:
    lemma = lemmatizer.lemmatize(word)
    stem = stemmer.stem(word)
    print(f"{word:<15} {lemma:<12} {stem:<12}")

# Meaning preservation analysis
print("\n=== Meaning Preservation Analysis ===")
meaning_examples = [
    (["studies", "studying", "studied"], "All should map to 'study'"),
    (["geese", "goose"], "Should map to 'goose'"),
    (["better", "best"], "Should map to 'good'"),
    (["computers", "computing"], "Should map to 'computer' and 'compute'"),
    (["corpora", "data"], "Should map to 'corpus' and 'datum'")
]

for words, description in meaning_examples:
    lemmatized = [lemmatizer.lemmatize(word) for word in words]
    stemmed = [stemmer.stem(word) for word in words]
    print(f"{words}")
    print(f"  Lemmatized: {lemmatized} - {description}")
    print(f"  Stemmed:    {stemmed}")
    print()

# Vocabulary reduction comparison
print("=== Vocabulary Reduction Comparison ===")
all_original = [token for tokens in df['original_tokens'] for token in tokens]
all_lemmatized = [token for tokens in df['lemmatized_tokens'] for token in tokens]
all_stemmed = [token for tokens in df['stemmed_tokens'] for token in tokens]

print(f"Original unique tokens: {len(set(all_original))}")
print(f"Lemmatized unique tokens: {len(set(all_lemmatized))}")
print(f"Stemmed unique tokens: {len(set(all_stemmed))}")
print(f"Lemmatization reduction: {len(set(all_original)) - len(set(all_lemmatized))} tokens")
print(f"Stemming reduction: {len(set(all_original)) - len(set(all_stemmed))} tokens")

# Real-world examples
print("\n=== Real-world Application Examples ===")
real_world_examples = [
    "The studies show that computers are running better than expected",
    "Geese were observed during the analyses of the phenomena",
    "Programmers are programming programs that program computers"
]

lemmatizer = SimpleLemmatizer()

for sentence in real_world_examples:
    words = sentence.lower().split()
    lemmatized = [lemmatizer.lemmatize(word) for word in words]
    print(f"Original:  {sentence}")
    print(f"Lemmatized: {' '.join(lemmatized)}")
    print("-" * 60)
