from twisted.internet import reactor, ssl, _sslverify
from twisted.web.client import Agent, readBody
from twisted.web.iweb import IPolicyForHTTPS
from zope.interface import implementer
from twisted.internet.defer import gatherResults
from bs4 import BeautifulSoup
from config import URL
from server import run_server


def onError(ignored):
    print(ignored)


def onResponse(response):
    deferred = readBody(response)
    deferred.addCallback(get_response)
    return deferred


def get_response(body):
    soup = BeautifulSoup(body, "html.parser")
    movie = soup.find('h1').text[:-5]
    run_server(movie)


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
