rotorIII = "bdfhjlcprtxvznyeiwgakmusqo"
rotorI = "ekmflgdqvzntowyhxuspaibrcj"
rotorIV = "esovpzjayquirhxlnftgkdcmwb"
reflektorA = "ejmzalyxvbwfcrquontspikhgd"


def axis(input, pos, layout):
    old_number = ord(input) - 96
    new_number = (old_number + pos + 1) % 26
    output = layout[new_number]
    return output


# def reflector(input, layout):
#   old_number = ord(input) - 96
#    new_number = (old_number + 1) % 26
#   output = layout[new_number]
# return output


def reflector(letter, layout):
    return layout[ord(letter.upper()) - 65].upper()


position = 14
rotor1 = "OPMYLBCWDFHKZXSNQTURJGAIVE"
test = str(input("giv din bogstav her: "))
print(rotor(test, reflektorA))
