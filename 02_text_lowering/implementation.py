"""
Text Lowering Implementation
"""

import pandas as pd

def lower_text(text):
    """
    Convert text to lowercase.
    
    Args:
        text (str): Input text to convert
        
    Returns:
        str: Lowercase text
    """
    if not isinstance(text, str):
        return text
    
    return text.lower()

def conditional_lowering(text, exceptions=None):
    """
    Convert text to lowercase with exceptions.
    
    Args:
        text (str): Input text to convert
        exceptions (list): List of words/phrases to keep in original case
        
    Returns:
        str: Text with conditional lowercase conversion
    """
    if not isinstance(text, str):
        return text
    
    if exceptions is None:
        return text.lower()
    
    words = text.split()
    result_words = []
    
    for word in words:
        # Check if word matches any exception
        is_exception = False
        for exception in exceptions:
            if word.lower() == exception.lower():
                is_exception = True
                break
        
        if is_exception:
            result_words.append(word)
        else:
            result_words.append(word.lower())
    
    return ' '.join(result_words)

def apply_lowering_to_series(text_series, exceptions=None):
    """
    Apply text lowering to a pandas Series.
    
    Args:
        text_series (pd.Series): Series containing text data
        exceptions (list): List of words to keep in original case
        
    Returns:
        pd.Series: Series with lowercase text
    """
    if exceptions is None:
        return text_series.apply(lower_text)
    else:
        return text_series.apply(lambda x: conditional_lowering(x, exceptions))

# Example usage and testing
if __name__ == "__main__":
    # Test examples
    test_texts = [
        "Hello WORLD! How ARE You?",
        "APPLE and apple are the same when lowered",
        "NASA is an acronym that should remain",
        "I LOVE Python Programming!",
        "Mixed CASE Text With Different WORDS"
    ]
    
    print("=== Simple Lowering Examples ===")
    for text in test_texts:
        lowered = lower_text(text)
        print(f"Original: {text}")
        print(f"Lowered:  {lowered}")
        print("-" * 50)
    
    # Conditional lowering example
    exceptions = ['NASA', 'Python']
    print("\n=== Conditional Lowering (keeping NASA and Python) ===")
    for text in test_texts:
        conditional_lowered = conditional_lowering(text, exceptions)
        print(f"Original: {text}")
        print(f"Conditional: {conditional_lowered}")
        print("-" * 50)
