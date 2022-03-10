'''
This is a web scraper for RSS feed(s) to demonstrate multithreading.

'''

from wsgiref.headers import Headers
import requests
import lxml
from bs4 import BeautifulSoup
from threading import Thread, Lock, Semaphore
import time
import string
from random import choice


# RSS_FEED_URLS = [
#     'https://www.nydailynews.com/arcio/rss/category/news/?sort=display_date:desc', 'https://www.nydailynews.com/arcio/rss/category/opinion/?sort=display_date:desc', 'https://www.nydailynews.com/arcio/rss/category/sports/?sort=display_date:desc']

RSS_FEED_URLS = [
    'https://www.france24.com/en/asia-pacific/rss', 'https://www.france24.com/en/africa/rss', 'https://www.france24.com/en/france/rss', 'https://www.france24.com/en/sport/rss']

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'

header = {
    'User-Agent': USER_AGENT
}


def addToIndex(data, indexLock, index):
    # Protect critical regions of code...
    with indexLock:
        index.append(data)


def downloadUrl(articleUrl, index, indexLock):
    try:
        request = requests.get(articleUrl, headers=header)
    except Exception as e:
        print(e)
    else:
        # Simulate parsing over a network
        time.sleep(0.10)
        # TODO: parse data from each article page
        soup = BeautifulSoup(request.text)
        paragraphs = soup.find('article').findAll('p')
        for paragraph in paragraphs:
            # print(paragraph)
            addToIndex(paragraph, indexLock, index)


def cleanup(threads):
    for thread in threads:
        thread.join()


def main():
    allUrls = []
    for feedUrl in RSS_FEED_URLS:
        request = requests.get(feedUrl, headers=header)
        print(request.status_code)
        if request.status_code == 200:
            try:
                soup = BeautifulSoup(request.text, 'lxml')
            except Exception as e:
                print('Could not parse the xml: ', request.url)
                print(e)
            # Source: https://www.jcchouinard.com/read-rss-feed-with-python/
            articles = soup.findAll('item')
            articles_dicts = [{'title': a.find('title').text, 'link': a.link.nextSibling.replace('\n', '').replace('\t', '').strip(), 'description': a.find(
                'description').text, 'pubdate': a.find('pubdate').text} for a in articles]
            urls = [d['link'] for d in articles_dicts if 'link' in d]
            titles = [d['title'] for d in articles_dicts if 'title' in d]
            allUrls += (urls)

    # print(allUrls)
    threads = []
    index = []
    indexLock = Lock()
    for url in allUrls:
        # TODO: Threadpool
        thread = Thread(target=downloadUrl, args=(url, index, indexLock))
        threads.append(thread)
        thread.start()
    cleanup(threads)
    print(index)


if __name__ == "__main__":
    main()
