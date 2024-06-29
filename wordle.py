import json
import os
import sys
from collections import Counter

WORD_LENGTH = None
FILENAME = "words.json"  # Name of the file to save the words

# Default word length
DEFAULT_WORD_LENGTH = 5
PREFIX = None

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


def load_words(filename):
    """Load words from a file if it exists, otherwise print error."""
    if os.path.exists(filename):
        print(f"Loading words from {filename}...\n")
        with open(filename, "r") as file:
            return json.load(file)
    else:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)


words = load_words(FILENAME)  # this list will be filtered down to the possible words
# use temp_words to store the full list of words. used for adding new words
temp_words = words

if PREFIX:
    words = [
        word for word in words if word.startswith(PREFIX) and len(word) == WORD_LENGTH
    ]
else:
    words = [word for word in words if len(word) == WORD_LENGTH]


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


def letter_frequency(words=temp_words, length=WORD_LENGTH, prefix=PREFIX):
    """
    Calculates the frequency of letters in words of a specified length and
    prefix. This is more efficient than the Monte Carlo simulation to find
    the best starting word, more efficient than calculating the frequency
    of all letters in the dictionary, and more accurate than referring to
    studies on letter frequency in languages, which might be based on real
    text data, not the dictionary.

    The function returns a dictionary of letter frequencies in descending order
    that you pass to the normalize_frequencies function.
    """

    # Filter words by the specified length and prefix if provided
    filtered_words = [
        word
        for word in words
        if len(word) == length and (prefix is None or word.startswith(prefix))
    ]

    # Remove the prefix from the filtered words for frequency calculation
    if prefix:
        filtered_words = [word[len(prefix) :] for word in filtered_words]

    # Join all the filtered words into a single string
    all_letters = "".join(filtered_words)

    # Calculate the frequency of each letter
    frequency = Counter(all_letters)

    # Calculate the total number of letters
    total_letters = sum(frequency.values())

    # Convert the frequency to percentage
    percentage_frequency = {
        letter: (count / total_letters) * 100 for letter, count in frequency.items()
    }

    # Sort the frequencies in descending order
    sorted_percentage_frequency = dict(
        sorted(percentage_frequency.items(), key=lambda item: item[1], reverse=True)
    )

    return sorted_percentage_frequency


def normalize_frequencies(frequencies=letter_frequency()):
    """
    Normalize the frequencies of letters to a scale of 0 to 10.
    Returns a dictionary of normalized frequencies saved as "letter_scores".

    The normalization formula is:
    normalized_value = ((value - min_value) / (max_value - min_value)) * 10

    The normalized frequencies are used to score words based on the presence
    of common letters. The score is calculated by summing the normalized
    frequencies of letters in the word.
    """

    max_freq = max(frequencies.values())
    min_freq = min(frequencies.values())

    # Normalize the frequencies
    normalized_frequencies = {
        letter: ((value - min_freq) / (max_freq - min_freq)) * 10
        for letter, value in frequencies.items()
    }

    return normalized_frequencies


letter_scores = normalize_frequencies()


def find_varying_positions(words):
    """
    Find positions in words where letters vary among the words.
    For example, in the words 'gaming' and 'japing',
    the letters vary at the first and third position.
    """
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
    """
    Collect all unique letters from varying positions.
    For example 'gaming' and 'japing' would return 'gjmp'.
    """
    unique_varying_letters = set()
    for letters in varying_positions.values():
        unique_varying_letters |= letters  # Union of sets to collect unique letters from all positions with varying letters

    return "".join(sorted(unique_varying_letters))


def find_filler_words(words, letters, n=6):
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

    # Return the top n words with the highest scores
    return [word for word, score in scored_words][:n]


def prompt_for_filler_letters():
    """
    Prompt the user to enter letters for searching filler words.
    """
    print("Enter letters to search for filler words (e.g., 'bhptw'):")
    letters = input().strip().lower()

    # ensure input is only letters
    while not letters.isalpha():
        print("\t⚠️ use only letters ⚠️")
        letters = input().strip().lower()

    return letters


def calculate_word_score(word, count_duplicates=False):
    """
    Calculate a score for a word based on the presence of common letters.
    Each letter contributes its score to the word's total score.
    """
    if guess_count > 2:
        count_duplicates = True

    if count_duplicates:
        return sum(letter_scores.get(letter, 0) for letter in word)
    else:
        return sum(letter_scores.get(letter, 0) for letter in set(word))


# Update the recommend function to return a list of recommendations
def recommend(words, n=5, length=WORD_LENGTH, prefix=PREFIX):
    """
    Recommend up to n guesses based on the possible set of words.
    Prioritize words that have a high score based on letter commonality and variety.
    """
    filtered_words = [
        word
        for word in words
        if len(word) == length and (prefix is None or word.startswith(prefix))
    ]
    scored_words = [(word, calculate_word_score(word)) for word in filtered_words]

    # Sort by score in descending order
    scored_words.sort(key=lambda x: x[1], reverse=True)

    return scored_words[:n]


def get_guess(n=5):
    """
    This function prompts the user to enter their guess and the corresponding feedback.
    """
    # The user manually selects a guess
    recommended_guesses = recommend(words, n)  # Get up to n recommendations
    print("Recommended guesses:")
    for i, (guess, score) in enumerate(recommended_guesses, 1):
        print(f"{i}. {guess} - {round(score, 2)}")
    print(
        f"\nEnter your guess, or choose 1-{n} from the recommendations, or 0 for fillers:"
    )

    guess = ""
    while not guess:
        user_input = input().strip().lower()

        if user_input == "0":
            letters = prompt_for_filler_letters()
            filler_words = find_filler_words(temp_words, letters)
            print(f"Filler words for letters '{letters}': {', '.join(filler_words)}")

        if user_input.isdigit() and 1 <= int(user_input) <= len(recommended_guesses):
            guess = recommended_guesses[int(user_input) - 1][0]

        if is_good_guess(user_input) and user_input.isalpha():
            guess = user_input

    result = ""
    while not result:
        result = input(f"enter the result of your guess, '{guess}': ")
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

    # we use temp_words here to get the full list of words
    temp_words.append(word)
    with open(FILENAME, "w") as file:
        json.dump(temp_words, file)
    print(f"added '{word}' to the dictionary\n")


guess_count = 1
choice = "yes"
has_word = ""

# Keep playing as long as the user wants to continue
while keep_playing(choice):

    # Filter the possible words based on the user's guess and feedback
    n = min(len(words), 9)  # Limit the number of recommendations to 9
    words = reverse_filter(words, get_guess(n))
    guess_count += 1  # Increment the guess count for scoring

    if len(words) > 30:
        print(f"{len(words)} remaining")

    # If the number of possible words is small, print them out
    if len(words) <= 30:
        p_words = pretty_print(words)
        print(f"\n🔥 {len(words)} remaining: {p_words} 🔥\n")

    # If there's only one possible word left, we've likely found the answer
    if len(words) == 1:
        print("✅ found it! ✅\n")

    # If there are no possible words left, it's not in the dictionary
    if len(words) == 0:
        print("🚫 word not in this dictionary 🚫\n")

    # If our dictionary is missing a word, then add it
    if len(words) <= 1:
        has_word = input("was your word in the dictionary? (y/n): ")
        if "n" in has_word:
            answer = input("what was the answer? ")
            add_to_dictionary(answer)
            break
        else:
            print("🎉 yay! 🎉")
            break
