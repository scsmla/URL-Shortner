ALLOW_STRING = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
base = len(ALLOW_STRING)

def encode(number):
    result = []

    if(number == 0):
        return ALLOW_STRING[number]

    while(number > 0):
        result.append(ALLOW_STRING[number % base])
        number = number // base
    result.reverse()

    return ''.join(result)


def decode(input):
    counter, decoded = 1, 0
    input_length = len(input)

    for character in input:
        decoded += ALLOW_STRING.find(character) * pow(base, input_length-counter)
        counter += 1

    return decoded
