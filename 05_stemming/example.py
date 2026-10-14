"""
Stemming Example
"""

import pandas as pd
from implementation import apply_stemming_to_tokens, PorterStemmer, simple_stemmer

# Sample data (already tokenized)
sample_data = [
    ["running", "studies", "organization", "computing"],
    ["university", "connection", "relational", "electricity"],
    ["programming", "developer", "development", "programs"],
    ["beautiful", "beauty", "beautifully", "beautify"],
    ["quickly", "quick", "quickness", "quicken"]
]

# Create DataFrame
df = pd.DataFrame({'original_tokens': sample_data})

# Apply different stemming methods
df['porter_stemmed'] = df['original_tokens'].apply(
    lambda x: apply_stemming_to_tokens(x, 'porter')
)
df['simple_stemmed'] = df['original_tokens'].apply(
    lambda x: apply_stemming_to_tokens(x, 'simple')
)

print("=== Stemming Comparison ===")
print(df[['original_tokens', 'porter_stemmed', 'simple_stemmed']])
print()

# Detailed comparison for specific words
comparison_words = [
    "running", "studies", "organization", "computing", "university",
    "connection", "relational", "electricity", "programming", "beautiful"
]

porter = PorterStemmer()

print("=== Detailed Word Comparison ===")
print(f"{'Original':<15} {'Porter':<10} {'Simple':<10}")
print("-" * 40)
for word in comparison_words:
    porter_result = porter.stem(word)
    simple_result = simple_stemmer(word)
    print(f"{word:<15} {porter_result:<10} {simple_result:<10}")

# Vocabulary reduction analysis
print("\n=== Vocabulary Reduction Analysis ===")
all_original = [token for tokens in df['original_tokens'] for token in tokens]
all_porter = [token for tokens in df['porter_stemmed'] for token in tokens]
all_simple = [token for tokens in df['simple_stemmed'] for token in tokens]

print(f"Original unique tokens: {len(set(all_original))}")
print(f"Porter unique tokens: {len(set(all_porter))}")
print(f"Simple unique tokens: {len(set(all_simple))}")
print(f"Porter reduction: {len(set(all_original)) - len(set(all_porter))} tokens")
print(f"Simple reduction: {len(set(all_original)) - len(set(all_simple))} tokens")

# Show examples of over-stemming
print("\n=== Over-stemming Examples ===")
over_stemming_examples = [
    ("university", "univers"),
    ("organization", "organ"),
    ("electricity", "electr")
]

for original, expected in over_stemming_examples:
    porter_result = porter.stem(original)
    print(f"{original:<15} -> {porter_result:<10} (expected: {expected})")

print("\n=== Stemming vs Original Meaning ===")
meaning_examples = [
    (["studies", "studying"], "Both should relate to 'study'"),
    (["organization", "organize"], "Different meanings, similar stems"),
    (["electricity", "electric"], "Related concepts, good stemming")
]

for words, description in meaning_examples:
    stemmed = [porter.stem(word) for word in words]
    print(f"{words} -> {stemmed} ({description})")
