# Passphrase Generator

## Overview

The Passphrase Generator is a command-line tool that generates secure and memorable passphrases. It allows users to customize the number of words, include special characters, and assess the strength of the generated passphrase.

## Features

- **User Input Validation**: Ensures that the number of words is a positive integer and does not exceed the available words in the list. Validates the `special_chars` argument to accept only 'true' or 'false'.
- **Custom Word List**: Users can specify a custom word list file via command-line arguments, providing flexibility in word selection.
- **Passphrase Complexity Options**:
  - Generates passphrases with a specified number of words (between 2 and 16).
  - Allows the inclusion of special characters in the passphrase.
- **Strength Assessment**:
  - Evaluates the strength of the generated passphrase based on length and character variety (uppercase, lowercase, digits, special characters).
  - Provides feedback on the strength of the passphrase (Very Weak, Weak, Normal, Strong, Very Strong).
- **Random Capitalization**: Randomly capitalizes a number of characters in the passphrase to enhance its strength, ensuring at least one character is capitalized and no more than half of the total characters.
- **Error Handling**: Robust error handling to manage potential issues, such as file not found errors or invalid input formats, with user-friendly error messages.

## Usage

To run the Passphrase Generator, use the following command in your terminal:

```bash
python passphrase-generator.py <num_words> <special_chars>
```

### Parameters

- `<num_words>`: The number of words to include in the passphrase (between 2 and 16).
- `<special_chars>`: Specify 'true' to include special characters or 'false' to exclude them.

### Example

```bash
python passphrase-generator.py 5 true
```

This command generates a passphrase consisting of 5 words, including special characters.

## Requirements

- Python 3.x
- A text file containing a list of words (e.g., `words-en.txt`) in the same directory as the script.

# Changes Made to Passphrase Generator

1. **User Input Validation**:
   - Implemented validation for `num_words` to ensure it is a positive integer and does not exceed the number of available words.
   - Validated the `special_chars` argument to ensure it only accepts 'true' or 'false'.

2. **Error Handling**:
   - Added robust error handling to manage potential issues and provide user-friendly error messages.

3. **Performance Optimization**:
   - Optimized vowel replacement using `str.maketrans` for faster character replacements.
   - Reduced string operations by building the passphrase more efficiently.

4. **Passphrase Generation Logic**:
   - Implemented continuous generation of passphrases until the total character count exceeds 10.
   - Ensured the passphrase does not exceed 100 characters and does not exceed 16 words.
   - Modified special character replacement to ensure at least one word is replaced and a maximum of half the selected words.

5. **General Improvements**:
   - Improved overall code structure and readability.
   - Added color-coded output for better user experience, with specific colors for errors, strength levels, and passphrase display.

## Future Improvements

- **Graphical User Interface (GUI)**: Consider creating a simple GUI for users who may not be comfortable with command-line operations.
- **Logging and History**: Implement logging to keep track of generated passphrases for user reference, with options to save or export them securely.
- **Internationalization**: Support multiple languages for the word list and user interface to cater to a broader audience.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by various password generation techniques and best practices for creating secure passwords.
