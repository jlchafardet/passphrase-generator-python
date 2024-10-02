import re
import glob
import os

def remove_special_characters(word_list):
    """Remove special characters from each word."""
    return [re.sub(r'[^a-zA-Z0-9]', '', word) for word in word_list]

def convert_to_lowercase(word_list):
    """Convert all words to lowercase."""
    return [word.lower() for word in word_list]

def trim_spaces(word_list):
    """Trim leading and trailing spaces from each word."""
    return [word.strip() for word in word_list]

def remove_short_words(word_list):
    """Remove words with less than 3 characters."""
    return [word for word in word_list if len(word) >= 3]

def remove_long_repeated_characters(word_list):
    """Remove words with more than 2 of the same character adjacent."""
    return [word for word in word_list if not re.search(r'(.)\1{2,}', word)]

def remove_duplicates(word_list):
    """Remove duplicate words."""
    return list(set(word_list))

def remove_numeric_characters(word_list):
    """Remove words that contain numbers."""
    return [word for word in word_list if not any(char.isdigit() for char in word)]

def remove_empty_lines(word_list):
    """Remove empty lines from the list."""
    return [word for word in word_list if word]

def filter_by_length(word_list, min_length=3, max_length=15):
    """Filter words by specified length."""
    return [word for word in word_list if min_length <= len(word) <= max_length]

def remove_common_words(word_list, common_words):
    """Remove common words from the list."""
    return [word for word in word_list if word not in common_words]

def clean_word_list(file_path, common_words=[]):
    """Main function to clean the word list."""
    try:
        with open(file_path, 'r') as file:
            word_list = file.readlines()
    except FileNotFoundError:
        return f"{file_path} not found. Please check the file path."
    except Exception as e:
        return f"An unexpected error occurred while reading {file_path}: {e}"

    # Apply cleaning methods
    original_length = len(word_list)
    word_list = remove_special_characters(word_list)
    word_list = convert_to_lowercase(word_list)
    word_list = trim_spaces(word_list)
    word_list = remove_short_words(word_list)
    word_list = remove_long_repeated_characters(word_list)
    word_list = remove_duplicates(word_list)
    word_list = remove_numeric_characters(word_list)
    word_list = remove_empty_lines(word_list)
    word_list = filter_by_length(word_list)
    word_list = remove_common_words(word_list, common_words)

    # Check if any changes were made
    if len(word_list) != original_length:
        try:
            with open(file_path, 'w') as file:
                for word in word_list:
                    file.write(f"{word}\n")
            return f"Cleaned {file_path}"
        except Exception as e:
            return f"An unexpected error occurred while writing to {file_path}: {e}"
    else:
        return f"{file_path} didn't need any cleaning up."

if __name__ == "__main__":
    # Common words to remove
    common_words = ['hola', 'adios', 'gracias', 'mama', 'papa', 'hijo', 'hija', 'tia', 'tio', 'soy', 'que', 'tal', 'muy', 'asi', 'mal', 'por', 'que', 'ver']

    # Iterate through all wordlist files
    log = []
    for file_path in glob.glob('words-*.txt'):
        result = clean_word_list(file_path, common_words)
        log.append(result)

    # Print log results
    for entry in log:
        print(entry)
