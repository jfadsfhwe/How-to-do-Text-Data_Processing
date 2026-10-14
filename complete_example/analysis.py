"""
Analysis and Visualization of Text Preprocessing Results
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import numpy as np

def analyze_preprocessing_results(file_path):
    """
    Analyze preprocessing results and create visualizations
    
    Args:
        file_path (str): Path to preprocessed CSV file
    """
    # Load data
    df = pd.read_csv(file_path)
    
    print("=== Text Preprocessing Analysis ===")
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Basic statistics
    print("\n=== Basic Statistics ===")
    print(f"Average original message length: {df['original_text'].str.len().mean():.1f} characters")
    print(f"Average final message length: {df['final_text'].str.len().mean():.1f} characters")
    print(f"Average number of tokens (original): {df['tokens'].str.len().mean():.1f}")
    print(f"Average number of tokens (final): {df['final_tokens'].str.len().mean():.1f}")
    
    # Vocabulary analysis
    print("\n=== Vocabulary Analysis ===")
    all_original_tokens = []
    all_final_tokens = []
    
    for tokens in df['tokens']:
        if isinstance(tokens, str):
            # Handle string representation of list
            tokens = eval(tokens)
        all_original_tokens.extend(tokens)
    
    for tokens in df['final_tokens']:
        if isinstance(tokens, str):
            tokens = eval(tokens)
        all_final_tokens.extend(tokens)
    
    original_vocab_size = len(set(all_original_tokens))
    final_vocab_size = len(set(all_final_tokens))
    
    print(f"Original vocabulary size: {original_vocab_size}")
    print(f"Final vocabulary size: {final_vocab_size}")
    print(f"Vocabulary reduction: {original_vocab_size - final_vocab_size} tokens ({((original_vocab_size - final_vocab_size) / original_vocab_size * 100):.1f}%)")
    
    # Most common words
    print("\n=== Top 20 Most Common Words ===")
    word_counts = Counter(all_final_tokens)
    for i, (word, count) in enumerate(word_counts.most_common(20), 1):
        print(f"{i:2d}. {word:<15} {count}")
    
    # Create visualizations
    create_visualizations(df, all_original_tokens, all_final_tokens, word_counts)

def create_visualizations(df, original_tokens, final_tokens, word_counts):
    """
    Create visualization plots
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Text Preprocessing Analysis', fontsize=16, fontweight='bold')
    
    # 1. Message length distribution
    ax1 = axes[0, 0]
    original_lengths = df['original_text'].str.len()
    final_lengths = df['final_text'].str.len()
    
    ax1.hist(original_lengths, alpha=0.7, label='Original', bins=20, color='skyblue')
    ax1.hist(final_lengths, alpha=0.7, label='Processed', bins=20, color='lightcoral')
    ax1.set_xlabel('Message Length (characters)')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Message Length Distribution')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Token count distribution
    ax2 = axes[0, 1]
    original_token_counts = df['tokens'].str.len()
    final_token_counts = df['final_tokens'].str.len()
    
    ax2.hist(original_token_counts, alpha=0.7, label='Original', bins=15, color='skyblue')
    ax2.hist(final_token_counts, alpha=0.7, label='Processed', bins=15, color='lightcoral')
    ax2.set_xlabel('Number of Tokens')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Token Count Distribution')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Top 15 most common words
    ax3 = axes[1, 0]
    top_words = dict(word_counts.most_common(15))
    words = list(top_words.keys())
    counts = list(top_words.values())
    
    bars = ax3.barh(words, counts, color='lightgreen', edgecolor='darkgreen')
    ax3.set_xlabel('Frequency')
    ax3.set_title('Top 15 Most Common Words')
    ax3.grid(True, alpha=0.3, axis='x')
    
    # Add value labels on bars
    for i, (bar, count) in enumerate(zip(bars, counts)):
        ax3.text(count + 0.1, bar.get_y() + bar.get_height()/2, 
                str(count), va='center', fontsize=9)
    
    # 4. Vocabulary reduction pie chart
    ax4 = axes[1, 1]
    original_vocab_size = len(set(original_tokens))
    final_vocab_size = len(set(final_tokens))
    reduction = original_vocab_size - final_vocab_size
    
    sizes = [final_vocab_size, reduction]
    labels = ['Remaining Vocabulary', 'Removed Words']
    colors = ['lightblue', 'lightcoral']
    
    wedges, texts, autotexts = ax4.pie(sizes, labels=labels, colors=colors, 
                                      autopct='%1.1f%%', startangle=90)
    ax4.set_title('Vocabulary Reduction')
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('preprocessing_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\nVisualization saved as 'preprocessing_analysis.png'")

def compare_stemming_vs_lemmatization(stem_file, lem_file):
    """
    Compare results between stemming and lemmatization
    """
    print("\n=== Stemming vs Lemmatization Comparison ===")
    
    df_stem = pd.read_csv(stem_file)
    df_lem = pd.read_csv(lem_file)
    
    # Get final tokens from both
    stem_tokens = []
    lem_tokens = []
    
    for tokens in df_stem['final_tokens']:
        if isinstance(tokens, str):
            tokens = eval(tokens)
        stem_tokens.extend(tokens)
    
    for tokens in df_lem['final_tokens']:
        if isinstance(tokens, str):
            tokens = eval(tokens)
        lem_tokens.extend(tokens)
    
    stem_vocab = set(stem_tokens)
    lem_vocab = set(lem_tokens)
    
    print(f"Stemming vocabulary size: {len(stem_vocab)}")
    print(f"Lemmatization vocabulary size: {len(lem_vocab)}")
    print(f"Common words: {len(stem_vocab & lem_vocab)}")
    print(f"Unique to stemming: {len(stem_vocab - lem_vocab)}")
    print(f"Unique to lemmatization: {len(lem_vocab - stem_vocab)}")
    
    # Show examples of differences
    print("\n=== Examples of Differences ===")
    stem_only = list(stem_vocab - lem_vocab)[:10]
    lem_only = list(lem_vocab - stem_vocab)[:10]
    
    print(f"Words only in stemming: {stem_only}")
    print(f"Words only in lemmatization: {lem_only}")

def main():
    """
    Main analysis function
    """
    try:
        # Analyze stemming results
        print("Analyzing stemming results...")
        analyze_preprocessing_results('preprocessed_stemmed.csv')
        
        # Analyze lemmatization results
        print("\n" + "="*60)
        print("Analyzing lemmatization results...")
        analyze_preprocessing_results('preprocessed_lemmatized.csv')
        
        # Compare both methods
        compare_stemming_vs_lemmatization('preprocessed_stemmed.csv', 'preprocessed_lemmatized.csv')
        
    except FileNotFoundError:
        print("Preprocessed files not found. Please run complete_pipeline.py first.")
    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    main()
