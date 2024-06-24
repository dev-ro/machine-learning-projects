import argparse
import json
import itertools

def load_words_from_json(file_path):
    with open(file_path, 'r') as file:
        words = json.load(file)
    return words



def find_matching_words(characters, words):
    matching_words = set()
    words_set = set(words)  # Convert list to set for O(1) lookups
    all_perms = set()  # To store unique permutations
    
    def can_form_word(word, characters):
        # Create a set of unique characters from the input for faster lookup
        unique_chars = set(characters)

        # Check if every character in the word is in the set of input characters
        for letter in set(word):
            if letter not in unique_chars:
                return False
        return True

    filtered_words = [
        word
        for word in words
        if can_form_word(word, characters)
    ]

    # sort by length of word
    filtered_words.sort(key=len, reverse=True)
    return filtered_words

def pretty_print(words):
    """ Print the words in a pretty format as tab separated 
    columns based on length of the longest word"""
    if not words:
        print("No matching words found")
        return

    max_length = max(len(word) for word in words)
    num_columns = 80 // (max_length + 2)
    words = [f"{word:<{max_length}}" for word in words]

    for i in range(0, len(words), num_columns):
        print("\t".join(words[i:i+num_columns]))

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Find words that can be formed from a list of characters.')
    parser.add_argument('starting_letter', nargs='?', help='The starting letter of words to filter by', default=None)
    args = parser.parse_args()
    
    # Load words from JSON
    file_path = 'words.json'
    words = load_words_from_json(file_path)

    words = [word for word in words if len(word) >= 4]
    
    # Filter words by starting letter if specified
    if args.starting_letter:
        words = [word for word in words if args.starting_letter in word]

    # Input characters from the user
    characters = list(input("Enter the list of characters (without spaces): "))
    
    # Find matching words
    matching_words = find_matching_words(characters, words)
    
    pretty_print(matching_words)

if __name__ == "__main__":
    main()