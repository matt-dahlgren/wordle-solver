"""Class representing a Word played in a WordleGame. Each word is exactly 5 letters long."""

class Word():
    """A Word containing an ordered list of letters.
    
    Attributes:
    - letters: an ordered list of single letters representing Word.
    - score: a word's score is initialized at -1, otherwise it updated before each round fo a WordleGame to determine what the
             next guess of the game is.
    - word: a string representation of Word.
    """
    letters: list[str]
    score: int

    def __init__(self, word: str) -> None:
        self.letters = list(word)
        #TODO: fix the scoring
        self.score = -1
        self.word = word
    
    def __str__(self) -> str:
        return self.word
    
    def score_word(self, mono_freq: dict[str, float], bi_freq: dict[str, float]) -> None:
        """Return a score dictating the frequency of letters and bigrams in Word.
        When WordleGame updates its guess bank, each word will be assigned a score based off frequencies of letters
        and bigrams in the remaining answers, recorded in mono_freq and bi_freq.
        """

        result = 0

        for letter in mono_freq:
            if letter in self.word:
                result += mono_freq[letter]
        
        for bigram in bi_freq:
            if bigram in self.word:
                result += bi_freq[letter]
        
        self.score = result