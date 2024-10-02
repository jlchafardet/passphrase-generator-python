import secrets  # Import the secrets module for generating secure random numbers
import argparse  # Import argparse to handle command-line arguments
import re  # Import regular expressions for string manipulation
import glob  # Import glob for file path matching
import random  # Import random for sampling functions

# Define color codes for terminal output
RED = "\033[31m"  # Red color for error messages
ORANGE = "\033[33m"  # Orange color for warnings
GREEN = "\033[32m"  # Green color for success messages
BLUE = "\033[34m"  # Blue color for informational messages
WHITE = "\033[37m"  # White color for normal text
RESET = "\033[0m"  # Reset color to default

# Create a translation table for replacing vowels with special characters
vowel_replacements = str.maketrans('aeiou', '@31µ0')

def load_word_list(language):
    """
    Load a list of words from a file based on the specified language.

    Parameters:
    language (str): The language code (e.g., 'en' for English, 'es' for Spanish).

    Returns:
    list: A list of words loaded from the specified file.

    Raises:
    FileNotFoundError: If the specified word list file does not exist.
    Exception: For any other unexpected errors that occur during file reading.
    """
    file_path = f'words-{language}.txt'  # Construct the file path based on the language
    try:
        with open(file_path, 'r') as file:  # Open the file in read mode
            return [line.strip() for line in file.readlines()]  # Read lines and remove whitespace
    except FileNotFoundError:
        print(f"{RED}Error: The file '{file_path}' was not found.{RESET}")  # Print error message if file not found
        exit(1)  # Exit the program with an error code
    except Exception as e:
        print(f"{RED}An unexpected error occurred while loading the word list: {e}{RESET}")  # Print any other errors
        exit(1)  # Exit the program with an error code

def replace_vowels(word):
    # Create a translation table for replacing vowels with special characters
    return word.translate(str.maketrans('aeio', '@310'))  # Exclude 'u' from replacement

def assess_strength(passphrase, language='en'):
    """
    Assess the strength of a given passphrase based on various criteria.

    Parameters:
    passphrase (str): The passphrase to be assessed.
    language (str): The language for output messages (default is English).

    Returns:
    str: A string indicating the strength of the passphrase.
    """
    length_score = len(passphrase) >= 12  # Length should be at least 12 characters
    upper_case = any(c.isupper() for c in passphrase)  # Check for uppercase letters
    lower_case = any(c.islower() for c in passphrase)  # Check for lowercase letters
    digits = any(c.isdigit() for c in passphrase)  # Check for digits
    special_chars = any(c in '@#$%^&*()_+!~`' for c in passphrase)  # Check for special characters

    # Count the number of character types present in the passphrase
    character_types = sum([length_score, upper_case, lower_case, digits, special_chars])

    # Determine strength based on the number of character types
    if len(passphrase) < 8:  # Adjust minimum length for 'Very Weak'
        return "Very Weak" if language == 'es' else "Very Weak"
    elif character_types == 1:
        return "Weak" if language == 'es' else "Weak"
    elif character_types == 2:
        return "Normal"  # Normal strength
    elif character_types == 3:
        return "Strong" if language == 'es' else "Strong"
    else:
        return "Very Strong" if language == 'es' else "Very Strong"

def capitalize_random_characters(passphrase):
    """
    Randomly capitalize characters in the passphrase to enhance its strength.

    Parameters:
    passphrase (str): The passphrase in which characters will be capitalized.

    Returns:
    str: The passphrase with randomly capitalized characters.
    """
    total_chars = len(passphrase)  # Get the total number of characters in the passphrase
    max_capitalize = total_chars // 2  # Determine the maximum number of characters to capitalize (up to half)
    num_to_capitalize = secrets.randbelow(max_capitalize) + 1  # At least 1 character will be capitalized

    # Convert the passphrase to a list to modify it
    passphrase_list = list(passphrase)
    
    # Randomly select indices to capitalize
    indices_to_capitalize = random.sample(range(total_chars), num_to_capitalize)
    
    for index in indices_to_capitalize:
        passphrase_list[index] = passphrase_list[index].upper()  # Capitalize the character at the selected index

    return ''.join(passphrase_list)  # Join the list back into a string and return it

