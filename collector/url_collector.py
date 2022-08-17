import json
import logging
import time
from typing import Dict, Iterable, List, Set

import requests
from tqdm import tqdm

from config import DOWNLOAD_CONFIG, RANKING_CONFIG, USER_CONFIG, NETWORK_CONFIG

PIXIV_ILLUST_URL = "https://www.pixiv.net/ajax/illust/{}/pages?lang=zh"


class Collector:
    def __init__(self):
        self.id_group: Set[str] = set()
        self.headers = NETWORK_CONFIG["HEADER"]
        self.headers["cookie"] = USER_CONFIG["COOKIE"]
        self.headers["x-user-id"] = USER_CONFIG["USER_ID"]

    def add(self, ids: Iterable[str]):
        for img_id in ids:
            self.id_group.add(img_id)

    def collect_single_img(self, image_id: str):
        url: str = PIXIV_ILLUST_URL.format(image_id)
        self.headers["Referer"] = f"https://www.pixiv.net/artworks/{image_id}"
        r = requests.get(url=url, headers=self.headers)
        r_dict: Dict = json.loads(r.text)
        if "error" in r_dict and r_dict["error"]:
            logging.error(f"FAILED to GET ARTWORK {image_id}'s META data {r_dict['error']}")
            return []

        if "body" not in r_dict:
            logging.error(f"FAILED to GET ARTWORK {image_id}'s META data NO BODY!")
            return []

        body = r_dict["body"]
        return list(map(lambda art: art["urls"]["original"], body))

    def collect(self):
        result = []
        for img_id in tqdm(self.id_group, desc="Collecting image url"):
            result.extend(self.collect_single_img(img_id))
            # time.sleep(0.1)
        return result


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.INFO,
                        handlers=[
                            logging.FileHandler("test.log"),
                            logging.StreamHandler()
                        ])
    c = Collector()

    # r = c.collect_single_img("93172108")
    # print(r)

    with open("../crawler/test_illust_id.txt", "r") as f:
        id_lines = [line.strip() for line in f.readlines()]
    c.add(id_lines)
    r = c.collect()
    with open("test_img_url.txt", "w") as f:
        f.write("\n".join(r))
