"""
Tokenization Implementation
"""

import re
import pandas as pd

def word_tokenization(text):
    """
    Split text into words using regular expressions.
    
    Args:
        text (str): Input text to tokenize
        
    Returns:
        list: List of word tokens
    """
    if not isinstance(text, str):
        return []
    
    # Split on non-word characters
    tokens = re.split(r'\W+', text)
    # Remove empty strings
    tokens = [token for token in tokens if token]
    return tokens

def sentence_tokenization(text):
    """
    Split text into sentences using regular expressions.
    
    Args:
        text (str): Input text to tokenize
        
    Returns:
        list: List of sentence tokens
    """
    if not isinstance(text, str):
        return []
    
    # Split on sentence endings (., !, ?)
    sentences = re.split(r'[.!?]+', text)
    # Remove empty strings and strip whitespace
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences

def advanced_word_tokenization(text, keep_punctuation=None):
    """
    Advanced word tokenization with options to keep specific punctuation.
    
    Args:
        text (str): Input text to tokenize
        keep_punctuation (list): List of punctuation to keep as separate tokens
        
    Returns:
        list: List of word tokens with optional punctuation
    """
    if not isinstance(text, str):
        return []
    
    if keep_punctuation is None:
        # Simple tokenization
        tokens = re.split(r'\W+', text)
    else:
        # Create pattern that keeps specified punctuation
        pattern = r'(\w+|[' + re.escape(''.join(keep_punctuation)) + '])'
        tokens = re.findall(pattern, text)
    
    # Remove empty strings
    tokens = [token for token in tokens if token]
    return tokens

def handle_contractions(text):
    """
    Handle common English contractions before tokenization.
    
    Args:
        text (str): Input text
        
    Returns:
        str: Text with expanded contractions
    """
    if not isinstance(text, str):
        return text
    
    # Common contraction patterns
    contractions = {
        "won't": "will not",
        "can't": "cannot",
        "n't": " not",
        "'re": " are",
        "'ve": " have",
        "'ll": " will",
        "'d": " would",
        "'m": " am"
    }
    
    for contraction, expansion in contractions.items():
        text = re.sub(contraction, expansion, text)
    
    return text

def apply_tokenization_to_series(text_series, tokenization_type='word'):
    """
    Apply tokenization to a pandas Series.
    
    Args:
        text_series (pd.Series): Series containing text data
        tokenization_type (str): 'word', 'sentence', or 'advanced'
        
    Returns:
        pd.Series: Series with tokenized text
    """
    if tokenization_type == 'word':
        return text_series.apply(word_tokenization)
    elif tokenization_type == 'sentence':
        return text_series.apply(sentence_tokenization)
    elif tokenization_type == 'advanced':
        return text_series.apply(advanced_word_tokenization)
    else:
        raise ValueError("tokenization_type must be 'word', 'sentence', or 'advanced'")

# Example usage and testing
if __name__ == "__main__":
    # Test examples
    test_texts = [
        "Hello world! How are you today?",
        "This is a test. With multiple sentences! And different punctuation.",
        "I can't believe it's already 2024! Time flies so fast.",
        "Email: user@domain.com, Phone: (123) 456-7890"
    ]
    
    print("=== Word Tokenization Examples ===")
    for text in test_texts:
        tokens = word_tokenization(text)
        print(f"Original: {text}")
        print(f"Tokens:   {tokens}")
        print("-" * 60)
    
    print("\n=== Sentence Tokenization Examples ===")
    for text in test_texts:
        sentences = sentence_tokenization(text)
        print(f"Original:   {text}")
        print(f"Sentences:  {sentences}")
        print("-" * 60)
    
    print("\n=== Advanced Tokenization (keeping punctuation) ===")
    for text in test_texts:
        tokens = advanced_word_tokenization(text, keep_punctuation=['!', '.', ','])
        print(f"Original: {text}")
        print(f"Tokens:   {tokens}")
        print("-" * 60)
    
    print("\n=== Contraction Handling Examples ===")
    contraction_texts = [
        "I can't believe it's already 2024!",
        "You're going to love this. I've been there before.",
        "They'll be here soon. We'd better prepare."
    ]
    
    for text in contraction_texts:
        expanded = handle_contractions(text)
        tokens = word_tokenization(expanded)
        print(f"Original:  {text}")
        print(f"Expanded:  {expanded}")
        print(f"Tokens:    {tokens}")
        print("-" * 60)
