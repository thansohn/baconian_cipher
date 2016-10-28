import json
import re

class BaconCipher:
    def __init__(self):
        self.cipher_key = {}

    def load_keys(self, filename):
        with open(filename) as data_file:    
            self.cipher_key = json.load(data_file)

    def encrypt(self, plaintext, passphrase):
        plaintext_length = sum(char != ' ' for char in plaintext)
        passphrase_length = sum(char != ' ' for char in passphrase)

        assert (plaintext_length * 5 == passphrase_length), \
        "Passphrase must be %r characters long, sans spaces. Your passphrase is " \
        "%r characters long." % ((plaintext_length * 5), passphrase_length)

        baconian_string = ""
        new_passphrase = ""
        current_baconian_char = 0

        #translate plaintext into baconian sequence
        for char in plaintext:
            if char != ' ': 
                baconian_string += (self.cipher_key[char.upper()])

        #translate baconian sequence into new passphase
        for char in passphrase:
            if char != ' ':
                if baconian_string[current_baconian_char] == "B":
                    new_passphrase += char.upper()
                elif baconian_string[current_baconian_char] == "A":
                    new_passphrase += char.lower()
                
                current_baconian_char += 1
            else:
                new_passphrase += char

        return new_passphrase

    def decrypt(self, passphrase):
        baconian_string = ""
        plaintext = ""

        for char in passphrase:
            if char != ' ':
                if char.isupper():
                    baconian_string += "B"
                elif char.islower():
                    baconian_string += "A"
                    
        for b in re.findall('.....', baconian_string):
            plaintext += self.cipher_key.keys()[self.cipher_key.values().index(b)]
        
        return plaintext

def main():
    bc = BaconCipher()
    plaintext = "python is cool"
    passphrase = "the quick brown fox jumped over the lazy dog because he was late for class"
    bc.load_keys("cipher.json")
    
    print "Plaintext: " + plaintext
    print "Passphrase: " + passphrase

    text = bc.encrypt(plaintext, passphrase)
    print "Encryption: " + text
    print "Decryption: " + bc.decrypt(text)

if __name__ == "__main__":
    main()