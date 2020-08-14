from twisted.internet import reactor, ssl, _sslverify
from twisted.web.client import Agent, readBody
from twisted.web.iweb import IPolicyForHTTPS
from zope.interface import implementer
from twisted.internet.defer import gatherResults
from utility import *
from bs4 import BeautifulSoup
from config import URL

lives = 7
missed_letters = []


def play(movie):
    global lives
    hangman = no_lost_lives()
    print(hangman)
    w = ''
    for c in movie:
        if c.isalpha():
            w += '_'
        else:
            w += c

    print(w)
    while True:
        letter = input('Type a letter:')
        if letter in movie or letter.upper() in movie:
            w = new_letter_guessed(movie, letter, w)
            print_missed_letters(missed_letters)
            print(hangman)
            print(w)
            if '_' not in w:
                print('You guessed the movie')
                break
        else:
            if letter not in missed_letters:
                missed_letters.append(letter)
                lives -= 1

                if lives == 6:
                    hangman = one_lost_life()
                elif lives == 5:
                    hangman = two_lost_lives()
                elif lives == 4:
                    hangman = three_lost_lives()
                elif lives == 3:
                    hangman = four_lost_lives()
                elif lives == 2:
                    hangman = five_lost_lives()
                elif lives == 1:
                    hangman = six_lost_lives()
                else:
                    hangman = seven_lost_lives()

            print_missed_letters(missed_letters)
            print(hangman)
            print(w)

            if lives == 0:
                print('You lost. The movie was ' + movie)
                break


def onError(ignored):
    print(ignored)


def onResponse(response):
    deferred = readBody(response)
    deferred.addCallback(get_response)
    return deferred


def get_response(body):
    soup = BeautifulSoup(body, "html.parser")
    movie = soup.find('h1').text[:-5]
    play(movie)


@implementer(IPolicyForHTTPS)
class IgnoreHTTPS:
    def creatorForNetloc(self, hostname, port):
        options = ssl.CertificateOptions(verify=False)
        return _sslverify.ClientTLSOptions(hostname.decode('ascii'), options.getContext())


agent = Agent(reactor, IgnoreHTTPS())
closedDeferredes = []
d = agent.request(
    b'GET',
    URL.encode()
)

d.addCallback(onResponse)
d.addErrback(onError)
closedDeferredes.append(d)
gatherResults(closedDeferredes).addCallback(lambda ignored: reactor.stop())
reactor.run()
