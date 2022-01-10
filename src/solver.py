from tkinter import *

directions = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1]]

class Solver:
    def __init__(self, wordsearch, MAX, words, window):
        self.wordsearch = wordsearch
        self.MAX = MAX
        self.words = words
        self.window = window

    def find_instance_of_starting(self, letter):
        coordinates = []
        indx = 0
        for indxR, _ in enumerate(self.wordsearch):
            for indxC, _ in enumerate(self.wordsearch):
                curr = self.wordsearch[indxR][indxC]
                if curr == letter:
                    coordinates.append([])
                    coordinates[indx] = [indxR, indxC]
                    indx += 1
        return coordinates

    def look_in_all_directions(self, coordinates, word):
        found = False
        found_coordinates = []
        for c in coordinates:
            if found:
                break
            for d in directions:    
                found_coordinates = []
                found_word = ''
                for i in range(len(word)):
                    currR = c[0] + i * d[0]
                    currC = c[1] + i * d[1]
                    if currR < 0 or currR >= self.MAX:
                        break
                    if currC < 0 or currC >= self.MAX:
                        break
                    if self.wordsearch[currR][currC] == word[i]:
                        found_coordinates.append([])
                        found_coordinates[i] = [currR, currC]
                        found_word += word[i]
                        continue
                    break
                if found_word == word:
                    found = True
                    break
        return found_coordinates

    def color_found_word(self, coordinates):
        for coords in coordinates:
            lbl = Label(self.window, text=self.wordsearch[coords[0]][coords[1]], padx=10, pady=10, fg="red", font=('Arial', 25))
            lbl.grid(row=coords[0], column=coords[1])

    def solve(self):
        for word in self.words:
            initial_coordinates = self.find_instance_of_starting(word[0])
            found_coords = self.look_in_all_directions(initial_coordinates, word)
            self.color_found_word(found_coords)