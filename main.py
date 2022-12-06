from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}

# ---------------------------- CREATE NEW FLASH CARDS ------------------------------- #
# Try reading from words_to_learn.csv except if it doesn't exist then read from french_words.csv
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
words_dict = data.to_dict(orient="records")

def random_word():
    '''1. Randomly generate a pair of keys from the dictionary generated using pandas from csv.
       2. Change card title to "French" , text color to black, and card image to white.
       3. Display value of the French key.
       4. Cancel timer then reactivate after a card is generated.'''
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(words_dict)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_image, image=front_image)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    '''Change card title to "English", text color to white, and card image to green.
    Display value of English key.'''
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word,text=current_card["English"], fill="white")
    canvas.itemconfig(canvas_image, image=back_image)

def is_correct():
    '''Remove current pair of keys from the dictionary then create a dataframe from the remaining
    keys and finally create/add dataframe to words_to_learn.csv.'''
    words_dict.remove(current_card)
    df = pandas.DataFrame(words_dict)
    df.to_csv("data/words_to_learn.csv", index=False)
    random_word()
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flash Card")
window.config(padx=5, pady=5, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=880, height=550, bg=BACKGROUND_COLOR, highlightthickness=0)
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(450, 280, image=front_image)
card_title = canvas.create_text(430, 150, text="Title", font=("Arial", 34, "italic"))
card_word = canvas.create_text(430, 350, text="word", font=("Arial", 44, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

x_img = PhotoImage(file="images/wrong.png")
x_button = Button(image=x_img, highlightthickness=0, command=random_word)
x_button.grid(column=0, row=1)

check_img = PhotoImage(file="images/right.png")
check_button = Button(image=check_img, highlightthickness=0, command=is_correct)
check_button.grid(column=1, row=1)

random_word()

window.mainloop()