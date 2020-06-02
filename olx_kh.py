import requests
from bs4 import BeautifulSoup
import re
import json

olx_apart = 'https://www.olx.ua/uk/nedvizhimost/kvartiry-komnaty/kha/?page=[INDEX]'
olx_house = 'https://www.olx.ua/uk/nedvizhimost/doma/kha/?page=[INDEX]'
olx_land = 'https://www.olx.ua/uk/nedvizhimost/zemlya/kha/?page=[INDEX]'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
full_info = []
print('________________________________________________________')

def parsing_links():

    for INDEX in range(1, 2):
        page_rotation = olx_apart.replace('[INDEX]', str(INDEX))
        full_page = requests.get(page_rotation, headers=headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        links = []

        for a in soup.select('td.title-cell h3 > a.link'):
            links.append(a['href'])
        return links




def parsing_page(link):

    page_request = requests.get(link, headers=headers)
    soup = BeautifulSoup(page_request.text, 'html.parser')

    page_details = {}
    table = {}

    try:
	    table["uid"] = soup.select('div#offerbottombar li:contains("Номер оголошення") strong')[0].text
	    table["title"] = soup.select('div.offer-titlebox h1')[0].text
	    table["price"] = soup.select('div.pricelabel strong')[0].text
	    table["description"] = soup.select('div#textContent')[0].text
	    table["bedrooms"] = soup.select('ul.offer-details li:contains("Кількість кімнат") strong')[0].text
	    table["total_area"] = soup.select('ul.offer-details li:contains("Загальна площа") strong')[0].text
	    table["kitchen_area"] = soup.select('ul.offer-details li:contains("Площа кухні") strong')[0].text
	    table["subtype"] = soup.select('ul.offer-details li:contains("Тип об\'єкта") strong')[0].text
	    table["condition"] = soup.select('ul.offer-details li:contains("Ремонт") strong')[0].text
	    table["heating"] = soup.select('ul.offer-details li:contains("Опалення") strong')[0].text
	    page_details["photos"] = [img['href'] for img in soup.select("ul#descGallery li a")]
    except:
    	pass
        
    for item in table:
        strint = table[item].split()
        result = " ".join(strint)
        page_details[item] = result
    
    return page_details


with open("olx_content.txt", "a") as f:
	for link in parsing_links():
		full_info.append(parsing_page(link))
		print('Listing added!______________________________')

	json.dump(full_info, f)




