"""analyzes the words.json file. 
It reads the file and counts the number of words in the file.
It then gives a summary of how many n-length words are in the file."""

import json
from collections import Counter
file_path = "words.json"

def analyze(file_path):
    with open(file_path, 'r') as file:
        words = json.load(file)
    word_count = len(words)
    word_lengths = [len(word) for word in words]
    word_length_count = Counter(word_lengths)
    print(f"Total number of words: {word_count}")
    print("Word length count:")
    
    # sort by word length
    for length, count in sorted(word_length_count.items()):
        print(f"{length}-letter words: {count}")

    # make a dictionary of lists
    word_dict = {length: [] for length in word_length_count.keys()}
    for word in words:
        if len(word) >= 20:
            word_dict[len(word)].append(word)

    print("Words with 25 or more letters:")
    for length, words in sorted(word_dict.items()):
        if length >= 20:
            print(f"{length}-letter words: {words}")

analyze(file_path)
