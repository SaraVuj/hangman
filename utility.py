def no_lost_lives():
    return '+---+\n|   |\n|\n|\n|\n|\n'


def new_letter_guessed(movie, letter, old_w):
    w = list(old_w)
    str = ''
    pos = 0
    for c in movie:
        if c.lower() == letter.lower():
            w[pos] = c
        pos += 1

    return str.join(w)


def print_missed_letters(missed_letters):
    if not len(missed_letters):
        print('Your missed letters will be shown here')
    else:
        print('Your missed letters: ', end=' ')
        for letter in missed_letters:
            if missed_letters[len(missed_letters) - 1] == letter:
                print(letter)
            else:
                print(letter + ',', end=' ')


def one_lost_life():
    return '+---+\n|   |\n|   O\n|\n|\n|\n'


def two_lost_lives():
    return '+---+\n|   |\n|   O\n|   |\n|\n|\n'


def three_lost_lives():
    return '+---+\n|   |\n|   O\n|  /|\n|\n|\n'


def four_lost_lives():
    return '+---+\n|   |\n|   O\n|  /|\\\n|\n|\n'


def five_lost_lives():
    return '+---+\n|   |\n|   O\n|  /|\\\n|  /\n|\n'


def six_lost_lives():
    return '+---+\n|   |\n|   O\n|  /|\\\n|  / \\\n|\n'


def seven_lost_lives():
    return '+---+\n|   |\n|   O\n|  /|\\\n|  / \\\n|    |\n'