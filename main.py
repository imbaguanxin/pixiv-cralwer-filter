import logging
import os.path

from collector.url_collector import Collector
from config import DOWNLOAD_CONFIG
from crawler.ranking import RankingMeta
from downloader.downloader import Downloader

if __name__ == '__main__':
    if not os.path.exists(DOWNLOAD_CONFIG["STORE_PATH"]):
        os.makedirs(DOWNLOAD_CONFIG["STORE_PATH"])

    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.INFO,
                        handlers=[
                            logging.FileHandler(DOWNLOAD_CONFIG["LOG_PATH"]),
                            logging.StreamHandler()
                        ])

    # ranking:
    rm = RankingMeta()
    artwork_ids = rm.collect_meta()
    logging.info(f"artwork ids: {artwork_ids}")

    # collecting
    collector = Collector()
    collector.add(artwork_ids)
    urls = collector.collect()
    url_str = "\n".join(urls)
    logging.info(f"img urls: {url_str}")

    # download
    downloader = Downloader()
    downloader.add(urls)
    totalsize = downloader.download()
    logging.info(f"total size of {totalsize} MB downloaded")
