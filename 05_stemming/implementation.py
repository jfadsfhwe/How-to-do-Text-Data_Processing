"""
Stemming Implementation
"""

import re
import pandas as pd

class PorterStemmer:
    """
    Simple implementation of Porter Stemming Algorithm
    """
    
    def __init__(self):
        self.vowels = {'a', 'e', 'i', 'o', 'u'}
    
    def is_consonant(self, word, i):
        """Check if character at position i is a consonant"""
        if word[i] in self.vowels:
            return False
        if word[i] == 'y':
            if i == 0:
                return True
            else:
                return not self.is_consonant(word, i-1)
        return True
    
    def measure(self, stem):
        """Measure the number of consonant sequences in stem"""
        groups = 0
        i = 0
        while i < len(stem):
            if self.is_consonant(stem, i):
                groups += 1
                while i < len(stem) and self.is_consonant(stem, i):
                    i += 1
            else:
                while i < len(stem) and not self.is_consonant(stem, i):
                    i += 1
        return groups
    
    def contains_vowel(self, stem):
        """Check if stem contains a vowel"""
        for i in range(len(stem)):
            if not self.is_consonant(stem, i):
                return True
        return False
    
    def ends_with_double_consonant(self, stem):
        """Check if stem ends with double consonant"""
        if len(stem) < 2:
            return False
        return (self.is_consonant(stem, len(stem)-1) and 
                self.is_consonant(stem, len(stem)-2) and 
                stem[-1] == stem[-2])
    
    def ends_with_cvc(self, stem):
        """Check if stem ends with consonant-vowel-consonant pattern"""
        if len(stem) < 3:
            return False
        return (self.is_consonant(stem, len(stem)-1) and 
                not self.is_consonant(stem, len(stem)-2) and 
                self.is_consonant(stem, len(stem)-3) and
                stem[-3] not in {'w', 'x', 'y'})
    
    def step1a(self, word):
        """Step 1a of Porter algorithm"""
        if word.endswith('sses'):
            return word[:-2]
        elif word.endswith('ies'):
            return word[:-2]
        elif word.endswith('ss'):
            return word
        elif word.endswith('s'):
            return word[:-1]
        return word
    
    def step1b(self, word):
        """Step 1b of Porter algorithm"""
        stem = word
        if stem.endswith('eed'):
            if self.measure(stem[:-3]) > 0:
                return stem[:-1]
        elif stem.endswith('ed'):
            if self.contains_vowel(stem[:-2]):
                stem = stem[:-2]
                if stem.endswith('at') or stem.endswith('bl') or stem.endswith('iz'):
                    stem += 'e'
                elif self.ends_with_double_consonant(stem) and not stem.endswith('l') and not stem.endswith('s') and not stem.endswith('z'):
                    stem = stem[:-1]
                elif self.measure(stem) == 1 and self.ends_with_cvc(stem):
                    stem += 'e'
        elif stem.endswith('ing'):
            if self.contains_vowel(stem[:-3]):
                stem = stem[:-3]
                if stem.endswith('at') or stem.endswith('bl') or stem.endswith('iz'):
                    stem += 'e'
                elif self.ends_with_double_consonant(stem) and not stem.endswith('l') and not stem.endswith('s') and not stem.endswith('z'):
                    stem = stem[:-1]
                elif self.measure(stem) == 1 and self.ends_with_cvc(stem):
                    stem += 'e'
        return stem
    
    def step1c(self, word):
        """Step 1c of Porter algorithm"""
        if word.endswith('y') and self.contains_vowel(word[:-1]):
            return word[:-1] + 'i'
        return word
    
    def step2(self, word):
        """Step 2 of Porter algorithm"""
        suffixes = {
            'ational': 'ate',
            'tional': 'tion',
            'enci': 'ence',
            'anci': 'ance',
            'izer': 'ize',
            'abli': 'able',
            'alli': 'al',
            'entli': 'ent',
            'eli': 'e',
            'ousli': 'ous',
            'ization': 'ize',
            'ation': 'ate',
            'ator': 'ate',
            'alism': 'al',
            'iveness': 'ive',
            'fulness': 'ful',
            'ousness': 'ous',
            'aliti': 'al',
            'iviti': 'ive',
            'biliti': 'ble'
        }
        
        for suffix, replacement in suffixes.items():
            if word.endswith(suffix):
                stem = word[:-len(suffix)]
                if self.measure(stem) > 0:
                    return stem + replacement
        return word
    
    def step3(self, word):
        """Step 3 of Porter algorithm"""
        suffixes = {
            'icate': 'ic',
            'ative': '',
            'alize': 'al',
            'iciti': 'ic',
            'ical': 'ic',
            'ful': '',
            'ness': ''
        }
        
        for suffix, replacement in suffixes.items():
            if word.endswith(suffix):
                stem = word[:-len(suffix)]
                if self.measure(stem) > 0:
                    return stem + replacement
        return word
    
    def step4(self, word):
        """Step 4 of Porter algorithm"""
        suffixes = ['al', 'ance', 'ence', 'er', 'ic', 'able', 'ible', 'ant', 'ement', 
                   'ment', 'ent', 'ion', 'ou', 'ism', 'ate', 'iti', 'ous', 'ive', 'ize']
        
        for suffix in suffixes:
            if word.endswith(suffix):
                stem = word[:-len(suffix)]
                if self.measure(stem) > 1:
                    return stem
        
        if word.endswith('ion'):
            stem = word[:-3]
            if self.measure(stem) > 1 and stem[-1] in {'s', 't'}:
                return stem
        
        return word
    
    def step5a(self, word):
        """Step 5a of Porter algorithm"""
        if word.endswith('e'):
            stem = word[:-1]
            if self.measure(stem) > 1:
                return stem
            elif self.measure(stem) == 1 and not self.ends_with_cvc(stem):
                return stem
        return word
    
    def step5b(self, word):
        """Step 5b of Porter algorithm"""
        if self.ends_with_double_consonant(word) and word.endswith('l') and self.measure(word[:-1]) > 1:
            return word[:-1]
        return word
    
    def stem(self, word):
        """Main stemming function"""
        if not isinstance(word, str) or len(word) <= 2:
            return word
        
        word = word.lower()
        
        # Apply all steps
        word = self.step1a(word)
        word = self.step1b(word)
        word = self.step1c(word)
        word = self.step2(word)
        word = self.step3(word)
        word = self.step4(word)
        word = self.step5a(word)
        word = self.step5b(word)
        
        return word

