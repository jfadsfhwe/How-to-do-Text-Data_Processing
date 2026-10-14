"""
Stopword Removal Implementation
"""

import pandas as pd

# Default English stopwords list
DEFAULT_STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", 
    "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 
    'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', 
    "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 
    'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 
    'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 
    'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 
    'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 
    'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 
    'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 
    'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 
    'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 
    'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 
    'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 
    'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', 
    "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', 
    "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 
    'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 
    'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
}

def remove_stopwords(tokens, stopwords=None):
    """
    Remove stopwords from a list of tokens.
    
    Args:
        tokens (list): List of word tokens
        stopwords (set): Set of stopwords to remove (uses default if None)
        
    Returns:
        list: List of tokens without stopwords
    """
    if not isinstance(tokens, list):
        return []
    
    if stopwords is None:
        stopwords = DEFAULT_STOPWORDS
    
    # Filter out stopwords
    filtered_tokens = [token for token in tokens if token.lower() not in stopwords]
    return filtered_tokens

def remove_stopwords_with_exceptions(tokens, stopwords=None, exceptions=None):
    """
    Remove stopwords but keep specified exceptions.
    
    Args:
        tokens (list): List of word tokens
        stopwords (set): Set of stopwords to remove
        exceptions (list): List of stopwords to keep
        
    Returns:
        list: List of tokens with selective stopword removal
    """
    if not isinstance(tokens, list):
        return []
    
    if stopwords is None:
        stopwords = DEFAULT_STOPWORDS
    
    if exceptions is None:
        exceptions = []
    
    # Create modified stopwords set (excluding exceptions)
    modified_stopwords = stopwords - set([word.lower() for word in exceptions])
    
    # Filter out stopwords except exceptions
    filtered_tokens = [
        token for token in tokens 
        if token.lower() not in modified_stopwords
    ]
    return filtered_tokens

def create_custom_stopwords(add_words=None, remove_words=None):
    """
    Create a custom stopwords set by adding or removing words from the default set.
    
    Args:
        add_words (list): Words to add to stopwords
        remove_words (list): Words to remove from stopwords
        
    Returns:
        set: Custom stopwords set
    """
    custom_stopwords = DEFAULT_STOPWORDS.copy()
    
    if add_words:
        custom_stopwords.update([word.lower() for word in add_words])
    
    if remove_words:
        custom_stopwords -= set([word.lower() for word in remove_words])
    
    return custom_stopwords

def apply_stopword_removal_to_series(token_series, stopwords=None):
    """
    Apply stopword removal to a pandas Series of token lists.
    
    Args:
        token_series (pd.Series): Series containing token lists
        stopwords (set): Set of stopwords to remove
        
    Returns:
        pd.Series: Series with stopwords removed
    """
    return token_series.apply(lambda x: remove_stopwords(x, stopwords))

# Example usage and testing
if __name__ == "__main__":
    # Test examples
    test_tokens = [
        ["this", "is", "a", "test", "sentence"],
        ["the", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"],
        ["i", "am", "not", "sure", "about", "this", "decision"],
        ["hello", "world", "how", "are", "you", "today"]
    ]
    
    print("=== Basic Stopword Removal Examples ===")
    for tokens in test_tokens:
        filtered = remove_stopwords(tokens)
        print(f"Original: {tokens}")
        print(f"Filtered: {filtered}")
        print("-" * 50)
    
    # Custom stopwords example
    custom_sw = create_custom_stopwords(add_words=["test", "example"], remove_words=["not", "no"])
    print(f"\nCustom stopwords (added 'test', 'example'; removed 'not', 'no'):")
    print(f"Size: {len(custom_sw)} stopwords")
    
    # Exception example (keep 'not' for sentiment analysis)
    print("\n=== Stopword Removal with Exceptions ===")
    sentiment_tokens = ["this", "is", "not", "a", "good", "movie"]
    filtered_with_exceptions = remove_stopwords_with_exceptions(
        sentiment_tokens, exceptions=["not"]
    )
    print(f"Original: {sentiment_tokens}")
    print(f"Filtered (keeping 'not'): {filtered_with_exceptions}")
    print("-" * 50)
    
    # Demonstrate vocabulary reduction
    all_tokens = [token for tokens_list in test_tokens for token in tokens_list]
    filtered_all = remove_stopwords(all_tokens)
    
    print(f"\n=== Vocabulary Reduction ===")
    print(f"Original tokens: {len(all_tokens)}")
    print(f"After stopword removal: {len(filtered_all)}")
    print(f"Reduction: {len(all_tokens) - len(filtered_all)} tokens ({((len(all_tokens) - len(filtered_all)) / len(all_tokens) * 100):.1f}%)")
