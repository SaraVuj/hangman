import socket, threading, sys
from config import HOST, PORT, END, WAIT_MESSAGE, BLOCK, UNBLOCK
from utility import print_word


def receive():
    while True:
        data = cli_sock.recv(1024)
        str = data.decode().split('#')
        if data.decode() == END:
            break

        if data.decode() == WAIT_MESSAGE:
            print(WAIT_MESSAGE)
            continue

        if len(str) == 4:
            print()
            print(str[0])
            print(str[1])
            print(str[2])
            print(str[3])
            break
        elif len(str) != 3:
            print(data.decode())
            break
        elif len(str) == 3:
            if str[2].endswith(UNBLOCK):
                blocked = False
                str2 = str[2].replace(UNBLOCK, ' ')
                note = 'Your turn to guess'
            elif str[2].endswith(BLOCK):
                blocked = True
                str2 = str[2].replace(BLOCK, ' ')
                note = 'Other player is guessing'

            print()
            print(str[0])
            print(str[1])
            print_word(str2)
            print(note)

            if not blocked:
                letter = input('Type a letter:')
                while not len(letter) == 1 or not letter.isalpha():
                    print('A single letter was expected')
                    letter = input('Type a letter:')
                cli_sock.send(letter.encode())

    sys.exit()


if __name__ == "__main__":
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    cli_sock.connect((HOST, PORT))

    thread_receive = threading.Thread(target=receive)
    thread_receive.start()
