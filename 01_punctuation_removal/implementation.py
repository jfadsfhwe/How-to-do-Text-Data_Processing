"""
Punctuation Removal Implementation
"""

import string
import pandas as pd

def remove_punctuation(text):
    """
    Remove all punctuation from the input text.
    
    Args:
        text (str): Input text to clean
        
    Returns:
        str: Text without punctuation
    """
    if not isinstance(text, str):
        return text
    
    # Join characters that are not in string.punctuation
    punctuation_free = "".join([char for char in text if char not in string.punctuation])
    return punctuation_free

def remove_punctuation_advanced(text, keep_chars=None):
    """
    Remove punctuation with option to keep specific characters.
    
    Args:
        text (str): Input text to clean
        keep_chars (list): List of punctuation characters to keep
        
    Returns:
        str: Text with selective punctuation removal
    """
    if not isinstance(text, str):
        return text
    
    if keep_chars is None:
        keep_chars = []
    
    # Create custom punctuation set (excluding characters to keep)
    custom_punctuation = ''.join([char for char in string.punctuation if char not in keep_chars])
    
    punctuation_free = "".join([char for char in text if char not in custom_punctuation])
    return punctuation_free

def apply_punctuation_removal_to_series(text_series):
    """
    Apply punctuation removal to a pandas Series.
    
    Args:
        text_series (pd.Series): Series containing text data
        
    Returns:
        pd.Series: Series with punctuation removed
    """
    return text_series.apply(lambda x: remove_punctuation(x))

# Example usage and testing
if __name__ == "__main__":
    # Test examples
    test_texts = [
        "Hello, World! How are you today?",
        "This is a test... with multiple punctuation!!!",
        "Email: user@domain.com, Phone: (123) 456-7890",
        "No punctuation here"
    ]
    
    print("=== Punctuation Removal Examples ===")
    for text in test_texts:
        cleaned = remove_punctuation(text)
        print(f"Original: {text}")
        print(f"Cleaned:  {cleaned}")
        print("-" * 50)
    
    # Advanced example (keep @ and . for emails)
    email_text = "Contact us at support@company.com or visit www.example.com!"
    cleaned_email = remove_punctuation_advanced(email_text, keep_chars=['@', '.'])
    print(f"\nAdvanced Example (keeping @ and .):")
    print(f"Original: {email_text}")
    print(f"Cleaned:  {cleaned_email}")
