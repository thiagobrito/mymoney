from queue import *
from threading import *


class WorkerBase:
    def __init__(self):
        self._ready = False

    def work(self):
        pass


class ProcessingQueue:
    def __init__(self, number_of_threads, testing=False):
        self.queue = Queue()
        self._thread_list = []
        self.start(number_of_threads)
        self._workers = {}
        self._testing = testing

    def __exit__(self, exc_type, exc_value, traceback):
        self.queue.get_nowait()

    def start(self, number_of_threads):
        for i in range(number_of_threads):
            thread = Thread(target=self._worker, daemon=True)
            thread.start()
            self._thread_list.append(thread)

    def add(self, id, item):
        if self._testing:
            return item.work()

        self._workers[id] = item
        self.queue.put(item)

    def locate(self, id):
        if id in self._workers:
            return self._workers[id]

    def _worker(self):
        while True:
            item = self.queue.get()
            item.work()
            self.queue.task_done()
