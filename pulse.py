import argparse
import logging
import random
import time

import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

PARSER = argparse.ArgumentParser(description='Mail.ru pulse exchange traffic buster')
PARSER.add_argument('-n', help='number point to bust, max 20', default=5)
ARGS = vars(PARSER.parse_args())


click_max = ARGS['n']

pulse_widget = 'partners_widget_egorovegorru'

sitemap_url = 'https://egorovegor.ru/post-sitemap.xml'
soup = BeautifulSoup(requests.get(sitemap_url).text, features="html.parser")
posts_list = [i.text for i in soup.find_all("loc")]

ua_url = 'https://user-agents.net/random'
resonse_ua_url = requests.post(ua_url, data={'limit': '100'})
while resonse_ua_url.status_code != 200:
    time.sleep(60)
    resonse_ua_url = requests.post(ua_url, data={'limit': '100'})
soup = BeautifulSoup(resonse_ua_url.text, features="html.parser")
ua_list = [i.text for i in soup.find_all("li")[11:-1]]

for i in range(click_max):
    headers = {
        'referer': '{}'.format(random.choice(posts_list)),
        'user-agent': '{}'.format(random.choice(ua_list)),
        'accept-encoding': 'gzip, deflate',
        'accept': '*/*',
    }
    api_url = 'https://recostream.go.mail.ru/?n=10&stream_id={}&use_orig_imgs=1'.format(pulse_widget)
    response = requests.get(api_url, headers=headers)
    url = response.json()['items'][random.randint(0, 9)]['data']['pxt']['click']
    requests.get(url, headers=headers)
