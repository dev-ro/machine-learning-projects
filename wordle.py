import random

# from pattern.en import pluralize, comparative, superlative, lexeme

# from english_words import get_english_words_set
# import pycountry

# # import nltk
# # nltk.download('words')
# from nltk.corpus import words
import json
import os
import sys

# country = pycountry.countries.lookup('de')
# print(country)

WORD_LENGTH = 8
FILENAME = "words.json"  # Name of the file to save the words

# Default word length
DEFAULT_WORD_LENGTH = 5
PREFIX = ""

# Check if a prefix argument is provided
if len(sys.argv) > 2:
    PREFIX = sys.argv[2].lower()
    print(f"Using prefix '{PREFIX}'.")

# Check if a word length argument is provided
if len(sys.argv) > 1:
    try:
        WORD_LENGTH = int(sys.argv[1])
    except ValueError:
        print(
            f"Invalid word length '{sys.argv[1]}'. Using default length {DEFAULT_WORD_LENGTH}."
        )
        WORD_LENGTH = DEFAULT_WORD_LENGTH
else:
    WORD_LENGTH = DEFAULT_WORD_LENGTH

# # Getting the set of all English words
# words = words.words()
# # lowercasing all the words
# words = [word.lower() for word in words]
# # set of all words
# words.extend(get_english_words_set(["web2"], lower=True))
# words = list(set(words))

# # countries = [country.name.lower() for country in pycountry.countries]
# # countries.extend([country.name.lower() for country in pycountry.subdivisions])
# # countries.extend([country.name.lower() for country in pycountry.languages])
# # countries.extend([country.name.lower() for country in pycountry.currencies])
# # countries.extend([country.name.lower() for country in pycountry.scripts])

# # words.extend(countries)


# def generate_words(words):
#     """
#     This function generates a list of words that are of length WORD_LENGTH.
#     """

#     inflected_words = []

#     for word in words:
#         try:
#             inflected_words.append(pluralize(word))
#         except:
#             pass
#         try:
#             inflected_words.append(comparative(word))
#         except:
#             pass
#         try:
#             inflected_words.append(superlative(word))
#         except:
#             pass
#         try:
#             inflected_words.extend(lexeme(word))
#         except:
#             pass

#     words.extend(inflected_words)


#     # Filter the words to only include words of length WORD_LENGTH
#     # words = [word for word in words if len(word) == WORD_LENGTH]

#     # remove words that have a space in them
#     words = [word for word in words if " " not in word]

#     words.extend(countries)
#     return list(set(words))


# def load_or_generate_words(filename, words=words):
#     """Load words from a file if it exists, otherwise generate and save them."""
#     if os.path.exists(filename):
#         print(f"Loading words from {filename}...\n")
#         with open(filename, "r") as file:
#             return json.load(file)
#     else:
#         print("Generating words...")
#         words = generate_words(words)
#         words.sort()
#         with open(filename, "w") as file:
#             json.dump(words, file)
#         return words

# https://github.com/dwyl/english-words


def load_words(filename):
    """Load words from a file if it exists, otherwise print error."""
    if os.path.exists(filename):
        print(f"Loading words from {filename}...\n")
        with open(filename, "r") as file:
            return json.load(file)
    else:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)


words = load_words(FILENAME)

# convert dictionary to list
# words = list(words.keys())
temp_words = words

if PREFIX:
    words = [
        word for word in words if word.startswith(PREFIX) and len(word) == WORD_LENGTH
    ]
else:
    words = [word for word in words if len(word) == WORD_LENGTH]

# This code is designed to "cheat" a word guessing game
# The user inputs character feedback which helps refine the possible set of words


def is_good_guess(word):
    """
    This function checks if the user's guess is valid.
    First it checks if the guess is the same length as WORD_LENGTH
    Then it checks if the guess is a feedback response of 'g', 'y', and/or 'b'
    """
    if len(word) != WORD_LENGTH and word.isalpha():
        print("\t⚠️ wrong guess length")
        return False
    if all(char in "gyb" for char in word):
        print("\t⚠️ enter a guess here, not feedback")
        return False
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
                feedback == "b"
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
        elif feedback == "b":
            # Exclude words where letter count in the word exceeds allowed 'g' and 'y' counts
            words = [
                word
                for word in words
                if word.count(letter)
                <= (correct_counts[letter] + present_counts[letter])
            ]

    return words

# based on oxford 1995 study of common letters in English words
letter_scores = {
    "e": 10.0,
    "a": 6.865,
    "r": 5.8586,
    "i": 5.8123,
    "o": 5.3727,
    "t": 5.1298,
    "n": 4.7827,
    "s": 3.73,
    "l": 3.4408,
    "c": 2.3419,
    "u": 1.2892,
    "d": 1.0,
}


def find_varying_positions(words):
    # Assuming all words are of the same length
    if not words:
        return {}

    word_length = len(words[0])
    varying_positions = {i: set() for i in range(word_length)}

    for word in words:
        for i, letter in enumerate(word):
            varying_positions[i].add(letter)

    # Filter out positions that do not vary (where all letters are the same)
    varying_positions = {
        pos: letters for pos, letters in varying_positions.items() if len(letters) > 1
    }

    return varying_positions


def collect_varying_letters(varying_positions):
    # Collect all unique letters from varying positions
    unique_varying_letters = set()
    for letters in varying_positions.values():
        unique_varying_letters |= letters  # Union of sets to collect unique letters from all positions with varying letters

    return "".join(sorted(unique_varying_letters))


