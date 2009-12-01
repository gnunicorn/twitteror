
from zope.interface import Interface, implements
from twisted.application.service import Service
from twisted.web.client import getPage

from StringIO import StringIO
import urllib

try:
    import json
except ImportError:
    import simplejson as json


def _jsonify(result):
    return json.load(StringIO(result))

def _get_none_keywords(keywords):
    results = {}
    for key, value in keywords.iteritems():
        if value is not None:
            results[key] = value
    return results


class TwitterorInterface(Interface):
    """
    The API of the TwitterorClient, allows to make requests
    """
    def query(self, url, **kwargs):
        pass

class AnonymousTwitteror(Service):
    implements(TwitterorInterface)

    def query(self, url, method='GET', **kwargs):
        dfr = getPage('?'.join([url, urllib.urlencode(kwargs, True)]), method=method)
        dfr.addCallback(_jsonify)
        return dfr

class Querier(object):

    def __init__(self, source="Twitteror"):
        self.source = source

    def _query(self, url, **kwargs):
        return self.parent.getServiceNamed(self.source
                ).query(url, **_get_none_keywords(kwargs))

class TwitterSearcher(Querier, Service):
    def search(self, term, lang=None, locale=None, rpp=None, page=None,
            since_id=None, geocode=None, show_user=None):
        search_url = "http://search.twitter.com/search.json"
        return self._query(search_url, q=term, lang=lang, locale=locale,
                rpp=rpp, page=page, since_id=since_id, geocode=geocode,
                show_user=show_user)

class TrendsSearcher(Querier, Service):
    """
    Can query everything trends based. Trends don't need any authentication.
    """
    def trends(self):
        url = "http://search.twitter.com/trends.json"
        return self._query(url)

    def trends_current(self, exclude=None):
        url = "http://search.twitter.com/trends/current.json"
        return self._query(url, exclude=exclude)

    def trends_daily(self, exclude=None, date=None):
        url = "http://search.twitter.com/trends/daily.json"
        return self._query(url, exclude=exclude, date=date)

    def trends_weekly(self, exclude=None, date=None):
        url = "http://search.twitter.com/trends/weekly.json"
        return self._query(url, exclude=exclude, date=None)

class Statuses(Querier, Service):
    """
    Queries everything Status based (timeline and status section in the API
    documentation). Some of those need authentication before you are able to
    use them. See their API documentation on apiwiki.twitter.com for more
    information.
    """
    def public_timeline(self):
        url = "http://twitter.com/statuses/public_timeline.json"
        return self._query(url)

    def home_timeline(self, since_id=None, max_id=None, count=None, page=None):
        url = "http://twitter.com/statuses/home_timeline.json"
        return self._query(url, since_id=since_id, max_id=max_id,
                count=count, page=page)

    def friends_timeline(self, since_id=None, max_id=None,
            count=None, page=None):
        url = "http://twitter.com/statuses/friends_timeline.json"
        return self._query(url, since_id=since_id, max_id=max_id,
                count=count, page=page)

    def user_timeline(self, id=None, user_id=None, screen_name=None,
            since_id=None, max_id=None, count=None, page=None):
        url = "http://twitter.com/statuses/user_timeline.json"
        return self._query(url, id=id, user_id=user_id, screen_name=screen_name,
                since_id=since_id, max_id=max_id, count=count, page=page)

    def mentions(self, since_id=None, max_id=None,
            count=None, page=None):
        url = "http://twitter.com/statuses/mentions.json"
        return self._query(url, since_id=since_id, max_id=max_id,
                count=count, page=page)

    def retweeted_by_me(self, since_id=None, max_id=None,
            count=None, page=None):
        url = "http://twitter.com/statuses/retweeted_by_me.json"
        return self._query(url, since_id=since_id, max_id=max_id,
                count=count, page=page)

    def retweeted_to_me(self, since_id=None, max_id=None,
            count=None, page=None):
        url = "http://twitter.com/statuses/retweeted_to_me.json"
        return self._query(url, since_id=since_id, max_id=max_id,
                count=count, page=page)

    def retweets_of_me(self, since_id=None, max_id=None,
            count=None, page=None):
        url = "http://twitter.com/statuses/retweets_of_me.json"
        return self._query(url, since_id=since_id, max_id=max_id,
                count=count, page=page)

    def show(self, tweet_id):
        url = "http://twitter.com/statuses/%s.json" % tweet_id
        return self._query(url)

    def update(self, status, in_reply_to_status_id=None, lat=None, long=None):
        # FIXME: "long" is really not nice here!
        url = "http://twitter.com/statuses/update.json"
        return self._query(url, method="POST", status=status, lat=lat,
                long=long, in_reply_to_status_id=in_reply_to_status_id)

    def destory(self, tweet_id):
        url = "http://twitter.com/statuses/destroy/%s.json" % tweet_id
        return self._query(url, method="DELETE")

    def retweets(self, tweet_id, count=None):
        url = "http://twitter.com/statuses/retweets/%s.json" % tweet_id
        return self._query(url, count=count)

