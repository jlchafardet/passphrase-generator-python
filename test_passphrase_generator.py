import sys
import unittest
from passphrase_generator import load_word_list, replace_vowels, assess_strength, generate_passphrase

class TestPassphraseGenerator(unittest.TestCase):

    def test_load_word_list(self):
        # Test loading a valid word list
        words = load_word_list('en')  # Assuming 'words-en.txt' exists
        self.assertGreater(len(words), 0)  # Ensure the list is not empty

        # Test loading an invalid word list
        with self.assertRaises(SystemExit):  # Expecting the program to exit
            load_word_list('invalid_language')  # This should trigger the error

    def test_replace_vowels(self):
        # Test replacing vowels in a word
        self.assertEqual(replace_vowels('hello'), 'h3ll0')  # Check vowel replacement
        self.assertEqual(replace_vowels('banana'), 'b@n@n@')  # Check vowel replacement for 'a'
        self.assertEqual(replace_vowels('umbrella'), 'umbr3ll@')  # Check vowel replacement for 'u' and 'e'

    def test_assess_strength(self):
        # Test strength assessment for various passphrases
        self.assertEqual(assess_strength('short'), 'Very Weak')  # Short passphrase
        self.assertEqual(assess_strength('LongerPassphrase123!'), 'Very Strong')  # Strong passphrase

    def test_generate_passphrase(self):
        # Test passphrase generation
        word_list = ['apple', 'banana', 'cherry', 'date', 'elderberry']
        passphrase = generate_passphrase(word_list, num_words=3, use_special_chars=False)
        self.assertGreaterEqual(len(passphrase.split()), 3)  # Ensure at least 3 words
        self.assertLessEqual(len(passphrase), 127)  # Ensure passphrase does not exceed 127 characters

if __name__ == '__main__':
    unittest.main()
