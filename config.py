import datetime

RANKING_CONFIG = {
    "START_DATE": datetime.date(2022, 8, 18),
    "N_RANKING": 1,
    "AVAILABLE_RANKING_MODES": [
        "daily", "weekly", "monthly",
        "male", "female",
        "daily_r18", "weekly_r18",
        "male_r18", "female_r18"
    ],
    "AVAILABLE_ART_TYPE": [
      "illust", "ugoira", "manga"
    ],
    "RANKING_MODE": "daily",
    "ART_TYPE": "illust",  # may omit for all (cannot appear with male/female)
    "TOP_N": 100,
}

OUTPUT_CONFIG = {
    "VERBOSE": False,
    "PRINT_ERROR": False
}

NETWORK_CONFIG = {
    "HEADER": {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"

    }
}

USER_CONFIG = {
    "USER_ID": "16929524",
    "COOKIE": "first_visit_datetime_pc=2021-11-30+14:44:30; yuid_b=IlV3chY; p_ab_id=9; p_ab_id_2=3; p_ab_d_id=654494356; privacy_policy_notification=0; a_type=0; b_type=1; d_type=1; ki_r=; ki_s=; login_ever=yes; ki_t=1638251087168;1640510366348;1640515957609;3;13; _gcl_au=1.1.1827514055.1660614346; __utmc=235335808; __utmz=235335808.1660614346.5.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not provided); _gid=GA1.2.947171708.1660614347; PHPSESSID=16929524_9JHwbqQRVWDu2yR9fHemOedEa4GGRwE0; device_token=7c4952a702fb3aba1946d9ef29a61b8c; c_type=25; __utmv=235335808.|2=login ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=16929524=1^9=p_ab_id=9=1^10=p_ab_id_2=3=1^11=lang=zh=1; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; __utma=235335808.1050018885.1638251070.1660614346.1660614436.6; privacy_policy_agreement=5; tag_view_ranking=0xsDLqCEW6~engSCj5XFq~m7Ok4YJ8uN~RTJMXD26Ak~MM6RXH_rlN~_vCZ2RLsY2~KN7uxuR89w~5oPIfUbtd6~fg8EOt4owo~dm8VKUFpT5~_EOd7bsGyl~iAHff6Sx6z~Xyw8zvsyR4~bLXLCzGML5~YXsA4N8tVW~0PBSfjVdjb~dbWQByG3DG~Ie2c51_4Sp~Y5Tw-5iHPe~_pwIgrV8TB~bXMh6mBhl8~SLphyXKNbQ~f5PteBDT0V~P92uTunpU8~YUuqn7At7n~TcgCqYbydo~QcneKFYI8h~VzfKuwHIlz~ETjPkL0e6r~8PDkVxzRxX~xjfPXTyrpQ~JhYN8o55n2~c15D8Cg2xk~AI_aJCDFn0~YqkiFsXxo0~JbHTIrAPZr~_hSAdpN9rx~1P--lTQMwI~gFY3XTihBM~EUwzYuPRbU~UlPyvjCQ1e~VbPCYJXdEP~TpDPYlVD87~4qWlGrZbSE~PLBZnYSxG5~SODJ0c3L2N~SWXibCVmfa~dEPPeTPGlr~3r9E8FVuwx~NT6HjMvlFJ~uC2yUZfXDc~YV0NSmOpUL~_3oeEue7S7~LC1hgCbGg1; _ga_75BBYNYN9J=GS1.1.1660623646.2.1.1660623810.0; _ga=GA1.2.1050018885.1638251070; __cf_bm=Knh.wio.CKzMu5nfYAXVosHU3xPkGLmPX.JEe5EJT5g-1660625588-0-AZRh4C7cmGRBy6t+qpaUx6e0cd5okhrKAw1eBIEExhRqIrRE208BkQzw9audepqEkqNGDz6r9He76tMkr32MFHQYXXNk/8kOwWq8Cx43PaJF",
}

DOWNLOAD_CONFIG = {
    "STORE_PATH": f"/home/gx/repo/pixiv/image/{RANKING_CONFIG['START_DATE'].strftime('%Y%m%d')}-{RANKING_CONFIG['RANKING_MODE']}",
    "LOG_PATH": f"/home/gx/repo/pixiv/image/{RANKING_CONFIG['START_DATE'].strftime('%Y%m%d')}-{RANKING_CONFIG['RANKING_MODE']}/log",
    "RETRY_TIMES": 5,
    "WITH_TAG": False,
    "FAIL_DELAY_SECOND": 2,
    "N_THREAD": 4,
    # waiting time after thread start
    "THREAD_DELAY_SECOND": 2
}
