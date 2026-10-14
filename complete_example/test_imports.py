"""
Test imports for the preprocessing pipeline
"""

# Import preprocessing functions directly
import sys
import os

# Add parent directory to path
parent_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, parent_dir)

# Direct imports from each module
sys.path.insert(0, os.path.join(parent_dir, '01_punctuation_removal'))
import implementation as punct_impl
remove_punctuation = punct_impl.remove_punctuation

sys.path.insert(0, os.path.join(parent_dir, '02_text_lowering'))
import implementation as lower_impl
lower_text = lower_impl.lower_text

sys.path.insert(0, os.path.join(parent_dir, '03_tokenization'))
import implementation as token_impl
word_tokenization = token_impl.word_tokenization

sys.path.insert(0, os.path.join(parent_dir, '04_stopword_removal'))
import implementation as stopword_impl
remove_stopwords = stopword_impl.remove_stopwords

sys.path.insert(0, os.path.join(parent_dir, '05_stemming'))
import implementation as stem_impl
apply_stemming_to_tokens = stem_impl.apply_stemming_to_tokens

sys.path.insert(0, os.path.join(parent_dir, '06_lemmatization'))
import implementation as lemm_impl
apply_lemmatization_to_tokens = lemm_impl.apply_lemmatization_to_tokens

def test_pipeline():
    """Test the complete pipeline on a simple example"""
    print("=== Testing Text Preprocessing Pipeline ===")
    
    # Test message
    test_text = "Hello, World! This is a test message with punctuation and STOPWORDS."
    
    print(f"Original: {test_text}")
    
    # Step 1: Punctuation removal
    text_no_punct = remove_punctuation(test_text)
    print(f"No punctuation: {text_no_punct}")
    
    # Step 2: Text lowering
    text_lower = lower_text(text_no_punct)
    print(f"Lower case: {text_lower}")
    
    # Step 3: Tokenization
    tokens = word_tokenization(text_lower)
    print(f"Tokens: {tokens}")
    
    # Step 4: Stopword removal
    tokens_no_sw = remove_stopwords(tokens)
    print(f"No stopwords: {tokens_no_sw}")
    
    # Step 5: Stemming
    stemmed_tokens = apply_stemming_to_tokens(tokens_no_sw, 'porter')
    print(f"Stemmed: {stemmed_tokens}")
    
    # Step 6: Lemmatization
    lemmatized_tokens = apply_lemmatization_to_tokens(tokens_no_sw)
    print(f"Lemmatized: {lemmatized_tokens}")
    
    print("\n=== Pipeline Test Complete ===")

if __name__ == "__main__":
    test_pipeline()
