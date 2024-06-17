import sys
import string
from colors import TextColors
# Encoding and Decoding Dictionaries
extra_chars = "€£¥₣₹₱₽"
chars = string.printable
chars = chars + extra_chars
encoding = {char: f"{i:03}" for i, char in enumerate(chars)} # Creates a dictionary called encoding where each character
                                                             # from chars is mapped to a zero-padded three-digit string representing its index.

decoding = {v: k for k, v in encoding.items()}               # Creates a reverse dictionary decoding where the keys are the three-digit strings 
                                                             # and the values are the original characters.
t = TextColors
def encode_text(text, encoding): # encodes the text
    encoded_text = ''
    text = str(text)
    for char in text:
        encoded_text += encoding.get(char, char)
    return encoded_text

def decode_text(encoded_text, decoding): # decodes the text
    decoded_text = ''
    i = 0
    while i < len(encoded_text):
        encoded_char = encoded_text[i:i+3]
        decoded_text += decoding.get(encoded_char, encoded_char)
        i += 3
    return decoded_text

def verify(): # verifies user by asking for a key. If a key is deleted all data is lost.
    key = ".KEY"
    try:
        with open(key, "r") as file:
            scrambled_key = file.read()
            temp_var_key = decode_text(scrambled_key, decoding)
            user_key = input(f"Please Enter Key:\n")
            if user_key == temp_var_key:
                print(f"Welcome Back to Expense Tracker\n")
            else:
                print(f"Incorrect Key")
                sys.exit(0)
    except FileNotFoundError:
        from main import forceful_reset
        forceful_reset()
        open(key, 'x')
        new_key = input(
            f"{t.bold}Key not Found, any Data has been Reset for Security purposes.{t.end}\n"
            f"Please Enter a New Key\n"
            f"({t.bold}Highly recommend strong key contain symbols, capital and lowercase letters and numbers!){t.end}\n"
        )
        scrambled_new_key = encode_text(new_key, encoding)
        with open(key, "w") as file:
            file.write(scrambled_new_key)
        print(f"Program closed, restart to load into program.\n")
        sys.exit(0)
