from tkinter import *
from solver import *
import string
import random
window = Tk()
print(window)

words = ["NUGGETS", "CHICKEN", "PURE", "FOODS", "CRAVE", "RIDE", "MEETING", "COMPUTER", "CODE"]
direction = ['h', 'v', 'd', 'rh', 'rv', 'rd'];
MAX = 15

direction_multiplier_horizontal = [0, 1]
direction_multiplier_horizontalR = [0, -1]

direction_multiplier_vertical = [1, 0]
direction_multiplier_verticalR = [-1, 0]

direction_multiplier_diagonal = [1, 1]
direction_multiplier_diagonalR = [1, -1]

wordsearch = []

class Main:
    def __init__(self, words):
        self.words = words
        self.wordsearch = wordsearch

    def main(self):
        # * Generates the matrix, size depending on 'MAX' var
        # TODO: Make it user interactive
        self.createMatrix()
        # * Places the words in the matrix in random starting point and direction
        self.generate_words()
        # * Fills other spaces with random letters
        self.fill_empty()
        # * Make the window
        self.create_window()

    def createMatrix(self):
        for row in range(0, MAX):
            self.wordsearch.append([])
            for col in range(0, MAX):
                self.wordsearch[row].append("-")

    def generate_words(self):
        for word in self.words:
            fit = False
            no_overlap = False
            while not fit or not no_overlap:
                d = self.getDirection()
                x_initial = self.getStartingIndex()
                y_initial = self.getStartingIndex()
                if d == 'h':
                    direction_mult = direction_multiplier_horizontal
                elif d == 'rh':
                    direction_mult = direction_multiplier_horizontalR
                elif d == 'v':
                    direction_mult = direction_multiplier_vertical
                elif d == 'rv':
                    direction_mult = direction_multiplier_verticalR
                elif d == 'd':
                    direction_mult = direction_multiplier_diagonal
                else:
                    direction_mult = direction_multiplier_diagonalR
                fit = self.checkFit(word, direction_mult, x_initial, y_initial)
                if not fit:
                    continue
                no_overlap = self.checkOverlap(word, direction_mult, x_initial, y_initial)
                if not no_overlap:
                    continue
                self.add_to_matrix(word, direction_mult, x_initial, y_initial)

    def getDirection(self):
        return random.choice(direction)

    def getStartingIndex(self):
        return random.randrange(MAX)

    def checkOverlap(self, word, direction_mult, initial_x, initial_y):
        if word != self.words[0]:
            for i in range(len(word)):
                curr = self.wordsearch[initial_x + i * direction_mult[0]][initial_y + i * direction_mult[1]]
                if curr == word[i]:
                    continue
                if curr != '-':
                    return False
        return True

    def checkFit(self, word, direction_mult, x_initial, y_initial):
        last_x = x_initial + len(word) * direction_mult[0]
        last_y = y_initial + len(word) * direction_mult[1]
        if last_x < 0 or last_x >= MAX:
            return False
        if last_y < 0 or last_y >= MAX:
            return False
        return True

    def add_to_matrix(self, word, direction_mult, initial_x, initial_y):
        for i in range(len(word)):
            self.wordsearch[initial_x + i * direction_mult[0]][initial_y + i * direction_mult[1]] = word[i]
            
    def fill_empty(self):
        for row in range(MAX):
            for col in range(MAX):
                if self.wordsearch[row][col] == '-':
                    self.wordsearch[row][col] = random.choice(string.ascii_uppercase)

    def create_window(self):
        solve = Solver(wordsearch, MAX, words, window)
        button = Button(window, text="Solve it", command=solve.solve)
        button.grid(row=16, column=16)
        for row in range(MAX):
            for col in range(MAX):
                lbl = Label(window, text=wordsearch[row][col], padx=10, pady=10)
                lbl.grid(row=row, column=col)

a = Main(words)
a.main()

window.title("Word Search")
window.geometry("800x800")
window.mainloop()
