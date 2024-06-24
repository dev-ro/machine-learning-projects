import json

file_path = "words.json"

def convert_to_txt(file_path):
    with open(file_path, 'r') as file:
        words = json.load(file)
    with open('words.txt', 'w') as file:
        for word in words:
            file.write(f"{word}\n")

convert_to_txt(file_path)

