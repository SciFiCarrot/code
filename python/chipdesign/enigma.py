rotorIII = "bdfhjlcprtxvznyeiwgakmusqo"
rotorI = "ekmflgdqvzntowyhxuspaibrcj"
rotorIV = "esovpzjayquirhxlnftgkdcmwb"
ukw_b = "yruhqsldpxngokmiebfzcwvjat"


def axis(letter, pos, layout, inverse=False):
    if not inverse:
        i = ord(letter.upper()) - 65
        wired = ord(layout[(i + pos) % 26].upper()) - 65
        o = (wired - pos) % 26
        return chr(o + 65)
    else:
        i = ord(letter.upper()) - 65
        wired = (i + pos) % 26
        src = layout.upper().index(chr(wired + 65))
        o = (src - pos) % 26
        return chr(o + 65)


test = str(input("giv din bogstav her: "))


def enigma(string, rotor1, rotor2, rotor3, reflector, rotor1pos, rotor2pos, rotor3pos):
    chars = []
    for char in string:
        char = axis(char, rotor1pos, rotor1)
        char = axis(char, rotor2pos, rotor2)
        char = axis(char, rotor3pos, rotor3)
        char = axis(char, 0, reflector)
        char = axis(char, rotor3pos, rotor3, True)
        char = axis(char, rotor2pos, rotor2, True)
        char = axis(char, rotor1pos, rotor1, True)
        chars.append(char)
        rotor1pos += 1

    crypted = "".join(chars)
    return crypted


print(enigma(test, rotorIII, rotorI, rotorIV, ukw_b, 1, 17, 12))
