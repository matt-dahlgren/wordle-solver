from typing import TextIO
from word_structure import Word
from constants import EMPTY_GAMEBOARD, ALPHABET

guess_bank = "guess_answer_banks/valid_guesses.txt"
answer_bank = "guess_answer_banks/valid_answers.txt"

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
    current_board: dict[int: list[str]]
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
