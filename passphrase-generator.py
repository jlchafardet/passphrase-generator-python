import random
import argparse
import re

def load_word_list(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def replace_vowels(word, use_special_chars):
    if not use_special_chars:
        return word
    replacements = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 'u': 'µ'}
    return ''.join(replacements.get(char, char) for char in word)

def generate_passphrase(word_list, num_words=4, use_special_chars=False):
    if num_words > len(word_list):
        raise ValueError("Not enough unique words in the list.")
    
    selected_words = random.sample(word_list, num_words)
    
    # Randomly capitalize the first letter of each word
    passphrase = ' '.join(
        word.capitalize() if random.choice([True, False]) else word
        for word in selected_words
    )
    
    # Replace vowels with special characters if specified
    passphrase = ' '.join(replace_vowels(word, use_special_chars) for word in passphrase.split())
    
    return passphrase

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a secure passphrase.')
    parser.add_argument('num_words', type=int, help='Number of words in the passphrase')
    parser.add_argument('special_chars', type=str, nargs='?', default='false', 
                        help='Use special characters (true/false)')

    args = parser.parse_args()
    
    # Convert special_chars argument to boolean
    use_special_chars = args.special_chars.lower() == 'true'
    
    word_list = load_word_list('words-en.txt')  # Ensure this is in the same directory
    passphrase = generate_passphrase(word_list, num_words=args.num_words, use_special_chars=use_special_chars)
    print("Generated Passphrase:", passphrase)
