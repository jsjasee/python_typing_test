from program import Program

program = Program()

program.window.mainloop()

# make the colour to word turn blue when the user is typing that word
# the green background should change to next word once user presses space
# future feature: implement the backspace mechanism, should return to previous word/entry the user typed?
# future feature: handle edge cases, person typing until it exceeds the length of the word, or copy and paste text inside without pressing space?

# calculate wpm once time is up, and disable user from typing in the entry box
# let the user try the typing test again -> use a "Try again" button (clear entry box, regenerate text, character count and restart timer etc.)