import requests
from bs4 import BeautifulSoup
import re
import json


xan_apart_rent = "http://xan.com.ua/ru/rent/dwelling/Kharkov/flats?page=[INDEX]"
xan_apart_sale = "http://xan.com.ua/ru/flats/find/Kharkov?page=[INDEX]"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
full_info = []


def parsing_links():

    for INDEX in range(1,2):
        page_rotation = xan_apart_sale.replace('[INDEX]', str(INDEX))
        full_page = requests.get(page_rotation, headers=headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')

        links = []

        for a in soup.select('div.w-contentBlog li > a'):
            links.append(a['href'])
        return links


def parsing_page(link):
    
    full_page = requests.get(link, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    page_details = {}
    table = {}



    page_details['uid'] = soup.select('article header p span')[0].text.split()[1]
    page_details['ref'] = soup.select('article header p span')[0].text.split()[1]
    page_details['contact'] = soup.select('div.g-contact-description h1')[0].text
    table['title'] = soup.select('article header h1')[0].text
    table['location'] = soup.select('article header p')[0].text
    table['descroption'] = soup.select('div.cont-advDetails-top > p')[0].text
    table['price'] = soup.select('div.cont-advDetails-details tr:contains("за объект") td:last-child')[0].text
    table['condition'] = soup.select('div.cont-advDetails-details tr:contains("Ремонт") td:last-child')[0].text
    table['rooms'] = soup.select('div.cont-advDetails-details tr:contains("Число комнат") td:last-child')[0].text
    table['total_area'] = soup.select('div.cont-advDetails-details tr:contains("Площадь общая") td:last-child')[0].text
    table['flour'] = soup.select('div.cont-advDetails-details tr:contains("Этаж") td:last-child')[0].text
    table['features'] = soup.select('div.cont-advDetails-details tr:contains("Этаж") td:last-child')[0].text
   

    _photos = soup.select('div.cont-advDetails-top figure')[0]['data-media']
    photos_soup = (json.loads(str(_photos)))
    photos = []

    for item in photos_soup:
        photos.append(item["src"])

    page_detail["photos"] = photos


    for item in table:
        strint = table[item].split()
        result = " ".join(strint)
        page_details[item] = result

    return page_details

with open('xan.txt', 'w') as f:
    for link in parsing_links():
        full_info.append(parsing_page(link))
        print('Page are parsed')
    json.dump(full_info, f)
