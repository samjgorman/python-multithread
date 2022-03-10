'''
This is a web scraper for RSS feed(s) to demonstrate multithreading.

Sources:
https://www.jcchouinard.com/read-rss-feed-with-python/

'''

import requests
import lxml
from bs4 import BeautifulSoup
from threading import Thread, Lock, Semaphore
import time

RSS_FEED_URLS = [
    'https://www.france24.com/en/asia-pacific/rss', 'https://www.france24.com/en/africa/rss', 'https://www.france24.com/en/france/rss', 'https://www.france24.com/en/sport/rss']

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'

header = {
    'User-Agent': USER_AGENT
}


class ThreadedRSSFeed:

    def __cleanup(self):
        for thread in self.threads:
            thread.join()

    def __addToIndex(self, data):
        # Protect critical regions of code...
        with self.indexLock:
            self.index.append(data)

    def __downloadUrl(self, articleUrl):
        try:
            request = requests.get(articleUrl, headers=self.headers)
        except Exception as e:
            print(e)
        else:
            # Simulate parsing over a network
            time.sleep(0.10)
            # TODO: parse data from each article page
            soup = BeautifulSoup(request.text)
            paragraphs = soup.find('article').findAll('p')
            for paragraph in paragraphs:
                self.__addToIndex(paragraph)

    def __dispatchThreads(self):
        for url in self.articleUrls:
            # TODO: Threadpool
            thread = Thread(target=self.__downloadUrl, args=(url,))
            self.threads.append(thread)
            thread.start()
        self.__cleanup()

    def __init__(self, RSSArray, headers):
        self.RSSArray = RSSArray
        self.headers = headers
        self.articleUrls = []
        self.index = []
        self.indexLock = Lock()
        self.threads = []

        for RSSfeed in self.RSSArray:
            request = requests.get(RSSfeed, headers=self.headers)
            if request.status_code == 200:
                try:
                    soup = BeautifulSoup(request.text, 'lxml')
                except Exception as e:
                    print('Could not parse the xml: ', request.url)
                    print(e)
            articles = soup.findAll('item')
            articles_dicts = [{'title': a.find('title').text, 'link': a.link.nextSibling.replace('\n', '').replace('\t', '').strip(), 'description': a.find(
                'description').text, 'pubdate': a.find('pubdate').text} for a in articles]
            urls = [d['link'] for d in articles_dicts if 'link' in d]
            titles = [d['title'] for d in articles_dicts if 'title' in d]
            self.articleUrls += (urls)
        self.__dispatchThreads()


def main():
    feed = ThreadedRSSFeed(RSS_FEED_URLS, header)
    print(feed.index)


if __name__ == "__main__":
    main()
