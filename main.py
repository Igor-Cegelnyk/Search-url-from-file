import pickle

import threading
import time
import httpx

from urlextract import URLExtract
from loguru import logger


message = "messages_to_parse.dat"


def get_urls_list(data_new: list) -> list:

    """Get urls from messages_to_parse.dat"""

    extractor = URLExtract()
    return [",".join(extractor.find_urls(elem, with_schema_only=True))
            for elem in data_new
            if extractor.find_urls(elem, with_schema_only=True)
            ]


def create_dicts_urls():

    """Creating one dictionary whit url key : response value,
    and second dictionary whit short url key : origin url value"""

    url_status_dict = {}
    origin_urls_dict = {}

    for url in get_urls_list(data_new):
        logger.info(f"Start get {url}")

        try:
            response = httpx.get(url)
            url_status_dict[url] = response.status_code
            logger.debug(f"{url} : status_code {response.status_code}")
            if origin_urls(response, url):
                logger.debug(f"{url} : {origin_urls(response, url)}")
                origin_urls_dict[url] = origin_urls(response, url)
        except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError):
            url_status_dict[url] = "404"
    print(url_status_dict, origin_urls_dict)


def origin_urls(response, url: str):

    """Get origin url from short"""

    try:
        if response.headers["Location"]:
            if (len(response.headers["Location"]) - len(url)) > 2:
                return response.headers["Location"]
    except KeyError:
        pass


def main_threads():

    """Ensures parallel operation of all functions
    for creating two dictionaries"""

    logger.add(
        "debug.log",
        format="{time:YY-MMM-D HH:mm:ss!UTC} {level} {message}",
        level="DEBUG",
        enqueue=True,
        rotation="5 minutes",
        retention="20 minutes",
    )

    tasks = []

    tasks.append(threading.Thread(target=create_dicts_urls))
    tasks[-1].start()

    for task in tasks:
        task.join()


with open(message, 'rb') as f:
    data_new = pickle.load(f)


if __name__ == "__main__":
    start = time.perf_counter()

    main_threads()

    end = time.perf_counter()
    print("Time:", end - start)
