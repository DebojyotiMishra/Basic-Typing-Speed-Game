from datetime import datetime
from time import sleep

# Description: A simple typing speed test program that uses python and only built-in libraries
# How to: 
# 1. After you provide your username, you will be provided with a sentence,
# 2. You will be able to type in the sentence after a 1 second delay
# 3. Press enter after typing to know your typing speed (and remember not to cheat - you won't be able to)


# -------------------- General Utility Functions --------------------
def clear(n=20):
    """clears the terminal with n newline characters"""
    print('\n'*n)


def average(lst):
    """returns average of elements of a provided list"""
    _sum = sum(lst)
    _len = len(lst)
    return round(_sum/_len, 1)


# -------------------- Typing Speed Calculation Functions --------------------
def get_words():
    """ Gets words from word_list.txt and returns a random selection of 5 words in the form of a list """
    from random import choice
    word_list_file = "word_list.txt"

    # getting words from word_list.txt
    with open(word_list_file, "r") as f:
        word_list = f.read()
        word_list = word_list.split("\n")

    words = []
    # choosing 5 random words from word_list and appending to words if it is not there
    for i in range(5):
        word = choice(word_list)
        if word not in words:
            words.append(word)
    return words


def accuracy(input_text, text):
    """ calculates accuracy of typing speed by comparing input_text and text on the basis of number of errors """
    # removing anti-cheat character from text (so we don't include it when comparing)
    text = text.replace("\u200e ", " ")
    error = 0
    text_lst = text.split()
    inp_lst = input_text.split()

    for i, c in enumerate(text_lst):
        for itr, cont in enumerate(c):
            try:
                if inp_lst[i][itr] == cont:
                    continue

                elif inp_lst[i][itr] != cont:
                    error += 1
            except IndexError:
                pass

    if len(input_text) > len(text):
        error += 2 * (len(input_text) - len(text))

    accuracy = ((len(input_text) - error) / len(text)) * 100

    if accuracy < 0:
        accuracy = 0.0
    return round(accuracy), error


def gross_wpm(input_text, total_time):
    """ returns gross_wpm(wpm without accounting for errors) formula: length of (input text x 60)/(5 x time_taken) """
    # Reasoning behind formula:
    # len(input_text) = characters per second, so len(input_text) * 60 gives us the characters per minute
    # Divide by 5 because the average word in English is 5 characters
    # Divide by time_taken to get the gross number of words per minute
    wpm = len(input_text) * 60 / (5 * total_time)
    return round(wpm)


def net_wpm(input_text, text, total_time):
    """ returns net_wpm(wpm accounting for errors) formula: (length of input_text - errors) x 60 / 5 x time_taken """
    errors = (accuracy(input_text, text))[1]
    wpm = ((len(input_text) - errors) * 60) / (total_time * 5)
    if wpm > 0:
        return round(wpm)
    else:
        return 0


# -------------------- Main Game Code --------------------
start_art = """
████████╗██╗   ██╗██████╗ ██╗███╗   ██╗ ██████╗     ███████╗██████╗ ███████╗███████╗██████╗ 
╚══██╔══╝╚██╗ ██╔╝██╔══██╗██║████╗  ██║██╔════╝     ██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗
   ██║    ╚████╔╝ ██████╔╝██║██╔██╗ ██║██║  ███╗    ███████╗██████╔╝█████╗  █████╗  ██║  ██║
   ██║     ╚██╔╝  ██╔═══╝ ██║██║╚██╗██║██║   ██║    ╚════██║██╔═══╝ ██╔══╝  ██╔══╝  ██║  ██║
   ██║      ██║   ██║     ██║██║ ╚████║╚██████╔╝    ███████║██║     ███████╗███████╗██████╔╝
   ╚═╝      ╚═╝   ╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚══════╝╚═╝     ╚══════╝╚══════╝╚═════╝ 
                            Brought to you by Debojyoti Mishra
\n
"""


def typing_speed(username):
    string = get_words()
    _string = "\u200e ".join(string)  # get string to be displayed, added zero width char to prevent cheating
    # Explanation: An invisible character is inserted into the randomly generated sentence. So, if the player decides
    # to cheat by copying and pasting the text instead of typing it, we can check for the presence of the invisible
    # character in their input and catch any attempts at cheating.
    print("Words:\n    " + _string)

    # timer
    sleep(1)
    start_time = datetime.now()
    user_input = input(" —> ")
    end_time = datetime.now()
    time_taken = round((end_time - start_time).total_seconds(), 1)  # calculate time-taken and rounding off

    if "\u200e " in user_input:  # anti-cheating mechanism (You can't copy and paste)
        print("Ha Ha, Nice Try but you can't do that")
        return

    netWPM = net_wpm(user_input, _string, time_taken)
    grossWPM = gross_wpm(user_input, time_taken)
    Accuracy, errors = accuracy(user_input, _string)

    # Printing results
    results = f"""
    Net WPM: {netWPM}     Accuracy: {Accuracy}%    Gross WPM: {grossWPM}
    Time Taken: {time_taken}     Errors: {errors}
    """
    print(results + "\n")


if __name__ == '__main__':
    print(start_art)
    username = input("Username: ").strip()

    while True:
        choice = input("    1.Play   2.Exit\n\t")
        clear()
        if choice.lower() in ["p", 'play', '1']:
            print(start_art, end='\n\n')
            typing_speed(username)

        elif choice.lower() in ["e", 'exit', '2']:
            break
