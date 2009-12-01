from twisted.application import service
from twisted.internet import reactor
from twitteror import Twitteror, Statuses

class SimpleTester(service.Service):
    def _found(self, result):
        print result

    def startService(self):
        dfr = self.parent.getServiceNamed('TwitterStatuses').home_timeline()
        dfr.addCallback(self._found)
        dfr.addCallback(lambda x: reactor.stop())

application = service.Application("simplesearch")

twitteror = Twitteror("USERNAME", "PASSWORD")
twitteror.setName("Twitteror")

statuses = Statuses()
statuses.setName("TwitterStatuses")

tester = SimpleTester()

twitteror.setServiceParent(application)
statuses.setServiceParent(application)
tester.setServiceParent(application)
