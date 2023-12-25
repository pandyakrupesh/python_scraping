import json
import multiprocessing
import os
import re
import sys
from datetime import datetime
from db_config import *
import pandas as pd
import requests
from lxml import html
import threading


def company_parse(company_url):
    import requests

    headers = {'authority': 'www.linkedin.com',
               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
               'accept-language': 'en-US,en;q=0.9',
               'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
               'sec-ch-ua-mobile': '?0',
               'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate',
               'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36', }

    response = requests.get(company_url, headers=headers)
    doc = html.fromstring(response.text)
    data = doc.xpath('//*[@type="application/ld+json"]//text()')[0].strip()
    try:
        js_data = json.loads(data)
    except:
        js_data = None

    try:
        try:
            headquarters_locality = js_data['address']['addressLocality']
        except:
            headquarters_locality = ''
        try:
            headquarters_region = js_data['address']['addressRegion']
        except:
            headquarters_region = ''
        headquarters = headquarters_locality + ' ' + headquarters_region
    except:
        headquarters = ''
    try:
        num_of_employess = js_data['numberOfEmployees']['value']
    except:
        num_of_employess = ''

    return headquarters, num_of_employess


def job_link(link):
    item = {}
    res1 = requests.get(link)
    retry_count = 0
    while res1.status_code != 200:
        if retry_count == 3:
            break
        res1 = requests.get(link)
        retry_count += 1

    if res1.status_code != 200:
        convert_to_csv(link)
        return False

    try:
        dom = html.fromstring(res1.text)
    except:
        return False
    try:
        item['Job_Post_URL'] = link
    except:
        item['Job_Post_URL'] = ''
    try:
        title = '\n'.join(dom.xpath(
            '//h1[@class="top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title"]/text()')).strip()
    except:
        title = ''

    if "Node.Js" in title or "Node JS" in title or "Node" in title:
        if not ".NET" in title or not "Java" in title or not "C#" in title or not "C++" in title or not "C" in title or not "PHP" in title or not "GO" in title or not "Rust" in title or not "Kotlin" in title or not "Ruby" in title:
            item['Job_Post_Title'] = title
            try:
                company_url = dom.xpath('//a[@class="topcard__org-name-link topcard__flavor--black-link"]/@href')[0]
                item['Company_Linkedin_URL'] = company_url.split('?')[0].strip()
            except:
                item['Company_Linkedin_URL'] = ''
            try:
                item['Industry'] = '\n'.join(
                    dom.xpath('//*[contains(text(),"Industries")]/following-sibling::span//text()')).strip()
            except:
                item['Industry'] = ''
            if item['Industry'] == '':
                try:
                    item['Industry'] = re.findall(',"industry":"(.*?)",', res1.text)[0]
                except:
                    item['Industry'] = ''
            try:
                item['Company_Name'] = '\n'.join(dom.xpath(
                    '//h4[@class="top-card-layout__second-subline font-sans text-sm leading-open text-color-text-low-emphasis mt-0.5"]/div/span[@class="topcard__flavor"]/a/text()')).strip()
            except:
                item['Company_Name'] = ''
            try:
                item['Job_Post_Text'] = '\n'.join(
                    dom.xpath('//div[@class="description__text description__text--rich"]//text()')).replace('\n',
                                                                                                            '').strip().replace(
                    'how more', '').replace('Show less', '').replace('\xa0', '').replace('BR', '').replace('S  ',
                                                                                                           '').strip()
            except:
                item['Job_Post_Text'] = ''
            comp_data = company_parse(item['Company_Linkedin_URL'])
            item['Company_Headquarters'] = comp_data[0]
            item['Company_Number_of_Employees'] = comp_data[1]

            check_word = [".NET", "C#", "C++", "PHP", "Ruby", "Rust", "Kotlin"]
            found_match = False
            for c in check_word:
                if c.lower() in item['Job_Post_Text'] or c.upper() in item['Job_Post_Text']:
                    found_match = True
                    break
            if not found_match:
                insert_into_table(item=item, table_name=table_name)


