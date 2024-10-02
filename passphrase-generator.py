import random
import argparse
import re

# Create a translation table for vowel replacement
vowel_replacements = str.maketrans('aeiou', '@31µ0')

def load_word_list(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while loading the word list: {e}")
        exit(1)

def replace_vowels(word):
    return word.translate(vowel_replacements)

def assess_strength(passphrase):
    length_score = len(passphrase) >= 12  # Length should be at least 12 characters
    upper_case = any(c.isupper() for c in passphrase)
    lower_case = any(c.islower() for c in passphrase)
    digits = any(c.isdigit() for c in passphrase)
    special_chars = any(c in '@#$%^&*()_+!~`' for c in passphrase)  # Define special characters

    # Count the number of character types present
    character_types = sum([length_score, upper_case, lower_case, digits, special_chars])

    # Determine strength based on character types
    if character_types == 0:
        return "Very Weak"
    elif character_types == 1:
        return "Weak"
    elif character_types == 2:
        return "Normal"
    elif character_types == 3:
        return "Strong"
    else:
        return "Very Strong"

def capitalize_random_characters(passphrase):
    total_chars = len(passphrase)
    max_capitalize = total_chars // 2  # Half of the total characters
    num_to_capitalize = random.randint(1, max_capitalize)  # At least 1, up to half

    # Convert passphrase to a list to modify it
    passphrase_list = list(passphrase)
    
    # Randomly select indices to capitalize
    indices_to_capitalize = random.sample(range(total_chars), num_to_capitalize)
    
    for index in indices_to_capitalize:
        passphrase_list[index] = passphrase_list[index].upper()  # Capitalize the character

    return ''.join(passphrase_list)  # Join the list back into a string

def generate_passphrase(word_list, num_words=4, use_special_chars=False):
    if num_words > len(word_list):
        raise ValueError("Not enough unique words in the list.")
    
    while True:
        selected_words = random.sample(word_list, num_words)
        
        # Randomly capitalize the first letter of each word
        passphrase_parts = [
            (word.capitalize() if random.choice([True, False]) else word)
            for word in selected_words
        ]
        
        # Determine how many words will have special characters replaced
        if use_special_chars:
            max_special_words = num_words // 2  # Maximum half of the selected words
            num_special_words = random.randint(1, max_special_words)  # At least 1 word
            
            # Randomly select which words to replace
            special_indices = random.sample(range(num_words), num_special_words)
            for index in special_indices:
                passphrase_parts[index] = replace_vowels(passphrase_parts[index])
        
        # Join the parts into a single passphrase
        passphrase = ' '.join(passphrase_parts)
        
        # Capitalize random characters in the passphrase
        passphrase = capitalize_random_characters(passphrase)
        
        # Validate passphrase length
        if len(passphrase) > 100:
            raise ValueError("The passphrase cannot exceed 100 characters.")
        if len(passphrase) > 10:  # Only check for minimum length
            return passphrase

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a secure passphrase.')
    parser.add_argument('num_words', type=int, nargs='?', help='Number of words in the passphrase')
    parser.add_argument('special_chars', type=str, nargs='?', default='false', 
                        help='Use special characters (true/false)')

    args = parser.parse_args()

    # Check if num_words is provided
    if args.num_words is None:
        parser.print_usage()
        print("Error: The number of words is required.")
        exit(1)

    try:
        # User Input Validation
        if args.num_words < 2:
            print("Error: Minimum words for the passphrase generated is 2.")
            parser.print_usage()
            exit(1)
        
        if args.num_words > 16:
            print("Error: The maximum number of words for the passphrase is 16.")
            parser.print_usage()
            exit(1)

        if args.num_words <= 0:
            print("Error: The number of words must be a positive integer.")
            parser.print_usage()
            exit(1)
        
        word_list = load_word_list('words-en.txt')  # Ensure this is in the same directory
        if args.num_words > len(word_list):
            print("Error: Not enough unique words in the list.")
            exit(1)
        
        # Convert special_chars argument to boolean
        if args.special_chars.lower() not in ['true', 'false']:
            print("Error: The special_chars argument must be 'true' or 'false'.")
            parser.print_usage()
            exit(1)
        
        use_special_chars = args.special_chars.lower() == 'true'
        
        passphrase = generate_passphrase(word_list, num_words=args.num_words, use_special_chars=use_special_chars)
        print("Generated Passphrase:", passphrase)

        # Assess the strength of the generated passphrase
        strength = assess_strength(passphrase)
        print(f"This passphrase is considered: {strength}")  # Updated print statement

    except ValueError as ve:
        print(f"Error: {ve}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)