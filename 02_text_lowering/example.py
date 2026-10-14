"""
Text Lowering Example
"""

import pandas as pd
from implementation import lower_text, conditional_lowering

# Sample data
sample_data = [
    "Hello WORLD! How ARE You?",
    "APPLE and apple are the same when lowered",
    "NASA is an acronym that should remain",
    "I LOVE Python Programming!",
    "Mixed CASE Text With Different WORDS",
    "The USA and UK are countries"
]

# Create DataFrame
df = pd.DataFrame({'original_text': sample_data})

# Apply simple lowering
df['lower_text'] = df['original_text'].apply(lower_text)

print("=== Simple Text Lowering Example ===")
print(df[['original_text', 'lower_text']])
print()

# Conditional lowering - keep acronyms and proper nouns
exceptions = ['NASA', 'Python', 'USA', 'UK']
df['conditional_lower'] = df['original_text'].apply(
    lambda x: conditional_lowering(x, exceptions)
)

print("=== Conditional Lowering (keeping acronyms and proper nouns) ===")
print(df[['original_text', 'conditional_lower']])

# Demonstrate vocabulary reduction
print("\n=== Vocabulary Reduction Demonstration ===")
unique_original = set(' '.join(df['original_text']).lower().split())
unique_lowered = set(' '.join(df['lower_text']).split())

print(f"Unique words (original, case-sensitive): {len(unique_original)}")
print(f"Unique words (lowercased): {len(unique_lowered)}")
print(f"Reduction: {len(unique_original) - len(unique_lowered)} words")