def main(keyword, location):
    start = 0
    next = True
    while next:
        print(f"in page {start}, keyword : {keyword}, location: {location}")
        headers = {'authority': 'www.linkedin.com', 'accept': '*/*',
                   # 'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                   'accept-language': 'en-US',
                   # 'cookie': 'bcookie="v=2&24dd2f2c-acb2-4222-8668-6b304f3d3958"; li_sugr=22a595c6-aad7-4925-8556-9b65ebec3520; bscookie="v=1&20230704044004c7cec674-6409-4f2e-84b8-fbe0c18de5e9AQGvgCSQOaSHofwwPbGggUcyDF0db8N4"; G_ENABLED_IDPS=google; li_gc=MTswOzE2OTA4ODQ4NTI7MjswMjFgR4Nfiuiht8amCQtm5tgIEyMI9aMrTCLxaJfhCHjGwg==; fid=AQG9R47rvjUh6AAAAYo_3V8vlxT4K6py6LOrXmit11ZLvUTk1xD3xIIKZ1ZPBa2iv4eWqeopUalPSA; UserMatchHistory=AQIJTvs6xQ9BlQAAAYpPCKy0amWNVNnDKLGFlexyfGPc10rL8sFguRD9acf6Xz3PdzUAeeF7sayMwA; AnalyticsSyncHistory=AQLzmgt3i95dgQAAAYpPCKy0L80Q31PwMmB-IqgvMBB5j2tfmbnB9I5YXfa2twB6TQonhzjk73yjETluQN4prg; lidc="b=OGST07:s=O:r=O:a=O:p=O:g=2622:u=1:x=1:i=1693543083:t=1693629483:v=2:sig=AQEBZTzCcUWoOFiRYIHNiQluJIOOiP1f"; JSESSIONID=ajax:2277979240440583776; lang=v=2&lang=en-us; g_state={"i_l":2,"i_p":1693644475439}; chp_token=AgEAcf881fkrewAAAYpP7rMHPSSRXXnLZz8CcRkDkwTThxPtbSl5vUmqIfGRueyMvzwLbJN5tgY9v640UzUp_t0qHBlKWih2h5_jqQ; fcookie=AQFWruoV7vaiAAAAAYpP7sgXOlu-wj8msZSUBMnYKeMSPa4Z471B1QZUlvKyU4O6SHK5QGQJV0VKmAutFHW9NXGwsWCWbWwz6dOvRtb8FC2uVt-Dsw3MaRT68Fu8UQFOrDaVfz0ahoHPMr9Qedc80XIimkSMH4s28kn6sD38sa9ExGkUloRicI8P9BpFP2tSX-e35TJPPR5N8JFUCa7VQShc2y9uA1pSNxvcZu0geWC_4f4TNoxW3LLZmQDoj5ESP6bcInDz1XI9XBRfGKE4/U0in3dD45ihEf+g6vs1jjPSfsnsfaBF1dhZuntnpqVhXfG3iNDIG7tVplbA==',
                   'csrf-token': 'ajax:2277979240440583776',
                   'referer': 'https://www.linkedin.com/jobs/search?keywords=Node.Js&location=worldwide&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
                   'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
                   'sec-ch-ua-mobile': '?0',
                   'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors',
                   'sec-fetch-site': 'same-origin',
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36', }

        params = {'keywords': keyword, 'location': location, 'geoId': '',
                  'trk': 'public_jobs_jobs-search-bar_search-submit', 'position': '1', 'pageNum': '0',
                  'start': f'{start}', }

        response = requests.get('https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search', params=params,
                                headers=headers, )
        retry_count = 0
        while response.status_code != 200:
            if retry_count == 3:
                break
            response = requests.get('https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search',
                                    params=params, headers=headers, )
            retry_count += 1


        try:
            res = html.fromstring(response.text)
        except:
            res = ''
        if not res == '':
            links = res.xpath(
                '//a[@class="base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]"]/@href')
            if not links:
                next = False
            for link in links:
                job_link(link)
            start += 25
        else:
            print(f"in page document is empty, keyword : {keyword}, location: {location}, current_page: {response.url}")
            break


def convert_to_csv(link):
    data = {'url': link}
    df = pd.DataFrame([data])
    filename = 'failed_links.csv'
    if os.path.exists(filename):
        df.to_csv(filename, mode="a", index=False, header=False, encoding='utf-8')
    else:
        df.to_csv(filename, mode='a', index=False, header=True, encoding='utf-8')


if __name__ == '__main__':
    create_database()
    create_table()
    start_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    print(start_time)
    keyword = sys.argv[1]
    location = sys.argv[2]
    print(keyword)
    print(location)
    main(keyword, location)
