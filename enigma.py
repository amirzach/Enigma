import string

class EnigmaMachine:
    def __init__(self, rotors, reflector, plugboard_connections, initial_positions=None):
        self.alphabet = string.ascii_uppercase
        
        # Prompt user for initial positions if not provided
        if initial_positions is None:
            initial_positions = []
            for i in range(len(rotors)):
                position = input(f"Enter initial position for Rotor {i+1} (A-Z): ").upper()
                while position not in self.alphabet:
                    position = input(f"Invalid input. Enter a valid position (A-Z) for Rotor {i+1}: ").upper()
                initial_positions.append(position)

        self.initial_positions = initial_positions
        self.rotors = [Rotor(rotor, pos) for rotor, pos in zip(rotors, initial_positions)]
        self.reflector = Reflector(reflector)
        self.plugboard = Plugboard(plugboard_connections)

    def reset_rotors(self):
        # Resets each rotor to the initial position
        for rotor, position in zip(self.rotors, self.initial_positions):
            rotor.set_position(position)

    def encode_letter(self, letter):
        # Pass through plugboard
        letter = self.plugboard.swap(letter)

        # Forward pass through rotors
        for rotor in self.rotors:
            letter = rotor.forward(letter)

        # Pass through reflector
        letter = self.reflector.reflect(letter)

        # Backward pass through rotors
        for rotor in reversed(self.rotors):
            letter = rotor.backward(letter)

        # Pass through plugboard again
        letter = self.plugboard.swap(letter)

        # Rotate the first rotor after each letter is encoded
        self.rotate_rotors()

        return letter

    def rotate_rotors(self):
        # Rotate the first rotor and manage cascading rotations
        rotate_next = self.rotors[0].rotate()
        for i in range(1, len(self.rotors)):
            if rotate_next:
                rotate_next = self.rotors[i].rotate()
            else:
                break

    def encode_message(self, message):
        encoded_message = ""
        for letter in message.upper():
            if letter in self.alphabet:
                encoded_message += self.encode_letter(letter)
            else:
                encoded_message += letter  # Non-alphabet characters are added as-is
        return encoded_message


class Rotor:
    def __init__(self, wiring, initial_position, notch="Q"):
        self.alphabet = string.ascii_uppercase
        self.wiring = wiring
        self.notch = notch
        self.position = self.alphabet.index(initial_position)

    def set_position(self, letter):
        # Set rotor to a specific position
        self.position = self.alphabet.index(letter)

    def forward(self, letter):
        index = (self.alphabet.index(letter) + self.position) % 26
        translated_letter = self.wiring[index]
        return self.alphabet[(self.alphabet.index(translated_letter) - self.position) % 26]

    def backward(self, letter):
        index = (self.alphabet.index(letter) + self.position) % 26
        translated_letter = self.alphabet[self.wiring.index(self.alphabet[index])]
        return self.alphabet[(self.alphabet.index(translated_letter) - self.position) % 26]

    def rotate(self):
        # Rotate the rotor and check if it hits the notch position
        self.position = (self.position + 1) % 26
        return self.alphabet[self.position] == self.notch


class Reflector:
    def __init__(self, wiring):
        self.alphabet = string.ascii_uppercase
        self.wiring = wiring

    def reflect(self, letter):
        index = self.alphabet.index(letter)
        return self.wiring[index]


class Plugboard:
    def __init__(self, connections):
        self.alphabet = string.ascii_uppercase
        self.mapping = {letter: letter for letter in self.alphabet}

        # Set up the plugboard connections
        for a, b in connections:
            self.mapping[a] = b
            self.mapping[b] = a

    def swap(self, letter):
        return self.mapping[letter]


# Enigma configuration
rotors = [
    "EKMFLGDQVZNTOWYHXUSPAIBRCJ",  # Rotor I
    "AJDKSIRUXBLHWTMCQGZNPYFVOE",  # Rotor II
    "BDFHJLCPRTXVZNYEIWGAKMUSQO"   # Rotor III
]
reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
plugboard_connections = [('A', 'M'), ('F', 'I'), ('N', 'V'), ('P', 'S'), ('T', 'U')]

# Prompt user for the message to encode and decode
message = input("Enter the message to encode: ")

# Create the Enigma machine with user-defined rotor positions
enigma = EnigmaMachine(rotors, reflector, plugboard_connections)

# Encode and decode the message
enigma.reset_rotors()  # Reset to initial positions before encoding
encoded_message = enigma.encode_message(message)

enigma.reset_rotors()  # Reset to initial positions before decoding
decoded_message = enigma.encode_message(encoded_message)

# Output the results
print(f"Original message: {message}")
print(f"Encoded message: {encoded_message}")
print(f"Decoded message: {decoded_message}")
