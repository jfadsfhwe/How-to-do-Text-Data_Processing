"""
Complete Text Preprocessing Pipeline - Fixed Version
SMS Spam Detection Example
"""

import pandas as pd
import string
import re
import importlib.util
import sys
import os
from collections import Counter

def load_module_from_path(module_name, module_path):
    """Load a module from a specific path"""
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

class TextPreprocessingPipeline:
    """
    Complete text preprocessing pipeline
    """
    
    def __init__(self, use_stemming=True):
        """
        Initialize the pipeline
        
        Args:
            use_stemming (bool): If True, use stemming; if False, use lemmatization
        """
        self.use_stemming = use_stemming
        self.processing_steps = []
        
        # Load modules dynamically to avoid conflicts
        base_dir = os.path.join(os.path.dirname(__file__), '..')
        
        # Load each preprocessing module
        punct_module = load_module_from_path('punct_impl', 
            os.path.join(base_dir, '01_punctuation_removal', 'implementation.py'))
        lower_module = load_module_from_path('lower_impl',
            os.path.join(base_dir, '02_text_lowering', 'implementation.py'))
        token_module = load_module_from_path('token_impl',
            os.path.join(base_dir, '03_tokenization', 'implementation.py'))
        stopword_module = load_module_from_path('stopword_impl',
            os.path.join(base_dir, '04_stopword_removal', 'implementation.py'))
        stem_module = load_module_from_path('stem_impl',
            os.path.join(base_dir, '05_stemming', 'implementation.py'))
        lemm_module = load_module_from_path('lemm_impl',
            os.path.join(base_dir, '06_lemmatization', 'implementation.py'))
        
        # Assign functions
        self.remove_punctuation = punct_module.remove_punctuation
        self.lower_text = lower_module.lower_text
        self.word_tokenization = token_module.word_tokenization
        self.remove_stopwords = stopword_module.remove_stopwords
        self.apply_stemming_to_tokens = stem_module.apply_stemming_to_tokens
        self.apply_lemmatization_to_tokens = lemm_module.apply_lemmatization_to_tokens
    
    def preprocess_text(self, text):
        """
        Apply all preprocessing steps to a single text
        
        Args:
            text (str): Input text
            
        Returns:
            list: Preprocessed tokens
        """
        if not isinstance(text, str):
            return []
        
        # Step 1: Punctuation removal
        text_no_punct = self.remove_punctuation(text)
        
        # Step 2: Text lowering
        text_lower = self.lower_text(text_no_punct)
        
        # Step 3: Tokenization
        tokens = self.word_tokenization(text_lower)
        
        # Step 4: Stopword removal
        tokens_no_sw = self.remove_stopwords(tokens)
        
        # Step 5: Stemming or Lemmatization
        if self.use_stemming:
            final_tokens = self.apply_stemming_to_tokens(tokens_no_sw, 'porter')
        else:
            final_tokens = self.apply_lemmatization_to_tokens(tokens_no_sw)
        
        return final_tokens
    
    def preprocess_dataframe(self, df, text_column):
        """
        Apply preprocessing to a pandas DataFrame
        
        Args:
            df (pd.DataFrame): Input DataFrame
            text_column (str): Name of the text column
            
        Returns:
            pd.DataFrame: DataFrame with preprocessing results
        """
        # Make a copy to avoid modifying original
        result_df = df.copy()
        
        # Apply preprocessing step by step for analysis
        result_df['original_text'] = result_df[text_column]
        result_df['no_punctuation'] = result_df[text_column].apply(self.remove_punctuation)
        result_df['lower_text'] = result_df['no_punctuation'].apply(self.lower_text)
        result_df['tokens'] = result_df['lower_text'].apply(self.word_tokenization)
        result_df['no_stopwords'] = result_df['tokens'].apply(self.remove_stopwords)
        
        if self.use_stemming:
            result_df['final_tokens'] = result_df['no_stopwords'].apply(
                lambda x: self.apply_stemming_to_tokens(x, 'porter')
            )
            result_df['final_text'] = result_df['final_tokens'].apply(' '.join)
        else:
            result_df['final_tokens'] = result_df['no_stopwords'].apply(
                self.apply_lemmatization_to_tokens
            )
            result_df['final_text'] = result_df['final_tokens'].apply(' '.join)
        
        return result_df
    
    def get_vocabulary_stats(self, df):
        """
        Get vocabulary statistics at different preprocessing stages
        
        Args:
            df (pd.DataFrame): Preprocessed DataFrame
            
        Returns:
            dict: Vocabulary statistics
        """
        stats = {}
        
        # Original vocabulary
        original_tokens = []
        for tokens in df['tokens']:
            original_tokens.extend(tokens)
        stats['original_vocab_size'] = len(set(original_tokens))
        
        # After stopword removal
        no_sw_tokens = []
        for tokens in df['no_stopwords']:
            no_sw_tokens.extend(tokens)
        stats['no_sw_vocab_size'] = len(set(no_sw_tokens))
        
        # Final vocabulary
        final_tokens = []
        for tokens in df['final_tokens']:
            final_tokens.extend(tokens)
        stats['final_vocab_size'] = len(set(final_tokens))
        
        # Reduction percentages
        stats['sw_reduction_pct'] = (
            (stats['original_vocab_size'] - stats['no_sw_vocab_size']) / 
            stats['original_vocab_size'] * 100
        )
        
        stats['final_reduction_pct'] = (
            (stats['original_vocab_size'] - stats['final_vocab_size']) / 
            stats['original_vocab_size'] * 100
        )
        
        return stats
    
    def get_most_common_words(self, df, n=20):
        """
        Get most common words after preprocessing
        
        Args:
            df (pd.DataFrame): Preprocessed DataFrame
            n (int): Number of top words to return
            
        Returns:
            list: List of (word, count) tuples
        """
        all_tokens = []
        for tokens in df['final_tokens']:
            all_tokens.extend(tokens)
        
        word_counts = Counter(all_tokens)
        return word_counts.most_common(n)

