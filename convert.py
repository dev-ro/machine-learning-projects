"""convert list of words from .txt file to .json dictionary"""
import json

# text format is utf-8
# json format is utf-8

# read the file
def convert_to_json(file_path):
    words = []
    with open(file_path, 'r', encoding='utf-16') as file:
        for line in file:
            words.append(line.strip())
    return json.dumps(words)

def main():
    file_path = 'spanish-words.txt'
    words = convert_to_json(file_path)
    with open('spanish-words.json', 'w') as file:
        file.write(words)

if __name__ == '__main__':
    main()

