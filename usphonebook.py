import os

import pandas as pd
import requests
from lxml import html
from uszipcode import SearchEngine
from geopy.geocoders import Nominatim

headers = {
    'authority': 'www.usphonebook.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,fr;q=0.8',
    'cache-control': 'max-age=0',
    'referer': 'https://www.usphonebook.com/',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}


def import_from_excel():
    df = pd.read_excel('Data BOOM LA City Addresses v1.xlsx')
    for i in df.values:
        property_add = i[0].title()
        property_address = i[0].replace('-', '').replace(' ', '-').replace('/', '').lower()
        zipcode = str(int(i[1]))
        city_name = find_city(zipcode=zipcode)
        country_name = city_name[1].lower()
        city_name = city_name[0].lower().replace(' ', '-')
        website_base = f'{property_address}_{city_name}-{country_name}'
        main_fun(website_base=website_base, property_add=property_add, zipcode=zipcode)


def find_city(zipcode):
    search = SearchEngine()

    zip_code = zipcode

    result = search.by_zipcode(zip_code)

    city_name = result.major_city
    country_name = result.state
    return city_name, country_name


def main_fun(website_base, property_add, zipcode):
    page = 1
    while True:
        site_base = f'https://www.usphonebook.com/address/{website_base}?page={page}'
        site_li = {'link': site_base}
        save_link(site_li)
        print(site_li)
        scrape_do = f"http://api.scrape.do?token=522399431c7f4facb198bcb967ecd4be917f3d5226c&url={site_base}"
        website = scrape_do
        response = requests.get(website, headers=headers)
        content = html.fromstring(response.text)
        ttl = content.xpath('//div[@class="success-wrapper-padding"]')
        if ttl:
            for t in ttl:
                text = t.xpath('.//span[contains(text(),"Lives at")]/following-sibling::span/a/text()')[0].strip()
                if property_add in text and zipcode in text:
                    link = 'https://www.usphonebook.com' + t.xpath('.//div[@class="address-view-report-div"]/a/@href')[
                        0]
                    get_details(link=link, property_add=property_add, zipcode=zipcode)
            page += 1
        else:
            break


def get_details(link, property_add, zipcode):
    scrape_do = f"http://api.scrape.do?token=522399431c7f4facb198bcb967ecd4be917f3d5226c&url={link}"
    response = requests.get(scrape_do, headers=headers)
    content = html.fromstring(response.text)
    try:
        address = ''.join(content.xpath(
            '//div[@class="address-content"]/span[contains(text(),"Address")]/parent::div/a/p/text()')).strip()
    except:
        address = ''
    if property_add in address and zipcode in address:
        try:
            name = ''.join(content.xpath('//h1[@class="ls_header-5"]/span/text()')).strip()
        except:
            name = ''

        try:
            number = ''.join(content.xpath(
                '//div[@class="address-content"]/span[contains(text(),"Phone")]/parent::div/div//a/span/text()')).strip()
        except:
            number = ''
        if number == '' and name == '':
            return

        data = {"Property_address": property_add,
                "Zipcode": zipcode,
                "Name": name,
                "Number": number}
        convert_to_csv(data)
        print(data)


def convert_to_csv(data):
    df = pd.DataFrame([data])
    filename = 'sample.csv'
    if os.path.exists(filename):
        df.to_csv(filename, mode="a", index=False, header=False, encoding='utf-8')
    else:
        df.to_csv(filename, mode='a', index=False, header=True, encoding='utf-8')


def save_link(site_li):
    df = pd.DataFrame([site_li])
    filename = 'site_links.csv'
    if os.path.exists(filename):
        df.to_csv(filename, mode="a", index=False, header=False, encoding='utf-8')
    else:
        df.to_csv(filename, mode='a', index=False, header=True, encoding='utf-8')


if __name__ == '__main__':
    import_from_excel()
