from word_structure import Word
from constants import ALPHABET, guess_bank, answer_bank
from score import letter_frequency, bigram_frequency

class WordleGame():
    """An abstract class referring to a WordleGame. All WordleGames end after 6 turns.
    
    Attributes:
    - answer: the answer to this WordleGame.
    - turn: the turn number of this WordleGame.
    - previous_guesses: guesses made in this game.
    - valid_guesses: a list of valid five letter Word guesses.
    """
    answer: str
    turn: int
    previous_guesses: list[int]
    valid_guesses: list[Word]

    def __init__(self, answer: str) -> None:
        self.answer = answer
        self.previous_guesses = []
        self.valid_guesses = []
        guess_bank.open()
        line = guess_bank.readline().split()
        while line != '':
            self.valid_guesses.append(Word(line))
            line = guess_bank.readline().split()
        guess_bank.close()
        self.turn = 0
    
    def make_guess(self, guess: str) -> None:
        raise NotImplementedError
    
    def run(self) -> bool:
        raise NotImplementedError

class ComputerWordleGame(WordleGame):
    """A WordleGame that will be played entirely through this program.
    
    Attributes:
    - valid_answers: a list of valid answers.
    - current_board: a dictionary of possible letters at each position in a word.
    - is_yellow: list of letters in word, but not in position guessed. 
    """
    valid_answers: list[str]
    current_board: dict[int: str]
    is_yellow: list[str]

    def __init__(self, answer: str) -> None:
        WordleGame.__init__(answer)
        self.valid_answers = []
        self.is_yellow = []
        self.current_board = {0: ALPHABET, 1: ALPHABET, 2: ALPHABET, 3: ALPHABET, 4: ALPHABET}
        # Sets the board so that all letters are valid in any position before any guesses have been made.
        answer_bank.open()
        line = answer_bank.readline().split()
        while line != '':
            self.valid_answers.append(line)
            line = answer_bank.readline().split()
        answer_bank.close()
        monograms = letter_frequency(self.valid_answers)
        bigrams = bigram_frequency(self.valid_answers)
        
        # Score each word in our guess list in preperation
        for word in self.valid_guesses:
            word.score_word(monograms, bigrams)
    
    def find_highest_score(self) -> str:
        """Return the highest scoring Word's string in self.valid_guesses
        Return the empty string if self.valid_guesses is empty
        """
        high_score = 0
        result = ''

        for word in self.valid_guesses:
            if word.score > high_score:
                result = word.word
                high_score = word.score
        
        return result
    
    def update_libraries(self) -> None:
        """Update self.valid_guesses and self.valid_answers by removing words that have found letters not to be in self.answer.
        """
        # Update self.valid_guesses
        for guess in self.valid_guesses:
            for yellow_letter in self.is_yellow:
                if yellow_letter not in guess.word:
                    self.valid_guesses.remove(guess)
            for i in range(0, 5):
                if guess.word[i] not in self.current_board[i]:
                    self.valid_guesses.remove(guess)
        
        for answer in self.valid_answers:
            for yellow_letter in self.is_yellow:
                if yellow_letter not in answer:
                    self.valid_answers.remove(answer)
            for k in range(0, 5):
                if answer[k] not in self.current_board[k]:
                    self.valid_answers.remove(answer)
    
    def make_guess(self, guess: str) -> bool:
        """Make a guess. Return True if the guess is the answer to the game. If the guess is 
        wrong update the current_board
        """
        if guess == self.answer:
            return True
        else:
            for i in range(0, 5):
                if guess[i] == self.answer[i]:
                    self.current_board[i] = guess[i]
                elif guess[i] in self.answer:
                    letter_index = str(self.current_board[i]).index(guess[i])
                    self.is_yellow.append(guess[i])
                    self.current_board[i] = self.current_board[i][:letter_index] + self.current_board[i][letter_index + 1:]
                else:
                    for k in range(0, 5):
                        if guess[i] in self.current_board[k]:
                            letter_index = str(self.current_board[k]).index(guess[i])
                            self.current_board[k] = self.current_board[k][:letter_index] + self.current_board[k][letter_index + 1:]
        return False
    
    def run(self) -> int:
        """Run a ComputerWordleGame, return self.turn if the answer is guessed on that turn. Return False otherwise."""
        win = False
        while self.turn < 6 and not win:
            self.turn += 1
            win = self.make_guess(self.find_highest_score())
            if not win:
                self.update_libraries
        return win
    
if __name__ == '__main__':
    new_game = ComputerWordleGame('movie')
    print(new_game.run())