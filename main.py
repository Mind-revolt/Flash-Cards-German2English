import pandas
from tkinter import *
import random
import csv
BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ('Arial', 40, 'italic')
LANGUAGE_POS = 400, 150
WORD_FONT = ('Arial', 60, 'bold')
WORD_POS = 400, 260
GERMAN_LANGUAGE = 'Deutsch'
ENGLISH_LANGUAGE = 'English'
OLD_IMAGE = 'images/card_front.png'
NEW_IMAGE = 'images/card_back.png'

# -------------------------------- START --------------------------------- #
data = pandas.read_csv('data/words_DE-EN.csv')

to_learn = data.to_dict(orient='records')

current_card = {}
# -------------------------------- NEXT CARD --------------------------------- #
def next_card():
    # to save something into a variable that can be used outside the function
    # type global <nameofthevariable> and write the action you want to save.
    global current_card
    try:
        current_card = random.choice(words_to_learn)
    except NameError:
        current_card = random.choice(to_learn)
    print(current_card["German"])
    canvas.itemconfig(card_background, image=card_front_image)
    canvas.itemconfig(card_title, text="German", fill='black')
    canvas.itemconfig(card_word, text=current_card["German"], fill='black')
    window.after(3000, func=flip_cards)

# -------------------------------- FLIP CARD --------------------------------- #
def flip_cards():
    canvas.itemconfig(card_background, image=card_back_image)
    canvas.itemconfig(card_title, text='English', fill='white')
    canvas.itemconfig(card_word, text=current_card['English'], fill='white')

# -------------------------------- WORD LEARNED ---------------------------------------- #
try:
    words_to_learn_csv = pandas.read_csv('data/words_to_learn1.csv', index_col=False)
    words_to_learn = words_to_learn_csv.to_dict(orient='records')
except FileNotFoundError:
    pass
def word_learned():
    try:
        words_to_learn.remove(current_card)
        x = pandas.DataFrame(words_to_learn)
        words_csv = x.to_csv('data/words_to_learn1.csv')
    except NameError:
        to_learn.remove(current_card)
        x = pandas.DataFrame(to_learn)
        words_csv = x.to_csv('data/words_to_learn1.csv')
    print(current_card)
    next_card()

# -------------------------------- UI ---------------------------------------- #
window = Tk()
window.title('Flash-Cards')
window.minsize(width=820, height=600)
window.config(pady=20, padx=20, highlightthickness=0, bg=BACKGROUND_COLOR)

window.after(3000, func=flip_cards)

canvas = Canvas(width=800, height=526, highlightthickness=0)
card_front_image = PhotoImage(file=OLD_IMAGE)
card_back_image = PhotoImage(file=NEW_IMAGE)
card_background = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(400, 158, text="Title", font=LANGUAGE_FONT)
card_word = canvas.create_text(400, 263, text='word', font=WORD_FONT)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)


# create buttons
right_image = PhotoImage(file='images/right.png')
right_button = Button(image=right_image, highlightthickness=0, width=100, height=100, command=word_learned)
right_button.grid(column=1, row=1)
wrong_image = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=wrong_image, highlightthickness=0, width=100, height=100, command=next_card)
wrong_button.grid(column=0, row=1)


with open('data/words_to_learn1.csv', mode='r') as file:
    word = 'dunkel'
    words_file = csv.reader(file)
    for line in words_file:
        if word in str(line):
            print(line)

next_card()
window.mainloop()
