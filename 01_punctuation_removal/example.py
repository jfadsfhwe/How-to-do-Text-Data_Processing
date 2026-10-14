"""
Punctuation Removal Example
"""

import pandas as pd
from implementation import remove_punctuation, remove_punctuation_advanced

# Sample data
sample_data = [
    "Hello, World! How are you today?",
    "This is a test... with multiple punctuation!!!",
    "Email: user@domain.com, Phone: (123) 456-7890",
    "No punctuation here",
    "Check out: https://example.com/page?param=value&other=123"
]

# Create DataFrame
df = pd.DataFrame({'original_text': sample_data})

# Apply punctuation removal
df['clean_text'] = df['original_text'].apply(remove_punctuation)

print("=== Punctuation Removal Example ===")
print(df)
print()

# Advanced example - keep specific characters for URLs/emails
df['clean_text_keep_special'] = df['original_text'].apply(
    lambda x: remove_punctuation_advanced(x, keep_chars=['@', '.', ':', '/', '?', '=', '&'])
)

print("=== Advanced Example (keeping URL/email characters) ===")
print(df[['original_text', 'clean_text_keep_special']])
