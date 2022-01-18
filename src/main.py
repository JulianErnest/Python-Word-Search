import tkinter as tk
import string
import random
from words import ALL_WORDS
from solver import *
from PIL import Image, ImageTk
window = tk.Tk()

direction = ['h', 'v', 'd', 'rh', 'rv', 'rd']
MAX = 15

# * Color theme:  https://coolors.co/03045e-023e8a-0077b6-0096c7-00b4d8-48cae4-90e0ef-ade8f4-caf0f8


light_blue = "#caf0f8"
light_blue_2 = "#ade8f4"
dark_blue = "#0077b6"
options = ["DOTA HEROES", "VALORANT CHAMPIONS", "PROGRAMMING LANGUAGES", "COMPUTER PARTS", "TECH BRANDS", "FASTFOOD RESTAURANTS"]

class Main:
    direction_multiplier_horizontal = [0, 1]
    direction_multiplier_horizontalR = [0, -1]

    direction_multiplier_vertical = [1, 0]
    direction_multiplier_verticalR = [-1, 0]

    direction_multiplier_diagonal = [1, 1]
    direction_multiplier_diagonalR = [1, -1]
    wordsearch = []
    def __init__(self):
        self.words = ''
        self.selected_letters = ''
        self.current_index_selected = 0
        self.selected_indices = []

    def main(self):
        self.initialize_app()

    def choose_option(self, chosen_indx):
        print(chosen_indx)
        self.words = ALL_WORDS[chosen_indx]
        self.generate_custom()
        self.show_options_words()
        self.show_actions()
    
    def show_options(self):
        if self.words:
            self.table_frame.grid_forget()
            self.table_frame.destroy()
        self.options_frame = tk.Frame(window)
        self.options_frame.grid(row=3, column=1)
        self.options_frame.configure(background=light_blue)
        for i in range(len(options)):
            option_label = Button(self.options_frame, text=options[i], padx=10, pady=10, bg=light_blue, fg=dark_blue, font=("Roboto", 14), command=lambda i=i:(self.choose_option(i)), width=40)
            option_label.grid(row=i, column=1, pady=20)

    def generate_custom(self):
        # * Generates the matrix, size depending on 'MAX' var
        # TODO: Make it user interactive
        self.createMatrix()
        # * Places the words in the matrix in random starting point and direction
        self.generate_words()
        # * Fills other spaces with random letters
        self.fill_empty()
        # * Make the window
        self.create_table()

    def solve(self):
        solve = Solver(self.wordsearch, MAX, self.words, self.table_frame)
        solve.solve()

    def initialize_app(self):
        window.configure(background=light_blue)
        # Logo
        image = Image.open("./assets/logo.png")
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(image=photo, bg=light_blue)
        label.image = photo
        label.grid(column=1, row=0, pady=10)

        # Left side
        image_option_text = Label(window, text="Upload a word search problem, and watch me solve it!", padx=10, pady=10, bg=light_blue, fg=dark_blue, font=("Roboto", 14))
        browse_text = StringVar()
        button_image = Button(window, text=browse_text, command=self.solve)
        browse_text.set("Upload")
        image_option_text.grid(column=0, row=1)
        button_image.grid(column=0, row=2)

        # Right side
        custom_option_text = Label(window, text="Play and choose from a custom list of topics, (always random!)", padx=10, pady=10, bg=light_blue, fg=dark_blue, font=("Roboto", 14))
        button_custom = Button(window, text="Play", command=self.show_options)
        custom_option_text.grid(column=2, row=1)
        button_custom.grid(column=2, row=2)

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
                    direction_mult = self.direction_multiplier_horizontal
                elif d == 'rh':
                    direction_mult = self.direction_multiplier_horizontalR
                elif d == 'v':
                    direction_mult = self.direction_multiplier_vertical
                elif d == 'rv':
                    direction_mult = self.direction_multiplier_verticalR
                elif d == 'd':
                    direction_mult = self.direction_multiplier_diagonal
                else:
                    direction_mult = self.direction_multiplier_diagonalR
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

    def select_letter(self, row, col):
        self.selected_letters += self.wordsearch[row][col]
        self.selected_indices.append([])
        self.selected_indices[self.current_index_selected] = [row, col]
        lbl = Button(self.table_frame, text=self.wordsearch[row][col], background='red')
        lbl.grid(row=row, column=col, padx=10, pady=10)
        self.current_index_selected += 1
    
    def confirm_selected(self):
        if self.selected_letters in self.words:
            for indx in self.selected_indices:
                btn = Button(self.table_frame, text=indx[0][1], background='green')
                btn.grid(row=indx[0], column=indx[1], padx=10, pady=10)
        self.selected_letters = '' 
    
    def show_options_words(self):
        self.options_frame = tk.Frame(window)
        self.options_frame.configure(background=dark_blue, pady=20)
        self.options_frame.grid(row=4, column=1, sticky="n")
        row = 0
        col = 0
        for x in range(len(self.words)):
            lbl = Label(self.options_frame, text=self.words[x])
            if col % 5 == 0 and col != 0:
                row += 1
                col = 0
            print(row, "row")
            print(col, "col")
            lbl.grid(row=row, column=col)
            col += 1

    def show_actions(self):
        self.confirm_button = Button(window, text="Confirm", background='green')
        self.confirm_button.grid(row=3, column=2, padx=10, pady=10)
        self.cancel_button = Button(window, text="Cancel", background='red')
        self.cancel_button.grid(row=3, column=0, padx=10, pady=10)
        
    def create_table(self):
        self.table_frame = tk.Frame(window)
        self.table_frame.configure(background=dark_blue)
        self.table_frame.grid(row=3, column=1, sticky="n")
        for row in range(MAX):
            for col in range(MAX):
                btn = Button(self.table_frame, text=self.wordsearch[row][col], background=light_blue_2, command=lambda row=row, col=col:self.select_letter(row, col))
                btn.grid(row=row, column=col, padx=10, pady=10)
    


a = Main()
a.main()

window.mainloop()
