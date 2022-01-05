from tkinter import *
import string
import random
window = Tk()

words = ["LINA", "AXE", "INVOKER", "MEDUSA", "EMBER"]
currWordIdx = 0;
currLetterWordIdx = 0;
direction = ['h', 'v', 'd', 'rh', 'rv', 'rd'];
MAX = 15;

direction_multiplier_horizontal = [1, 0]
direction_multiplier_horizontalR = [-1, 0]

direction_multiplier_vertical = [0, 1]
direction_multiplier_verticalR = [0, -1]

direction_multiplier_diagonal = [1, 1]
direction_multiplier_diagonalR = [-1, -1]

wordsearch = []
for row in range(0,MAX):
  wordsearch.append([])
  for col in range(0,MAX):
    wordsearch[row].append("-")

def getDirection():
    return random.choice(direction)

def decideReverse(startingIndex):
    lastIndex = startingIndex + len(word) 
    print("last index:", lastIndex)
    if lastIndex > MAX or lastIndex < 0:
        return -1
    return 1

def getStartingIndex():
    return random.randrange(0, MAX - 1)

def checkOverlap(word, direction, initial_x, initial_y):
    if word != words[0]:
        for i in range(len(word)):
            curr = 'A';
            if direction == 'h':
                curr = wordsearch[initial_x + i * direction_multiplier_horizontal[0]][initial_y + i * direction_multiplier_horizontal[1]]
            elif direction == 'rh':
                curr = wordsearch[initial_x + i * direction_multiplier_horizontalR[0]][initial_y + i * direction_multiplier_horizontalR[1]]
            elif direction == 'v':
                curr = wordsearch[initial_x + i * direction_multiplier_vertical[0]][initial_y + i * direction_multiplier_vertical[1]]
            elif direction == 'rv':
                curr = wordsearch[initial_x + i * direction_multiplier_verticalR[0]][initial_y + i * direction_multiplier_verticalR[1]]
            elif direction == 'd':
                curr = wordsearch[initial_x + i * direction_multiplier_diagonal[0]][initial_y + i * direction_multiplier_diagonal[1]]
            else:
                curr = wordsearch[initial_x + i * direction_multiplier_diagonalR[0]][initial_y + i * direction_multiplier_diagonalR[1]]
            if curr != word[i] or curr != "-":
                return False
    return True

def checkFit(word, direction, x_initial, y_initial):
    last_x = 0;
    last_y = 0;
    if direction == 'h':
        last_x = x_initial + len(word) * direction_multiplier_horizontal[0]
        last_y = y_initial + len(word) * direction_multiplier_horizontal[1]
    elif direction == 'rh':
        last_x = x_initial + len(word) * direction_multiplier_horizontalR[0]
        last_y = y_initial + len(word) * direction_multiplier_horizontalR[1]
    elif direction == 'v':
        last_x = x_initial + len(word) * direction_multiplier_vertical[0]
        last_y = y_initial + len(word) * direction_multiplier_vertical[1]
    elif direction == 'rv':
        last_x = x_initial + len(word) * direction_multiplier_verticalR[0]
        last_y = y_initial + len(word) * direction_multiplier_verticalR[1]
    elif direction == 'd':
        last_x = x_initial + len(word) * direction_multiplier_diagonal[0]
        last_y = y_initial + len(word) * direction_multiplier_diagonal[1]
    elif direction == 'rd':
        last_x = x_initial + len(word) * direction_multiplier_diagonalR[0]
        last_y = y_initial + len(word) * direction_multiplier_diagonalR[1]
    if last_x < 0 and last_y >= MAX:
        return False
    return True

def add_to_matrix(word, direction, initial_x, initial_y):
    for i in range(len(word)):
        if direction == 'h':
            wordsearch[initial_x + i * direction_multiplier_horizontal[0]][initial_y + i * direction_multiplier_horizontal[1]] = word[i]
        elif direction == 'rh':
            wordsearch[initial_x + i * direction_multiplier_horizontalR[0]][initial_y + i * direction_multiplier_horizontalR[1]] = word[i]
        elif direction == 'v':
            wordsearch[initial_x + i * direction_multiplier_vertical[0]][initial_y + i * direction_multiplier_vertical[1]] = word[i]
        elif direction == 'rv':
            wordsearch[initial_x + i * direction_multiplier_verticalR[0]][initial_y + i * direction_multiplier_verticalR[1]] = word[i]
        elif direction == 'd':
            wordsearch[initial_x + i * direction_multiplier_diagonal[0]][initial_y + i * direction_multiplier_diagonal[1]] = word[i]
        else:
            wordsearch[initial_x + i * direction_multiplier_diagonalR[0]][initial_y + i * direction_multiplier_diagonalR[1]] = word[i]
        

for word in words:
    fit = False
    no_overlap = False
    while not fit or not no_overlap:
        d = getDirection()
        x_initial = getStartingIndex()
        y_initial = getStartingIndex()
        fit = checkFit(word, d, x_initial, y_initial)
        if not fit:
            continue
        no_overlap = checkOverlap(word, d, x_initial, y_initial)
        if not no_overlap:
            continue
        add_to_matrix(word, d, x_initial, y_initial)

for row in range(0,MAX):
    for col in range(0,MAX):
        print(wordsearch[col][row], end="")
    print("")

window.title("Word Search")
window.geometry("800x500")
window.mainloop()