import random
import argparse
import re
import glob

# Color codes
RED = "\033[31m"
ORANGE = "\033[33m"
GREEN = "\033[32m"
BLUE = "\033[34m"
WHITE = "\033[37m"
RESET = "\033[0m"

# Create a translation table for vowel replacement
vowel_replacements = str.maketrans('aeiou', '@31µ0')

def load_word_list(language):
    file_path = f'words-{language}.txt'
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"{RED}Error: The file '{file_path}' was not found.{RESET}")
        exit(1)
    except Exception as e:
        print(f"{RED}An unexpected error occurred while loading the word list: {e}{RESET}")
        exit(1)

def replace_vowels(word):
    return word.translate(vowel_replacements)

def assess_strength(passphrase, language='en'):
    length_score = len(passphrase) >= 12  # Length should be at least 12 characters
    upper_case = any(c.isupper() for c in passphrase)
    lower_case = any(c.islower() for c in passphrase)
    digits = any(c.isdigit() for c in passphrase)
    special_chars = any(c in '@#$%^&*()_+!~`' for c in passphrase)  # Define special characters

    # Count the number of character types present
    character_types = sum([length_score, upper_case, lower_case, digits, special_chars])

    # Determine strength based on character types
    if character_types == 0:
        return "Muy Débil" if language == 'es' else "Very Weak"
    elif character_types == 1:
        return "Débil" if language == 'es' else "Weak"
    elif character_types == 2:
        return "Normal"  # No translation needed
    elif character_types == 3:
        return "Fuerte" if language == 'es' else "Strong"
    else:
        return "Muy Fuerte" if language == 'es' else "Very Strong"

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
        if len(passphrase) > 127:  # Updated max length to 127 characters
            raise ValueError("The passphrase cannot exceed 127 characters.")
        if len(passphrase) > 10:  # Only check for minimum length
            return passphrase

def get_language(args):
    """Get the first valid language argument from the command line."""
    languages = ['es', 'en']
    for arg in args:
        if arg in languages:
            return arg
    return 'en'  # Default to English if no valid language is found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a secure passphrase.')
    parser.add_argument('args', nargs='*', help='Arguments for number of words, special characters, and language')

    args = parser.parse_args().args

    # Initialize variables
    num_words = None
    use_special_chars = False
    language = None

    # Process arguments
    for arg in args:
        if arg.isdigit():
            num_words = int(arg)
        elif arg.lower() in ['true', 'false']:
            use_special_chars = arg.lower() == 'true'
        elif arg in ['es', 'en']:
            if language is None:  # Only set the language if it hasn't been set yet
                language = arg

    # Default to 2 words if no valid integer is detected
    if num_words is None:
        num_words = 2

    try:
        # User Input Validation
        if num_words < 2:
            print(f"{RED}Error: Minimum words for the passphrase generated is 2.{RESET}")
            exit(1)
        
        if num_words > 16:
            print(f"{RED}Error: The maximum number of words for the passphrase is 16.{RESET}")
            exit(1)

        word_list = load_word_list(language if language else 'en')  # Default to English if no language is specified
        if num_words > len(word_list):
            print(f"{RED}Error: Not enough unique words in the list.{RESET}")
            exit(1)
        
        passphrase = generate_passphrase(word_list, num_words=num_words, use_special_chars=use_special_chars)
        
        # Output based on language
        if language == 'es':
            print(f"{BLUE}Fraseeclave Generada: {WHITE}{passphrase}{RESET}")
            strength = assess_strength(passphrase, language='es')
            print(f"{BLUE}Esta fraseclave se considera: {strength}{RESET}")
        else:
            print(f"{BLUE}Generated Passphrase: {WHITE}{passphrase}{RESET}")
            strength = assess_strength(passphrase, language='en')
            print(f"{BLUE}This passphrase is considered: {strength}{RESET}")

    except ValueError as ve:
        print(f"{RED}Error: {ve}{RESET}")
        exit(1)
    except Exception as e:
        print(f"{RED}An unexpected error occurred: {e}{RESET}")
        exit(1)