"""
Stopword Removal Example
"""

import pandas as pd
from implementation import remove_stopwords, remove_stopwords_with_exceptions, create_custom_stopwords

# Sample data (already tokenized)
sample_data = [
    ["this", "is", "a", "test", "sentence"],
    ["the", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"],
    ["i", "am", "not", "sure", "about", "this", "decision"],
    ["hello", "world", "how", "are", "you", "today"],
    ["this", "movie", "is", "not", "very", "good", "but", "entertaining"]
]

# Create DataFrame
df = pd.DataFrame({'original_tokens': sample_data})

# Apply basic stopword removal
df['filtered_tokens'] = df['original_tokens'].apply(remove_stopwords)

print("=== Basic Stopword Removal ===")
print(df[['original_tokens', 'filtered_tokens']])
print()

# Sentiment analysis example (keep negation words)
df['sentiment_tokens'] = df['original_tokens'].apply(
    lambda x: remove_stopwords_with_exceptions(x, exceptions=["not", "no", "never"])
)

print("=== Sentiment-Aware Stopword Removal ===")
sentiment_examples = df[df['original_tokens'].apply(lambda x: any(word in ['not', 'no'] for word in x))]
for idx, row in sentiment_examples.iterrows():
    print(f"Original:   {row['original_tokens']}")
    print(f"Basic:      {row['filtered_tokens']}")
    print(f"Sentiment:  {row['sentiment_tokens']}")
    print("-" * 50)

# Custom stopwords example
custom_stopwords = create_custom_stopwords(
    add_words=["movie", "film"],  # Add domain-specific stopwords
    remove_words=["not", "no"]     # Keep negation words
)

df['custom_filtered'] = df['original_tokens'].apply(
    lambda x: remove_stopwords(x, custom_stopwords)
)

print("\n=== Custom Stopwords (added 'movie', 'film'; removed 'not', 'no') ===")
print(df[['original_tokens', 'custom_filtered']])

# Statistics
print("\n=== Stopword Removal Statistics ===")
all_original = [token for tokens in df['original_tokens'] for token in tokens]
all_filtered = [token for tokens in df['filtered_tokens'] for token in tokens]

print(f"Total original tokens: {len(all_original)}")
print(f"Total filtered tokens: {len(all_filtered)}")
print(f"Tokens removed: {len(all_original) - len(all_filtered)}")
print(f"Reduction percentage: {((len(all_original) - len(all_filtered)) / len(all_original) * 100):.1f}%")

print(f"\nUnique original tokens: {len(set(all_original))}")
print(f"Unique filtered tokens: {len(set(all_filtered))}")
print(f"Unique tokens removed: {len(set(all_original)) - len(set(all_filtered))}")
