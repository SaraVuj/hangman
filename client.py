import socket, threading
from config import HOST, PORT, END
from utility import *

IND = True


def send():
    while IND:
        letter = input('Type a letter:')
        if not len(letter) == 1 or not letter.isalpha():
            print('A single letter was expected')
            continue
        else:
            cli_sock.send(letter.encode())


def receive():
    global IND
    while IND:
        data = cli_sock.recv(1024)
        str = data.decode().split('#')
        if data.decode() == END:
            print('Two players already playing')
            IND = False
            break
        print()
        print(str[0])
        print(str[1])
        print(str[2])


if __name__ == "__main__":
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    cli_sock.connect((HOST, PORT))

    thread_send = threading.Thread(target=send)
    thread_send.start()

    thread_receive = threading.Thread(target=receive)
    thread_receive.start()