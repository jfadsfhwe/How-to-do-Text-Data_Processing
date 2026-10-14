"""
Tokenization Example
"""

import pandas as pd
from implementation import word_tokenization, sentence_tokenization, advanced_word_tokenization, handle_contractions

# Sample data
sample_data = [
    "Hello world! How are you today?",
    "This is a test. With multiple sentences! And different punctuation.",
    "I can't believe it's already 2024! Time flies so fast.",
    "Email: user@domain.com, Phone: (123) 456-7890",
    "You're going to love this. I've been there before."
]

# Create DataFrame
df = pd.DataFrame({'original_text': sample_data})

# Apply different tokenization methods
df['word_tokens'] = df['original_text'].apply(word_tokenization)
df['sentence_tokens'] = df['original_text'].apply(sentence_tokenization)
df['advanced_tokens'] = df['original_text'].apply(
    lambda x: advanced_word_tokenization(x, keep_punctuation=['!', '.', ','])
)

print("=== Tokenization Comparison ===")
print(df[['original_text', 'word_tokens']].head())
print()

print("=== Sentence Tokenization ===")
for idx, row in df.head(3).iterrows():
    print(f"Text: {row['original_text']}")
    print(f"Sentences: {row['sentence_tokens']}")
    print("-" * 50)

# Contraction handling example
df['expanded_text'] = df['original_text'].apply(handle_contractions)
df['expanded_tokens'] = df['expanded_text'].apply(word_tokenization)

print("\n=== Contraction Handling Example ===")
contraction_examples = df[df['original_text'].str.contains("can't|you're|I've|they'll", case=False)]
for idx, row in contraction_examples.iterrows():
    print(f"Original:  {row['original_text']}")
    print(f"Expanded:  {row['expanded_text']}")
    print(f"Tokens:    {row['expanded_tokens']}")
    print("-" * 50)

# Token statistics
print("\n=== Token Statistics ===")
all_word_tokens = [token for tokens in df['word_tokens'] for token in tokens]
all_expanded_tokens = [token for tokens in df['expanded_tokens'] for token in tokens]

print(f"Total word tokens: {len(all_word_tokens)}")
print(f"Total expanded tokens: {len(all_expanded_tokens)}")
print(f"Unique word tokens: {len(set(all_word_tokens))}")
print(f"Unique expanded tokens: {len(set(all_expanded_tokens))}")
