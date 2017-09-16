import requests
import threading
import time
from queue import Queue


from utils import handle_exception


class JsonCrawler(threading.Thread):
    crawlers = dict()

    def __init__(self, url, name, period=10., active=False):
        if name in JsonCrawler.crawlers:
            JsonCrawler.crawlers[name]._stop()
        super(JsonCrawler, self).__init__()
        self._stop_event = threading.Event()
        self.setDaemon(True)
        self.queue = Queue()

        self.active = active
        self.period = period
        self.url = url
        self.name = name
        JsonCrawler.crawlers[name] = self

        self.start()

    def _stop(self):
        self._stop_event.set()

    def kill(self):
        del JsonCrawler.crawlers[self.name]
        self._stop()

    def run(self):
        if self.active:
            while True:
                self.crawl()
                time.sleep(self.period)
        else:
            self.crawl()

    def __str__(self):
        return self.name

    @classmethod
    @handle_exception
    def get_by_name(cls, name):
        return cls.crawlers[name]

    @handle_exception
    def crawl(self):
        # Collect data from website
        response = requests.get(self.url)
        response.raise_for_status()
        data = response.json()
        self.queue.put(data)

    def get_data(self):
        return self.queue.get()