def create_sample_data():
    """
    Create sample SMS spam data for demonstration
    """
    data = {
        'label': ['ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'ham'],
        'message': [
            "Go until jurong point, crazy.. Available only in bugis n great world la e buffet...",
            "Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005.",
            "Nah I don't think he goes to usf, he lives around here though",
            "WINNER!! As a valued network customer you have been selected to receivea £900 prize reward!",
            "I'm back & we're packing the car now, I'll let you know if there's any room",
            "Had your mobile 11 months or more? U R entitled to Update to the latest colour mobiles with camera for Free!",
            "I've been searching for the right words to thank you for this breather. I promise i wont take your help for granted",
            "I HAVE A DATE ON SUNDAY WITH WILL!!"
        ]
    }
    return pd.DataFrame(data)

def main():
    """
    Main function to run the complete preprocessing pipeline
    """
    print("=== Complete Text Preprocessing Pipeline ===")
    print("SMS Spam Detection Example\n")
    
    # Create sample data
    df = create_sample_data()
    print(f"Dataset shape: {df.shape}")
    print(f"Label distribution:\n{df['label'].value_counts()}\n")
    
    # Initialize pipeline with stemming
    print("Running pipeline with stemming...")
    pipeline_stem = TextPreprocessingPipeline(use_stemming=True)
    df_stem = pipeline_stem.preprocess_dataframe(df, 'message')
    
    # Initialize pipeline with lemmatization
    print("Running pipeline with lemmatization...")
    pipeline_lem = TextPreprocessingPipeline(use_stemming=False)
    df_lem = pipeline_lem.preprocess_dataframe(df, 'message')
    
    # Show preprocessing results for first message
    print("\n=== Preprocessing Results (First Message) ===")
    first_msg = df_stem.iloc[0]
    print(f"Original: {first_msg['original_text']}")
    print(f"No Punct: {first_msg['no_punctuation']}")
    print(f"Lower:    {first_msg['lower_text']}")
    print(f"Tokens:   {first_msg['tokens']}")
    print(f"No SW:    {first_msg['no_stopwords']}")
    print(f"Stemmed:  {first_msg['final_tokens']}")
    print(f"Final:    {first_msg['final_text']}")
    
    # Vocabulary statistics
    print("\n=== Vocabulary Statistics ===")
    stem_stats = pipeline_stem.get_vocabulary_stats(df_stem)
    lem_stats = pipeline_lem.get_vocabulary_stats(df_lem)
    
    print("Stemming Results:")
    print(f"  Original vocab: {stem_stats['original_vocab_size']}")
    print(f"  After stopword removal: {stem_stats['no_sw_vocab_size']}")
    print(f"  Final vocab: {stem_stats['final_vocab_size']}")
    print(f"  Total reduction: {stem_stats['final_reduction_pct']:.1f}%")
    
    print("\nLemmatization Results:")
    print(f"  Original vocab: {lem_stats['original_vocab_size']}")
    print(f"  After stopword removal: {lem_stats['no_sw_vocab_size']}")
    print(f"  Final vocab: {lem_stats['final_vocab_size']}")
    print(f"  Total reduction: {lem_stats['final_reduction_pct']:.1f}%")
    
    # Most common words
    print("\n=== Most Common Words (Stemmed) ===")
    common_words = pipeline_stem.get_most_common_words(df_stem, 10)
    for word, count in common_words:
        print(f"{word}: {count}")
    
    print("\n=== Most Common Words (Lemmatized) ===")
    common_words = pipeline_lem.get_most_common_words(df_lem, 10)
    for word, count in common_words:
        print(f"{word}: {count}")
    
    # Save results
    df_stem.to_csv('preprocessed_stemmed.csv', index=False)
    df_lem.to_csv('preprocessed_lemmatized.csv', index=False)
    print(f"\nResults saved to 'preprocessed_stemmed.csv' and 'preprocessed_lemmatized.csv'")
    
    return df_stem, df_lem

if __name__ == "__main__":
    df_stem, df_lem = main()
