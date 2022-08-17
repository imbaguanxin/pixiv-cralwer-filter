import datetime
import json
import logging
import time

from config import DOWNLOAD_CONFIG, RANKING_CONFIG, USER_CONFIG, NETWORK_CONFIG
import requests

PIXIV_RANKING_URL = "https://www.pixiv.net/ranking.php"


class RankingMeta():
    def __init__(self):
        self.date = RANKING_CONFIG["START_DATE"]
        self.n_ranking = RANKING_CONFIG["N_RANKING"]
        self.top_n = RANKING_CONFIG["TOP_N"]
        self.mode = RANKING_CONFIG["RANKING_MODE"]
        self.headers = NETWORK_CONFIG["HEADER"]
        self.headers["cookie"] = USER_CONFIG["COOKIE"]
        self.headers["Referer"] = "https://accounts.pixiv.net/"

    def collect_meta(self):
        date = self.date.strftime('%Y%m%d')
        n_count = 0
        illust_ids = []
        complete_contents = []
        while date and n_count < self.n_ranking:
            ids, cnts, next_date = self.collect_single_ranking_meta(date, self.top_n)
            n_count += 1
            illust_ids.extend(ids)
            complete_contents.extend(cnts)
            logging.info(f"COMPLETED DATE: {date}, total illust id collected: {len(illust_ids)}")
            date = next_date
            time.sleep(1)

        # with open("test_illust_id.txt", "w") as f:
        #     illust_ids = map(str, illust_ids)
        #     f.write("\n".join(illust_ids))

        return illust_ids

    def collect_single_ranking_meta(self, date: str, top_n: int):
        params = {'p': 1, 'mode': self.mode, 'date': date, 'format': 'json'}
        if "ART_TYPE" in RANKING_CONFIG:
            params['content'] = RANKING_CONFIG["ART_TYPE"]

        def single_request():
            r = requests.get(url=PIXIV_RANKING_URL, params=params, headers=self.headers)
            logging.info(f"GET: {r.url}")
            return json.loads(r.text)

        illust_ids = []
        complete_contents = []
        next_available = True
        prev_date = None
        while next_available:
            current = single_request()
            if 'error' in current:
                logging.error(f"CANNOT GET THIS RANKING PAGE: error! {params}")
                break

            # check next date
            if 'prev_date' in current:
                prev_date = current['prev_date']
            # check contents
            if 'contents' not in current:
                logging.error(f"CANNOT GET THIS RANKING PAGE: no content field {params}")
                break
            for c in current['contents']:
                if 'illust_id' in c:
                    illust_ids.append(c['illust_id'])
            complete_contents.extend(current['contents'])
            if len(illust_ids) >= top_n:
                break

            # check has next
            if 'next' not in current:
                logging.error(f"CANNOT GET THIS RANKING PAGE: no next field {params}")
                break
            next_available = current['next']
            params['p'] += 1

            time.sleep(0.5)

        # print(illust_ids)
        # with open("test_meta.json", "w") as f:
        #     json.dump(complete_contents, f)
        #
        # with open("test_illust_id.txt", "w") as f:
        #     illust_ids = map(str, illust_ids)
        #     f.write("\n".join(illust_ids))

        return illust_ids, complete_contents, prev_date


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.INFO,
                        handlers=[
                            logging.FileHandler("test.log"),
                            logging.StreamHandler()
                        ])
    rm = RankingMeta()
    # rm.collect_single_ranking_meta(rm.date.strftime('%Y%m%d'), rm.top_n)
    rm.collect_meta()
