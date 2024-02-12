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


letter_scores = {
    "r": 1.5,
    "s": 1.1,
    "t": 1.3,
    "l": 1,
    "n": 1.2,
    "e": 2,
    "a": 1.8,
    "o": 1.3,
    "i": 1.5,
    "c": 0.8,
    "j": -1,
    "q": -1,
    "x": -1,
    "z": -1.5,
}


def calculate_word_score(word):
    """
    Calculate a score for a word based on the presence of common letters.
    Each letter contributes its score to the word's total score.
    """
    return sum(letter_scores.get(letter, 0) for letter in set(word))


def recommend(words):
    """
    Recommend a guess based on the possible set of words.
    Prioritize words that have a high score based on letter commonality and variety.
    """
    if guess_count <= 3:
        # Score words based on their letters
        scored_words = [(word, calculate_word_score(word)) for word in words]
        # Sort words by their score in descending order
        scored_words.sort(key=lambda x: x[1], reverse=True)
        # Prefer words with the highest score
        high_score_words = [
            word for word, score in scored_words if score == scored_words[0][1]
        ]
        guess = random.choice(high_score_words)
    else:
        guess = random.choice(words)

    print(f"\n🤔 recommended_guess = '{guess}' 🤔")
    return guess


# def recommend(words):
#     """
#     This function recommends a guess based on the possible set of words.

#     The function selects a word that has only distinct characters if possible.
#     If there are no words with distinct characters, the function selects a word at random.

#     The function also selects a word at random if the number of possible words is greater than 3 and the guess count is
#     greater than 3.
#     """
#     # Unique words are the words that have only distinct characters
#     unique_words = [word for word in words if len(set(word)) == len(word)]

#     # Select the word to guess
#     if guess_count == 1 and "soare" in words:
#         guess = "soare"
#     elif unique_words and guess_count <= 3:
#         guess = random.choice(unique_words)
#     else:
#         guess = random.choice(words)

#     print(f"\n🤔 recommended_guess = '{guess}' 🤔")
#     return guess


def get_guess():
    """
    This function prompts the user to enter their guess and the corresponding feedback.
    """
    # The user manually selects a guess
    guess = ""
    while not guess:
        recommended_guess = recommend(words)
        guess = input("enter the word you guessed (r for recommended): ")
        guess = guess.strip().lower()
        if guess == "":
            continue
        # if guess contains no vowels, it's not a valid word
        if not any(vowel in guess for vowel in "aeiou") and guess != "r":
            print("\t⚠️  guess here, not result ⚠️")
            guess = ""
        # if guess == "r" then the user wants the recommended guess
        if guess == "r":
            guess = recommended_guess

    # The function automatically recommends a guess
    # guess = recommend(words)

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
