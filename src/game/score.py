from constants import EMPTY_GAMEBOARD

"""This module is responsible for tracking the frequencies of letters and bigrams. These frequencies will be used to find the 
best Word for WordleGame's next guess to either (guess this Word, if str(Word) == self.answer), or eliminate the most amount
of guesses from self.guess_list"""

def letter_frequency(sample: list[str]) -> dict[str: int]:
    """Return a dictionary containing the amount of times each letter in the alphabet appears in a list of strings. 
    
    Precondition:
    - sample is a list of strings only containing lowercase letters.
    """
    result = EMPTY_GAMEBOARD

    for word in sample:
        for letter in word:
            result[letter] += 1
    
    
    return result

def bigram_frequency(sample: list[str]) -> dict[str: int]:
    """Return a dictionary containing every bigram that appears at least twice in a list of strings.
    
    Precondition:
    - sample is a list of strings only containing lowercase letters.
    """
    result = {}

    for word in sample:
        bigrams = fetch_bigrams(word)
        for bigram in bigrams:
            if not bigram in result:
                result[bigram] = 1
            else:
                result[bigram] += 1
    
    return result

def fetch_bigrams(word: str) -> list[str]:
    """Return a list of bigrams from word. The length of the resulting list will be exactly one less than the length of word"""
    result = []

    for i in range(0, len(word) - 1):
        result.append(word[i] + word[i + 1])
    
    return result