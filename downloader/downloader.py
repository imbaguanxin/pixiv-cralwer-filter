import logging
import os
import re
import time
from typing import Set, Iterable
from tqdm import tqdm
import requests

from config import DOWNLOAD_CONFIG, NETWORK_CONFIG, USER_CONFIG


class Downloader:
    def __init__(self):
        self.urls: Set[str] = set()
        self.retry_times = DOWNLOAD_CONFIG["RETRY_TIMES"]
        self.fail_delay_second = DOWNLOAD_CONFIG["FAIL_DELAY_SECOND"]
        self.headers = NETWORK_CONFIG["HEADER"]
        self.headers["cookie"] = USER_CONFIG["COOKIE"]
        self.store_path = DOWNLOAD_CONFIG["STORE_PATH"]

    def add(self, urls: Iterable[str]):
        for url in urls:
            self.urls.add(url)

    def download_single_url(self, url) -> float:
        img_name = url[url.rfind("/") + 1:]
        search_result = re.search("/(\\d+)_", url)
        if search_result is None:
            logging.error(f"Bad URL in downloader: {url}")
            return 0

        image_path = os.path.join(self.store_path, img_name)
        if os.path.exists(image_path):
            logging.info(f"{img_name} exists.")
            return 0

        artwork_id = search_result.group(1)
        self.headers["Referer"] = f"https://www.pixiv.net/artworks/{artwork_id}"
        wait_time = 10
        for i in range(self.retry_times):
            try:
                r = requests.get(url, headers=self.headers, timeout=(4, wait_time))
                if r.status_code // 100 != 2:
                    logging.error(f"DOWNLOAD {img_name} failed for {i + 1} times")
                    continue

                # check completeness
                if "content-length" not in r.headers:
                    logging.info(f"{img_name} content length not found.")
                    break
                image_size = int(r.headers["content-length"])
                if len(r.content) != image_size:
                    time.sleep(self.fail_delay_second)
                    wait_time += 6
                    continue

                # write to file
                with open(image_path, "wb") as f:
                    f.write(r.content)
                    logging.debug(f"{img_name} download complete")
                return image_size / (1 << 20)

            except Exception as e:
                logging.error(f"DOWNLOAD {img_name} failed for {i + 1} times: {e}")
                time.sleep(self.fail_delay_second)

        logging.error(f"DOWNLOAD {img_name} failed!")
        return 0

    def download(self):
        size = .0
        for url in tqdm(self.urls, desc="downloading"):
            size += self.download_single_url(url)
        return size


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.INFO,
                        handlers=[
                            logging.FileHandler("test.log"),
                            logging.StreamHandler()
                        ])
    d = Downloader()
    # pic_size = d.download_single_url("https://i.pximg.net/img-original/img/2022/08/11/00/38/01/100388405_p1.jpg")

    with open("../collector/test_img_url.txt", "r") as f:
        urls = [line.strip() for line in f.readlines()]

    d.add(urls)
    d.download()
