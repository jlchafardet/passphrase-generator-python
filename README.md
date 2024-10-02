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