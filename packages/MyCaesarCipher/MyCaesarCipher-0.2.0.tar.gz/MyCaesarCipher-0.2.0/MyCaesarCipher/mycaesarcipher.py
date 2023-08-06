#!/usr/bin/env python3

from random import Random


class CaesarCipher:
    """Class containing cryptographic encryption/decryption methods using the Caesar-Cipher algorithm.

    - Substitutes each letter of a message with new "matching" letter shifted down alphabetically by a given amount.
    - Not for real-world cryptographic applications, as the Caesar Cipher is notoriously easy to crack.
    - More information on this cipher:
        - https://en.wikipedia.org/wiki/Caesar_cipher
    """

    def __init__(self):
        pass

    def encrypt(self,
                text: str,
                key: int = None,
                print_to_console: bool = True) -> str:
        """Encrypt text using the Caesar-Cypher cryptography algorithm.

        - Generates encrypted form of `text: str` using the Caesar-Cipher algorithm.
        - If no `key` is provided, a random key is generated.

        :param text: text to encrypt.
        :type text: str
        :param key: numeric value used to encrypt the given text, defaults to None
        :type key: int, optional
        :param print_to_console: toggles print statements to stdout, defaults to True
        :type print_to_console: bool, optional
        :return: encrypted form of `text: str`
        :rtype: str
        """

        result: str = ''
        if key is None:
            key = Random().randint(1, 25)

        #@ Iterate through text char by char.
        for character in text:
            #@ Encrypt uppercase characters in text
            if (character.isupper()):
                result += chr((ord(character) + key - 65) % 26 + 65)
            #@ Encrypt lowercase characters in text
            elif (character.islower()):
                result += chr((ord(character) + key - 97) % 26 + 97)
            #@ Encrypt numbers in text
            elif (character.isdigit()):
                result += str((int(character) + key) % 10)
            #@ Leave all non-alphanumeric characters unchanged.
            else:
                result += character
        info: str = f'> Original Msg : {text}\n> Shift-key : {key}\n> Encrypted Result: {result}\n'

        if print_to_console:
            print(info)

        return result

    def decrypt(self, text: str, print_to_console: bool = True):
        """Decrypt Caesar-Cipher encrypted messages using brute force.

        ---

        :param text: text to decode.
        :type text: str
        :param print_to_console: if true enable printing output to stdout, defaults to True.
        :type print_to_console: bool
        :return: all possible pairs of shift-keys and their decrypted results.
        :rtype: str
        """

        #@ Outputs all possible shift-keys using the english alphabet.
        for key in range(26):
            translated = ''
            for character in text:
                if (character.isupper()):
                    translated += chr((ord(character) - key - 65) % 26 + 65)
                #@ Decrypt lowercase characters in text
                elif (character.islower()):
                    translated += chr((ord(character) - key - 97) % 26 + 97)
                #@ Decrypt numbers in text
                elif (character.isdigit()):
                    translated += str((int(character) - key) % 10)
                #@ Leave all non-alphanumeric characters unchanged.
                else:
                    translated += character

            if print_to_console:
                print(f'> Decrypted Shift-Key {key} : {translated}\n')
        return translated