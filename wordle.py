import random
from english_words import get_english_words_set

# Getting the set of all English words
all_words = get_english_words_set(["web2"], lower=True)
WORD_LENGTH = 5


# Building the list of words with the specified length
words = [word for word in all_words if len(word) == WORD_LENGTH]


# This code is designed to "cheat" a word guessing game
# The user inputs character feedback which helps refine the possible set of words


def is_good_guess(word):
    """
    This function checks if the user's guess is valid.
    """
    return True


def reverse_filter(words, guess):
    # Dictionary to hold counts of 'g' and 'y' for each letter
    correct_counts = {letter: 0 for letter, _ in guess}
    present_counts = {letter: 0 for letter, _ in guess}

    # First pass to count 'g' and 'y'
    for letter, feedback in guess:
        if feedback == "g":
            correct_counts[letter] += 1
        elif feedback == "y":
            present_counts[letter] += 1

    # Filter words based on 'g' and 'y' counts first
    def filter_based_on_feedback(word):
        word_letter_counts = {letter: word.count(letter) for letter, _ in guess}
        for letter, feedback in guess:
            if feedback == "g" and word_letter_counts[letter] < correct_counts[letter]:
                return False
            if feedback == "y" and (
                letter not in word
                or word_letter_counts[letter] <= correct_counts[letter]
            ):
                return False
            if (
                feedback == "x"
                and letter in word
                and word_letter_counts[letter]
                > (correct_counts[letter] + present_counts[letter])
            ):
                return False
        return True

    words = [word for word in words if filter_based_on_feedback(word)]

    # Detailed filtering for each letter based on position and feedback
    for i in range(len(guess)):
        letter, feedback = guess[i]

        if feedback == "g":
            words = [word for word in words if word[i] == letter]
        elif feedback == "y":
            words = [word for word in words if letter in word and word[i] != letter]
        elif feedback == "x":
            # Exclude words where letter count in the word exceeds allowed 'g' and 'y' counts
            words = [
                word
                for word in words
                if word.count(letter)
                <= (correct_counts[letter] + present_counts[letter])
            ]

    return words


def recommend(words):
    """
    This function recommends a guess based on the possible set of words.

    The function selects a word that has only distinct characters if possible.
    If there are no words with distinct characters, the function selects a word at random.

    The function also selects a word at random if the number of possible words is greater than 3 and the guess count is
    greater than 3.
    """
    # Unique words are the words that have only distinct characters
    unique_words = [word for word in words if len(set(word)) == len(word)]

    # Select the word to guess
    if guess_count == 1 and "soare" in words:
        guess = "soare"
    elif unique_words and guess_count <= 3:
        guess = random.choice(unique_words)
    else:
        guess = random.choice(words)

    print(f"\nrecommended_guess={guess}")
    return guess


def get_guess():
    """
    This function prompts the user to enter their guess and the corresponding feedback.
    """
    # The user manually selects a guess
    guess = ""
    while not guess:
        recommend(words)
        guess = input("enter the word you guessed: ")
        guess = guess.strip().lower()

    # The function automatically recommends a guess
    # guess = recommend(words)

    # Prompt the user to enter the result of their guess
    print(
        f"put the result of '{guess}' as one string like this: gyxxx to say green,yellow,grey,grey,grey"
    )
    result = ""
    while len(result) != WORD_LENGTH:
        result = input("enter the result of your guess: ")
        result = result.strip().lower()
        if len(result) != WORD_LENGTH:
            print("bad result input")
    # Convert the guess and the result to a list of tuples
    return list(zip(guess, result))


def keep_playing(choice):
    """
    This function checks if the user wants to continue playing.
    """
    return True if "y" in choice else False


# Initialize the guess counter and user choice
guess_count = 1
choice = "yes"

# Keep playing as long as the user wants to continue
while keep_playing(choice):
    # Filter the possible words based on the user's guess and feedback
    words = reverse_filter(words, get_guess())
    guess_count += 1
    print(f"words_size={len(words)}")
    # If the number of possible words is small, print them out
    if len(words) <= 300:
        print(f"possible_words={words}")
    # If there's only one possible word left, we've found the answer
    if len(words) <= 1:
        print("🎉HA! got em'! 🎉✌")
        break
    # Prompt the user if they want to continue playing
    # choice = input("continue? yes or no: ")