def generate_passphrase(word_list, num_words=4, use_special_chars=False):
    """
    Generate a secure passphrase using a list of words.

    Parameters:
    word_list (list): A list of words to use for generating the passphrase.
    num_words (int): The number of words to include in the passphrase (default is 4).
    use_special_chars (bool): Whether to include special character replacements (default is False).

    Returns:
    str: The generated passphrase.

    Raises:
    ValueError: If the number of words requested exceeds the available unique words.
    """
    if num_words > len(word_list):
        raise ValueError("Not enough unique words in the list.")  # Raise an error if not enough words are available
    
    while True:
        selected_words = random.sample(word_list, num_words)  # Securely select random words from the list
        
        # Randomly capitalize the first letter of each word
        passphrase_parts = [
            (word.capitalize() if secrets.randbelow(2) else word)  # Randomly decide to capitalize
            for word in selected_words
        ]
        
        # Determine how many words will have special characters replaced
        if use_special_chars:
            max_special_words = num_words // 2  # Maximum half of the selected words can have special characters
            num_special_words = secrets.randbelow(max_special_words) + 1  # At least 1 word will have special characters
            
            # Randomly select which words to replace with special characters
            special_indices = random.sample(range(num_words), num_special_words)
            for index in special_indices:
                passphrase_parts[index] = replace_vowels(passphrase_parts[index])  # Replace vowels in the selected words
        
        # Join the parts into a single passphrase
        passphrase = ' '.join(passphrase_parts)
        
        # Capitalize random characters in the passphrase
        passphrase = capitalize_random_characters(passphrase)
        
        # Validate passphrase length
        if len(passphrase) > 127:  # Ensure the passphrase does not exceed 127 characters
            raise ValueError("The passphrase cannot exceed 127 characters.")
        if len(passphrase) > 10:  # Ensure the passphrase is at least 10 characters long
            return passphrase  # Return the generated passphrase

def get_language(args):
    """
    Get the first valid language argument from the command line.

    Parameters:
    args (list): The list of command-line arguments.

    Returns:
    str: The first valid language code found in the arguments, or 'en' if none is found.
    """
    languages = ['es', 'en']  # List of supported languages
    for arg in args:
        if arg in languages:
            return arg  # Return the first valid language found
    return 'en'  # Default to English if no valid language is found

if __name__ == "__main__":
    # Create an argument parser to handle command-line input
    parser = argparse.ArgumentParser(description='Generate a secure passphrase.')
    parser.add_argument('args', nargs='*', help='Arguments for number of words, special characters, and language')

    args = parser.parse_args().args  # Parse the command-line arguments

    # Initialize variables for user input
    num_words = None  # Number of words for the passphrase
    use_special_chars = False  # Flag for using special characters
    language = None  # Language for output messages

    # Process command-line arguments
    for arg in args:
        if arg.isdigit():
            num_words = int(arg)  # Convert the argument to an integer if it's a digit
        elif arg.lower() in ['true', 'false']:
            use_special_chars = arg.lower() == 'true'  # Set the flag based on the argument
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
            exit(1)  # Exit if the number of words is less than 2
        
        if num_words > 16:
            print(f"{RED}Error: The maximum number of words for the passphrase is 16.{RESET}")
            exit(1)  # Exit if the number of words exceeds 16

        # Load the appropriate word list based on the specified language
        word_list = load_word_list(language if language else 'en')  # Default to English if no language is specified
        if num_words > len(word_list):
            print(f"{RED}Error: Not enough unique words in the list.{RESET}")
            exit(1)  # Exit if there are not enough unique words
        
        # Generate the passphrase
        passphrase = generate_passphrase(word_list, num_words=num_words, use_special_chars=use_special_chars)
        
        # Output based on language
        if language == 'es':
            print(f"{BLUE}Fraseclave Generada: {WHITE}{passphrase}{RESET}")  # Output in Spanish
            strength = assess_strength(passphrase, language='es')  # Assess strength in Spanish
            print(f"{BLUE}Esta fraseclave se considera: {strength}{RESET}")  # Output strength in Spanish
        else:
            print(f"{BLUE}Generated Passphrase: {WHITE}{passphrase}{RESET}")  # Output in English
            strength = assess_strength(passphrase, language='en')  # Assess strength in English
            print(f"{BLUE}This passphrase is considered: {strength}{RESET}")  # Output strength in English

    except ValueError as ve:
        print(f"{RED}Error: {ve}{RESET}")  # Print any value errors encountered
        exit(1)  # Exit with an error code
    except Exception as e:
        print(f"{RED}An unexpected error occurred: {e}{RESET}")  # Print any unexpected errors
        exit(1)  # Exit with an error code