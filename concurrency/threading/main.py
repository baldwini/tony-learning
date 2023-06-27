import concurrent.futures
import logging
import threading
import time
import requests

class FakeDatabase:
    def __init__(self):
        self.value = 0
        self._lock =  threading.Lock()

    def locked_update(self, name):
        logging.info('Thread %s: starting update', name)
        logging.info("Thread %s about to lock", name)
        with self._lock:
            logging.debug("Thread %s has lock", name)
            local_copy = self.value
            local_copy += 1
            time.sleep(0.1)
            self.value = local_copy
            logging.debug("Thread %s about to release lock", name)
        logging.debug("Thread %s after release", name)
        logging.info("Thread %s: finishing update", name)

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finished", name)

def request_function(req_tuple):
    logging.info("Thread %s: starting", req_tuple[1])
    r = requests.get(req_tuple[0], verify=False)
    logging.info(r.status_code)
    logging.info("Thread %s: finished", req_tuple[1])

if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG,
                        datefmt="%H:%M:%S")

    args = []
    for i in range(3):
        args.append(("https://www.google.com", i))
    print(args)

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(request_function, args)

    # logging.info("Main: before creating thread")
    # x = threading.Thread(target=thread_function, args=("1",), daemon=True)
    # logging.info("Main: before running thread")
    # x.start()
    # logging.info("Main: wait for the thread to finish")
    # x.join()
    # logging.info("Main: all done")

    # threads = []
    # for i in range(3):
    #     logging.info("Main: create and start thread %d.", i)
    #     x = threading.Thread(target=thread_function, args=(i,))
    #     threads.append(x)
    #     x.start()
    #
    # for i, thread in enumerate(threads):
    #     logging.info("Main: before joining thread %d.", i)
    #     thread.join()
    #     logging.info("Main: thread %d done", i)

    # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    #     executor.map(thread_function, range(3))

    # database = FakeDatabase()
    # logging.info("Testing update. Starting value is %d", database.value)
    # with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    #     for index in range(2):
    #         executor.submit(database.locked_update, index)
    # logging.info("Testing update. Ending value is %d", database.value)

    # request_function("https://www.google.com")