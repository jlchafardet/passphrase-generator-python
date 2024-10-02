import re

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

def clean_word_list(input_file, output_file, common_words=[]):
    """Main function to clean the word list."""
    with open(input_file, 'r') as file:
        word_list = file.readlines()

    # Apply cleaning methods
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

    # Write cleaned word list to output file
    with open(output_file, 'w') as file:
        for word in word_list:
            file.write(f"{word}\n")

if __name__ == "__main__":
    # Example usage
    input_file = 'input_wordlist.txt'  # Replace with your input file
    output_file = 'cleaned_wordlist.txt'  # Output file for cleaned words
    common_words = ['hola', 'adios', 'gracias', 'mama', 'papa', 'hijo', 'hija', 'tia', 'tio', 'soy', 'que', 'tal', 'muy', 'asi', 'mal', 'por', 'que', 'ver']  # Updated common words list

    clean_word_list(input_file, output_file, common_words)
    print(f"Cleaned word list has been saved to {output_file}.")
