import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import json


def update_info():
    url = 'http://ft.org.ua/ua/program'
    ua = UserAgent()
    headers = {'User-Agent': f'{ua.random}'}
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    cards = soup.find_all(class_="button hvr-shutter-out-horizontal")
    result = {}
    id_card = 1
    for card in cards:
        onclick_value = card.get('onclick')
        buy_ticket = re.search(r"popup_ticket_banner\('(.+?)'\)", onclick_value)

        if buy_ticket:
            response = requests.get(url=buy_ticket.group(1), headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                description = soup.find("h1", class_="summary description").text.replace("’", "`").replace("–", "-")
                free_places = []
                prices_div = soup.find("div", id="prices")
                prices = {}
                for div in prices_div.find_all('div', class_='price_item'):
                    style = div['style']
                    color = style.split(':')[1].strip()
                    price = div.next_sibling.replace('-', '').strip()
                    prices[color] = price
                places = soup.findAll(class_="tooltip-button")
                date = soup.find(class_='date')
                count = 0
                for place in places:
                    fill = place.get('fill')
                    if fill and fill != 'gray':
                        free_places.append(prices[fill])
                        count += 1
                if count != 0:
                    if description in result:
                        result[description]["date"].append(date.text.replace("  ", "").strip())
                        result[description]["free_places"].append(", ".join(map(str, sorted(set(free_places)))))
                        result[description]["count_free_places"].append(count)
                        result[description]["link"].append(buy_ticket.group(1))
                    else:
                        result[description] = {
                            "id" : id_card,
                            "date": [date.text.replace("  ", "").strip()],
                            "free_places": [", ".join(map(str, sorted(set(free_places))))],
                            "count_free_places": [count],
                            "link": [buy_ticket.group(1)]
                        }

                        id_card += 1
    with open('result.json', 'w', encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)
