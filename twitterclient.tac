from twisted.application import service
from twisted.internet import reactor
from twitteror import AnonymousTwitteror, TwitterSearcher

class SimpleTester(service.Service):
    def _found(self, result):
        print result

    def startService(self):
        dfr = self.parent.getServiceNamed('TwitterSearch').search("#funny")
        dfr.addCallback(self._found)
        dfr.addCallback(lambda x: reactor.stop())

application = service.Application("simplesearch")

twitteror = AnonymousTwitteror()
twitteror.setName("Twitteror")

searcher = TwitterSearcher()
searcher.setName("TwitterSearch")

tester = SimpleTester()

twitteror.setServiceParent(application)
searcher.setServiceParent(application)
tester.setServiceParent(application)