def simple_stemmer(word):
    """
    Very simple stemmer using basic rules
    """
    if not isinstance(word, str) or len(word) <= 3:
        return word.lower()
    
    word = word.lower()
    
    # Basic suffix removal
    suffixes = ['ing', 'ly', 'ed', 'es', 's']
    for suffix in suffixes:
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[:-len(suffix)]
    
    return word

def apply_stemming_to_tokens(tokens, stemmer_type='porter'):
    """
    Apply stemming to a list of tokens.
    
    Args:
        tokens (list): List of word tokens
        stemmer_type (str): 'porter' or 'simple'
        
    Returns:
        list: List of stemmed tokens
    """
    if not isinstance(tokens, list):
        return []
    
    if stemmer_type == 'porter':
        stemmer = PorterStemmer()
        return [stemmer.stem(token) for token in tokens]
    elif stemmer_type == 'simple':
        return [simple_stemmer(token) for token in tokens]
    else:
        raise ValueError("stemmer_type must be 'porter' or 'simple'")

def apply_stemming_to_series(token_series, stemmer_type='porter'):
    """
    Apply stemming to a pandas Series of token lists.
    
    Args:
        token_series (pd.Series): Series containing token lists
        stemmer_type (str): 'porter' or 'simple'
        
    Returns:
        pd.Series: Series with stemmed tokens
    """
    return token_series.apply(lambda x: apply_stemming_to_tokens(x, stemmer_type))

# Example usage and testing
if __name__ == "__main__":
    # Test examples
    test_words = [
        "running", "studies", "organization", "computing", 
        "university", "connection", "relational", "electricity"
    ]
    
    stemmer = PorterStemmer()
    
    print("=== Stemming Examples ===")
    for word in test_words:
        porter_result = stemmer.stem(word)
        simple_result = simple_stemmer(word)
        print(f"Original: {word:15} Porter: {porter_result:10} Simple: {simple_result}")
    
    print("\n=== Token Stemming Examples ===")
    test_tokens = [
        ["running", "studies", "organization"],
        ["computing", "university", "connection"],
        ["relational", "electricity", "programming"]
    ]
    
    for tokens in test_tokens:
        stemmed = apply_stemming_to_tokens(tokens, 'porter')
        print(f"Original: {tokens}")
        print(f"Stemmed: {stemmed}")
        print("-" * 50)
