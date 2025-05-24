from itertools import chain
from tkinter import *
import random
import time

# # this just runs a program to download a package of words, run this code for first time use
# import nltk
# nltk.download('words')
# nltk.download('brown') # this is a corpus (collection) of all the words with frequency info

from nltk.corpus import words, brown
from nltk import FreqDist

words_only = [word.lower() for word in brown.words() if word.isalpha()] # isalpha() checks if it is alphabet
freq_dist = FreqDist(words_only)
WORD_LIST = [word for word, freq in freq_dist.most_common(1000) if len(word) >= 3]

# WORD_LIST = words.words() # the original word list contains rare uncommon words
BLACKLIST_KEYS = ["BackSpace", "Shift_R", "Shift_L", "Return", "Left", "Right", "Up", "Down", "Meta_L", "Meta_R"]
TIMER = 10

class Program:
    def __init__(self):
        self.window = Tk()
        self.window.title("Typing Test")
        self.window.minsize(width=1000, height=500)
        self.words_index_dict = {}

        # Add title
        title = Label(text="Typing Speed Test", font=("Helvetica", 30, "bold"))
        title.grid(column=0, row=0)

        desc = Label(text="How fast are your fingers? Do the one-minute typing test to find out! Press the space bar after each word. "
                          "At the end, you'll get your typing speed in WPM. Good luck!", font=("Helvetica", 15, "italic"))
        desc.grid(column=0, row=1, pady=10, padx=10)

        self.typing_var = StringVar()
        self.user_entry = Entry(textvariable=self.typing_var)
        self.user_entry.bind("<KeyRelease>", self.track_typing)
        self.user_entry.grid(column=0, row=3)
        self.char_count = -1
        self.generated_text = self.add_typing_text()

        self.time_left = TIMER
        self.time_label = Label(text=f"Time left: {self.time_left}")
        self.time_label.grid(column=0, row=4)
        self.start_typing = False
        self.wpm_label = Label(text="")
        self.wpm_label.grid(column=0, row=5)
        self.try_again = Button(text="Try Again", state="disabled", command=self.restart)
        self.try_again.grid(column=0, row=6)

    def add_typing_text(self):
        random_para = random.sample(WORD_LIST, 300) # ensures no duplicates
        random_para_str = ' '.join(random_para)
        gen_text = Text(self.window, wrap="word")
        gen_text.insert("1.0", random_para_str) # first digit 1 means line 1, second digit is character position on that line, 0, means start from the first character
        gen_text.config(state="disabled") # prevent tying in the text box containing the prompt
        gen_text.grid(column=0, row=2)

        word = ""
        indexes = []
        for num in range(len(random_para_str)):
            if random_para_str[num] != " ":
                word += random_para_str[num]
                indexes.append("1." + str(num))
            else:
                word += " "
                indexes.append("1." + str(num))
                self.words_index_dict[word] = indexes
                word = ""
                indexes = []

        # Create a tag for the widget
        gen_text.tag_config("Selected", background="#99ccff")
        gen_text.tag_config("Unselected", background="") # resets background colour to default, effectively removing it
        gen_text.tag_config("Correct", background="#99ff99")
        gen_text.tag_config("Incorrect", background="#ff6666")

        # need to somehow assign a tag to the word as the user types, and change background colour accordingly
        # also need to get hold of the index of the word so that a tag can be assigned to the word
        print(self.words_index_dict)
        return gen_text

    def track_typing(self, event):
        # pressing shift will also increase the character by 1
        # this is sort of like the telebot, the function MUST accept an argument which is event.
        print(event.keysym)

        if not self.start_typing:
            self.start_typing = True
            self.start_timer()

        if event.keysym not in BLACKLIST_KEYS:
            self.char_count += 1
        elif event.keysym == "BackSpace" and self.char_count >= 0: # adding the >= 0 solved the bug of the offset by 1 when user press backspace all the way to the first character
            self.char_count -= 1

        current_index = "1." + str(self.char_count)
        print(current_index)
        print(self.generated_text.get(current_index))

        # when press BackSpace also need the current or previous index letter to remove formatting
        if event.keysym == "BackSpace":
            self.generated_text.tag_remove("Correct", "1." + str(self.char_count + 1))  # instead of putting current index which is the word it is in, this makes it so that the character IN FRONT of what you are typing is NOT formatted
            self.generated_text.tag_remove("Incorrect", "1." + str(self.char_count + 1))
            if current_index == "1.0":
                self.generated_text.tag_remove("Correct", current_index)  # instead of putting current index which is the word it is in, this makes it so that the character IN FRONT of what you are typing is NOT formatted
                self.generated_text.tag_remove("Incorrect", current_index)

        for word, list_of_indexes in self.words_index_dict.items():
            if current_index in list_of_indexes:
                print(list_of_indexes)
                self.generated_text.tag_add("Selected", list_of_indexes[0], f"{list_of_indexes[-1]} +1c")
                # note the end index, the 3rd argument, is NON-inclusive, so you HAVE to +1c to include the last character as well!
                # In Text.tag_add(start, end), the 'end' index is non-inclusive,
                # so the character at that position is not highlighted.
                # To ensure the last character of a word is included, use '+1c' on the final index.
                # For example: tag_add("tag", start, f"{end} +1c")
                if event.keysym not in BLACKLIST_KEYS:
                    if event.char == self.generated_text.get(current_index):
                        self.generated_text.tag_remove("Incorrect", current_index)
                        self.generated_text.tag_add("Correct", current_index, f"{current_index} +1c")
                    else:
                        self.generated_text.tag_remove("Correct", current_index)
                        self.generated_text.tag_add("Incorrect", current_index, f"{current_index} +1c")

            else:
                self.generated_text.tag_remove("Selected", list_of_indexes[0], f"{list_of_indexes[-1]} +1c")
                self.generated_text.tag_add("Unselected", list_of_indexes[0], f"{list_of_indexes[-1]} +1c")

    def start_timer(self):
        # while self.time_left > 0: # a while is extremely dangerous because it blocks the GUI from functioning and cannot run in the background, as mainloop is blocked
        # use another method like window.after() instead
        #     self.time_left -= 1
        #     self.time_label.config(text=f"Time left: {self.time_left}")
        #     time.sleep(1)

        if self.time_left > 0:
            self.time_left -= 1
            self.time_label.config(text=f"Time left: {self.time_left}")
            self.window.after(ms=1000, func=self.start_timer)

        elif self.time_left == 0:
            self.user_entry.delete(0, END)
            self.user_entry.config(state="disabled")
            self.user_entry.unbind("<KeyRelease>")
            self.calculate_wpm()
            self.try_again.config(state="active")

    def calculate_wpm(self):
        ranges = self.generated_text.tag_ranges("Correct")
        # print(ranges)
        correct_char = 0
        for num in range(0, len(ranges), 2):
            # range(0, len(ranges), 2) gives numbers that jumps by 2
            # since the ranges come in (start1, stop1, start2, stop2)
            # print(num)
            start = ranges[num]
            end = ranges[num + 1]
            correct_text = self.generated_text.get(start, end)
            correct_char += len(correct_text)

        self.wpm_label.config(text=f"Your wpm is {correct_char // 5}")


    def restart(self):
        self.wpm_label.config(text="")
        self.try_again.config(state="disabled")

        # reset the text and allow user to type in the box again, and also the timer and the index
        self.words_index_dict = {} # need to reset the dictionary otherwise the code will still previous index from previous run, messing up the index and 'Selected' functionality of the code
        self.time_left = TIMER
        self.time_label.config(text=f"Time left: {self.time_left}")
        self.char_count = -1
        self.generated_text.delete(0, END)
        self.generated_text = self.add_typing_text()
        self.user_entry.unbind("<KeyRelease>")
        self.user_entry.bind("<KeyRelease>", self.track_typing)
        self.user_entry.config(state="normal")

        self.start_typing = False
