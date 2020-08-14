import socket, threading
from config import HOST, PORT, END
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


def accept_client(movie):
    while True:
        cli_sock, cli_add = ser_sock.accept()
        if len(CONNECTION_LIST) < 2:
            CONNECTION_LIST.append(cli_sock)
            print('New player')
            thread_client = threading.Thread(target=broadcast, args=[cli_sock, movie])
            thread_client.start()
        else:
            print('Two players already playing')
            cli_sock.send(END.encode())
            cli_sock.close()


def broadcast(cli_sock, movie):
    global w
    global missed_letters
    global hangman
    global lives
    global missed_letters_str
    msg = ''
    while True:
        try:
            data = cli_sock.recv(1024)
            letter = data.decode()
            if letter in movie or letter.upper() in movie or letter.lower() in movie:
                w = new_letter_guessed(movie, letter, w) + '\n'

                if '_' not in w:
                    msg = 'You guessed the movie'
                    send(msg)
            else:
                if letter not in missed_letters:
                    missed_letters.append(letter)
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

            if lives == 0:
                msg = 'You lost. The movie was ' + movie
                send(msg)
                break

            missed_letters_str = get_missed_letters(missed_letters)
            msg += missed_letters_str + '#' + hangman + '#' + w
            send(msg)

        except Exception as e:
            print(e)
            break


def send(msg):
    for client in CONNECTION_LIST:
        print(client)
        client.send(msg.encode())


def run_server(movie):
    global w
    w = get_word_at_start(movie)
    thread_accept = threading.Thread(target=accept_client, args=[movie])
    thread_accept.start()
