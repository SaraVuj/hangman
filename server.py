import random
import socket
import threading

from config import HOST, PORT, END, WAIT_MESSAGE, BLOCK, UNBLOCK
from utility import *

NUM_OF_PLAYERS = 2
CONNECTION_LIST = []
ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ser_sock.bind((HOST, PORT))
ser_sock.listen(1)

lives = 6
missed_letters = []
hangman = no_lost_lives()
w = ''
missed_letters_str = ''
msg = ' '
GAME_OVER = False
current_player = None


def accept_client(movie):
    global msg, w, missed_letters_str, missed_letters, hangman
    while not GAME_OVER:
        cli_sock, cli_add = ser_sock.accept()
        if len(CONNECTION_LIST) < NUM_OF_PLAYERS:
            CONNECTION_LIST.append(cli_sock)

            thread_client = threading.Thread(target=broadcast, args=[cli_sock, movie])
            thread_client.start()
        else:
            cli_sock.send(END.encode())
            cli_sock.close()


def broadcast(cli_sock, movie):
    global msg, w, missed_letters, hangman, lives, missed_letters_str
    global GAME_OVER, current_player
    sent = False
    start_game = True
    while True:
        if len(CONNECTION_LIST) != NUM_OF_PLAYERS and not sent:
            cli_sock.send(WAIT_MESSAGE.encode())
            sent = True
            continue
        elif len(CONNECTION_LIST) != NUM_OF_PLAYERS:
            continue
        elif start_game and len(CONNECTION_LIST) == NUM_OF_PLAYERS and CONNECTION_LIST[NUM_OF_PLAYERS - 1] == cli_sock:
            missed_letters_str = get_missed_letters(missed_letters)
            if msg == ' ':
                msg = missed_letters_str + '#' + hangman + '#' + w

            current_player = random.choice(CONNECTION_LIST)
            unblocking_msg = msg + UNBLOCK
            current_player.send(unblocking_msg.encode())

            blocking_msg = msg + BLOCK
            send_except_current(current_player, blocking_msg)
            start_game = False

        try:
            data = cli_sock.recv(1024)
            letter = data.decode()

            if letter in movie or letter.upper() in movie or letter.lower() in movie:
                w = new_letter_guessed(movie, letter, w)
                current_player = cli_sock
                if '_' not in w:
                    msg = missed_letters_str + '#' + hangman + '#' + w + '#You guessed the movie'
                    cli_sock.send(msg.encode())
                    send_except_current(cli_sock, 'You lost. The movie was ' + movie)
                    GAME_OVER = True
                    break
            else:
                if letter.lower() not in missed_letters:
                    current_player = get_other_player(cli_sock)

                    missed_letters.append(letter.lower())
                    lives -= 1

                    if lives == 5:
                        hangman = one_lost_life()
                    elif lives == 4:
                        hangman = two_lost_lives()
                    elif lives == 3:
                        hangman = three_lost_lives()
                    elif lives == 2:
                        hangman = four_lost_lives()
                    elif lives == 1:
                        hangman = five_lost_lives()
                    else:
                        hangman = six_lost_lives()

            missed_letters_str = get_missed_letters(missed_letters)
            if lives == 0:
                msg = missed_letters_str + '#' + hangman + '#' + w + '#You lost. The movie was ' + movie
                send(msg)
                GAME_OVER = True
                break

            msg = missed_letters_str + '#' + hangman + '#' + w
            unblocking_msg = msg + UNBLOCK
            current_player.send(unblocking_msg.encode())

            blocking_msg = msg + BLOCK
            send_except_current(current_player, blocking_msg)
        except Exception as e:
            print(e)
            break


def send(msg):
    for client in CONNECTION_LIST:
        client.send(msg.encode())


def send_except_current(current, msg):
    for client in CONNECTION_LIST:
        if client != current:
            client.send(msg.encode())


def get_other_player(current):
    for client in CONNECTION_LIST:
        if client != current:
            return client


def run_server(movie):
    global w
    w = get_word_at_start(movie)
    thread_accept = threading.Thread(target=accept_client, args=[movie])
    thread_accept.start()
