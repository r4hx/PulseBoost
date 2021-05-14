import logging
import os
import random
import time

import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logging.info("Инициализация переменных окружения")
BOOST_POINT = int(os.environ["BOOST_POINT"])
SLEEP_INTERVAL = int(os.environ["SLEEP_INTERVAL"])
PULSE_WIDGET_ID = os.environ["PULSE_WIDGET_ID"]
PULSE_API_URL = (
    f"https://recostream.go.mail.ru/?n=10&stream_id={PULSE_WIDGET_ID}&use_orig_imgs=1"
)
SITEMAP_URL = os.environ["SITEMAP_URL"]
USER_AGENT_URL = "https://user-agents.net/random"

logging.info("Активация бесконечного цикла")
while True:
    logging.info("Получаем ссылки из sitemap")
    soup = BeautifulSoup(requests.get(SITEMAP_URL).text, features="html.parser")
    posts_list = [i.text for i in soup.find_all("loc")]
    logging.info("Получаем список USER AGENT")
    response = requests.post(USER_AGENT_URL, data={"limit": "100"})

    while response.status_code != 200:
        logging.info("Возникла ошибка подключения к генератору USER AGENT")
        time.sleep(60)
        logging.info("Повторное соединение к сервису генерации USER AGENT")
        response = requests.post(USER_AGENT_URL, data={"limit": "100"})

    soup = BeautifulSoup(response.text, features="html.parser")
    ua_list = [i.text for i in soup.find_all("li")[11:-1]]

    logging.info("Генерируем запросы к API Mail.ru Pulse")
    for i in range(BOOST_POINT):
        headers = {
            "referer": f"{random.choice(posts_list)}",
            "user-agent": f"{random.choice(ua_list)}",
            "accept-encoding": "gzip, deflate",
            "accept": "*/*",
        }
        response = requests.get(PULSE_API_URL, headers=headers)
        url = response.json()["items"][random.randint(0, 9)]["data"]["pxt"]["click"][0]
        requests.get(url, headers=headers)
    logging.info(f"Ожидаем {SLEEP_INTERVAL} секунд")
    time.sleep(SLEEP_INTERVAL)
