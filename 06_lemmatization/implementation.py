"""
Lemmatization Implementation
"""

import re
import pandas as pd

class SimpleLemmatizer:
    """
    Simple lemmatizer using basic rules and a small dictionary
    """
    
    def __init__(self):
        # Basic lemmatization dictionary
        self.lemma_dict = {
            # Irregular verbs
            'am': 'be', 'is': 'be', 'are': 'be', 'was': 'be', 'were': 'be',
            'being': 'be', 'been': 'be',
            'have': 'have', 'has': 'have', 'had': 'have', 'having': 'have',
            'do': 'do', 'does': 'do', 'did': 'do', 'doing': 'do', 'done': 'do',
            'go': 'go', 'goes': 'go', 'went': 'go', 'gone': 'go', 'going': 'go',
            'get': 'get', 'gets': 'get', 'got': 'get', 'gotten': 'get', 'getting': 'get',
            'make': 'make', 'makes': 'make', 'made': 'make', 'making': 'make',
            'see': 'see', 'sees': 'see', 'saw': 'see', 'seen': 'see', 'seeing': 'see',
            'come': 'come', 'comes': 'come', 'came': 'come', 'coming': 'come',
            'take': 'take', 'takes': 'take', 'took': 'take', 'taken': 'take', 'taking': 'take',
            
            # Common nouns
            'men': 'man', 'women': 'woman', 'people': 'person', 'persons': 'person',
            'children': 'child', 'teeth': 'tooth', 'feet': 'foot', 'mice': 'mouse',
            'geese': 'goose', 'lives': 'life', 'leaves': 'leaf', 'wolves': 'wolf',
            'knives': 'knife', 'wives': 'wife', 'selves': 'self', 'elves': 'elf',
            'loaves': 'loaf', 'potatoes': 'potato', 'tomatoes': 'tomato',
            
            # Academic terms
            'studies': 'study', 'studying': 'study', 'studied': 'study',
            'analyses': 'analysis', 'analyzing': 'analyze', 'analyzed': 'analyze',
            'theses': 'thesis', 'hypotheses': 'hypothesis',
            'criteria': 'criterion', 'phenomena': 'phenomenon',
            'data': 'datum', 'bacteria': 'bacterium', 'media': 'medium',
            
            # Common adjectives
            'better': 'good', 'best': 'good', 'worse': 'bad', 'worst': 'bad',
            'more': 'much', 'most': 'much', 'less': 'little', 'least': 'little',
            
            # Technology terms
            'computers': 'computer', 'computing': 'compute', 'computed': 'compute',
            'programs': 'program', 'programming': 'program', 'programmed': 'program',
            'databases': 'database', 'networks': 'network', 'algorithms': 'algorithm'
        }
        
        # Common suffix patterns and their replacements
        self.suffix_patterns = [
            (r'ies$', 'y'),           # studies -> study
            (r'ves$', 'f'),           # wolves -> wolf
            (r'ses$', 's'),           # analyses -> analysis
            (r'xes$', 'x'),           # boxes -> box
            (r'ches$', 'ch'),         # watches -> watch
            (r'shes$', 'sh'),         # wishes -> wish
            (r'ments$', 'ment'),      # developments -> development
            (r'ents$', 'ent'),        # students -> student
            (r'ions$', 'ion'),        # connections -> connection
            (r'ers$', 'er'),          # teachers -> teacher
            (r'ings$', 'ing'),        # meetings -> meeting
            (r'lys$', 'ly'),          # families -> family
            (r'ied$', 'y'),           # tried -> try
            (r'ied$', 'y'),           # studied -> study
        ]
    
    def lemmatize_noun(self, word):
        """Lemmatize noun forms"""
        # Check dictionary first
        if word.lower() in self.lemma_dict:
            return self.lemma_dict[word.lower()]
        
        # Apply suffix patterns
        for pattern, replacement in self.suffix_patterns:
            if re.search(pattern, word.lower()):
                return re.sub(pattern, replacement, word.lower())
        
        # Simple plural removal
        if word.endswith('s') and len(word) > 3:
            return word[:-1]
        
        return word.lower()
    
    def lemmatize_verb(self, word):
        """Lemmatize verb forms"""
        # Check dictionary first
        if word.lower() in self.lemma_dict:
            return self.lemma_dict[word.lower()]
        
        # Remove common verb endings
        if word.endswith('ing'):
            if len(word) > 5:
                return word[:-3]  # Remove 'ing'
        elif word.endswith('ed'):
            if len(word) > 4:
                return word[:-2]  # Remove 'ed'
        elif word.endswith('s') and len(word) > 3:
            return word[:-1]  # Remove 's'
        
        return word.lower()
    
    def lemmatize(self, word, pos_tag='noun'):
        """
        Main lemmatization function
        
        Args:
            word (str): Word to lemmatize
            pos_tag (str): Part of speech tag ('noun', 'verb', 'adjective')
        
        Returns:
            str: Lemma of the word
        """
        if not isinstance(word, str) or len(word) <= 2:
            return word.lower()
        
        word = word.lower()
        
        # Check dictionary first
        if word in self.lemma_dict:
            return self.lemma_dict[word]
        
        # Apply POS-specific lemmatization
        if pos_tag == 'verb':
            return self.lemmatize_verb(word)
        elif pos_tag == 'noun':
            return self.lemmatize_noun(word)
        else:
            # Try both noun and verb rules
            noun_lemma = self.lemmatize_noun(word)
            verb_lemma = self.lemmatize_verb(word)
            
            # Return the shorter one (usually more basic)
            return noun_lemma if len(noun_lemma) <= len(verb_lemma) else verb_lemma