### Example Usage
# words = ["gaging", "gaming", "gaping", "gazing", "yawing", "japing", "jawing",
#          "maying", "mawing", "mazing", "naging", "naming", "paging", "paying",
#          "paving", "pawing", "waging", "waying", "waning", "waving", "waxing"]
# varying_positions = find_varying_positions(words)
# unique_varying_letters = collect_varying_letters(varying_positions)
# print(f"Unique Varying Letters: {unique_varying_letters}")


def find_filler_words(words, letters):
    """
    Find filler words that contain the highest combination of the specified letters,
    without counting double letters more than once.
    """
    # Filter words that contain any of the specified letters
    filtered_words = [
        word
        for word in words
        if any(letter in word for letter in letters) and len(word) == WORD_LENGTH
    ]

    # Score words based on the presence of unique specified letters
    scored_words = [
        (word, sum(1 for letter in set(letters) if letter in word))
        for word in filtered_words
    ]

    # Sort words by their score in descending order to get words with the most specified letters first
    scored_words.sort(key=lambda x: x[1], reverse=True)

    # Return the top 5 words with the highest scores
    return [word for word, score in scored_words][:5]


def prompt_for_filler_letters():
    """
    Prompt the user to enter letters for searching filler words.
    """
    print("Enter letters to search for filler words (e.g., 'bhptw'):")
    letters = input().strip().lower()
    # You may want to add validation to ensure input is only letters
    return letters


def calculate_word_score(word):
    """
    Calculate a score for a word based on the presence of common letters.
    Each letter contributes its score to the word's total score.
    """
    return sum(letter_scores.get(letter, 0) for letter in set(word))


# Update the recommend function to return a list of recommendations
def recommend(words, n=5):
    """
    Recommend up to n guesses based on the possible set of words.
    Prioritize words that have a high score based on letter commonality and variety.
    """
    scored_words = [(word, calculate_word_score(word)) for word in words]
    # sort by score in descending order
    scored_words.sort(key=lambda x: x[1], reverse=True)
    recommendations = [word for word, score in scored_words[:n]]
    return recommendations


def get_guess():
    """
    This function prompts the user to enter their guess and the corresponding feedback.
    """
    # The user manually selects a guess
    recommended_guesses = recommend(words, 5)  # Get up to 5 recommendations
    print("Recommended guesses:")
    for i, guess in enumerate(recommended_guesses, 1):
        print(f"{i}. {guess}")
    print("Enter your guess, or choose 1-5 from the recommendations, or 0 for fillers:")

    guess = ""
    while not guess:
        user_input = input().strip().lower()

        if user_input == "0":
            letters = prompt_for_filler_letters()
            filler_words = find_filler_words(temp_words, letters)
            print(f"Filler words for letters '{letters}': {', '.join(filler_words)}")
        if user_input.isdigit() and 1 <= int(user_input) <= len(recommended_guesses):
            guess = recommended_guesses[int(user_input) - 1]
        if is_good_guess(user_input) and user_input.isalpha():
            guess = user_input

    # Prompt the user to enter the result of their guess
    print(f"put the result of '{guess}'")
    result = ""
    while not result:
        result = input("enter the result of your guess: ")
        result = result.strip().lower()

        if len(result) != WORD_LENGTH:
            print("\t⚠️ wrong result length ⚠️")
            result = ""

        # if the result contains invalid characters, it's not a valid result
        if not all(char in "gyb" for char in result):
            print("\t⚠️ use only 'gyb' for result ⚠️")
            result = ""
    # Convert the guess and the result to a list of tuples
    return list(zip(guess, result))


def keep_playing(choice):
    """
    This function checks if the user wants to continue playing.
    """
    return True if "y" in choice else False


def pretty_print(words):
    """
    This function prints the words in a pretty format.
    """
    string = ""
    for i in range(0, len(words), 5):
        string = ", ".join(words)
    return string


def add_to_dictionary(word):
    """
    This function adds a word to the dictionary.
    """

    def check(word):
        """
        This function checks if the word is valid.
        """
        if len(word) != WORD_LENGTH:
            print(f"⚠️ word length must be {WORD_LENGTH} ⚠️")
            return False
        if not all(char.isalpha() for char in word):
            print("⚠️ word must contain only letters ⚠️")
            return False
        return True

    is_valid = check(word)

    while not is_valid:
        word = input("enter a valid word: ")
        is_valid = check(word)

    # Add the word to the dictionary
    word = word.strip().lower()
    temp_words.append(word)
    with open(FILENAME, "w") as file:
        json.dump(temp_words, file)
    print(f"added '{word}' to the dictionary\n")


# Initialize the guess counter and user choice
guess_count = 1
choice = "yes"
has_word = ""

# Keep playing as long as the user wants to continue
while keep_playing(choice):
    # Filter the possible words based on the user's guess and feedback
    words = reverse_filter(words, get_guess())
    guess_count += 1
    if len(words) > 30:
        print(f"{len(words)} remaining")
    # If the number of possible words is small, print them out
    if len(words) <= 30:
        p_words = pretty_print(words)
        print(f"🔥 {len(words)} remaining: {p_words}🔥")
    # If there's only one possible word left, we've found the answer
    if len(words) == 1:
        print("✅ found it! ✅\n")
    # If there are no possible words left, it's not in the dictionary
    if len(words) == 0:
        print("🚫 word not in this dictionary 🚫\n")
    if len(words) <= 1:
        has_word = input("was your word in the dictionary? (y/n): ")
        if "n" in has_word:
            answer = input("what was the answer? ")
            add_to_dictionary(answer)
            break
        else:
            print("🎉 yay! 🎉")
            break