def apply_lemmatization_to_tokens(tokens, pos_tags=None):
    """
    Apply lemmatization to a list of tokens.
    
    Args:
        tokens (list): List of word tokens
        pos_tags (list): List of POS tags for each token (optional)
        
    Returns:
        list: List of lemmatized tokens
    """
    if not isinstance(tokens, list):
        return []
    
    lemmatizer = SimpleLemmatizer()
    
    if pos_tags is None:
        # Default to noun lemmatization
        return [lemmatizer.lemmatize(token) for token in tokens]
    else:
        # Use provided POS tags
        lemmatized = []
        for token, pos in zip(tokens, pos_tags):
            if pos.startswith('V'):  # Verb
                lemmatized.append(lemmatizer.lemmatize(token, 'verb'))
            elif pos.startswith('N'):  # Noun
                lemmatized.append(lemmatizer.lemmatize(token, 'noun'))
            else:
                lemmatized.append(lemmatizer.lemmatize(token))
        return lemmatized

def apply_lemmatization_to_series(token_series, pos_tags_series=None):
    """
    Apply lemmatization to a pandas Series of token lists.
    
    Args:
        token_series (pd.Series): Series containing token lists
        pos_tags_series (pd.Series): Series containing POS tag lists
        
    Returns:
        pd.Series: Series with lemmatized tokens
    """
    if pos_tags_series is None:
        return token_series.apply(apply_lemmatization_to_tokens)
    else:
        return pd.Series([
            apply_lemmatization_to_tokens(tokens, pos_tags)
            for tokens, pos_tags in zip(token_series, pos_tags_series)
        ])

# Example usage and testing
if __name__ == "__main__":
    # Test examples
    test_words = [
        "studies", "studying", "studied", "corpora", "geese",
        "better", "running", "computers", "analyses", "phenomena"
    ]
    
    lemmatizer = SimpleLemmatizer()
    
    print("=== Lemmatization Examples ===")
    for word in test_words:
        lemma = lemmatizer.lemmatize(word)
        print(f"{word:<15} -> {lemma}")
    
    print("\n=== Token Lemmatization Examples ===")
    test_tokens = [
        ["studies", "computers", "running"],
        ["geese", "better", "analyses"],
        ["phenomena", "corpora", "women"]
    ]
    
    for tokens in test_tokens:
        lemmatized = apply_lemmatization_to_tokens(tokens)
        print(f"Original: {tokens}")
        print(f"Lemmatized: {lemmatized}")
        print("-" * 50)
