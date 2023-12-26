import os

import pandas as pd
import pymongo
import requests
import json


def get_product_list(access_token):
    headers = {
        'CJ-Access-Token': access_token,
    }
    next_page = True
    while next_page:
        page = 1
        response = requests.get(f'https://developers.cjdropshipping.com/api2.0/v1/product/list?pageNum={page}',
                                headers=headers)
        if response.status_code != 200:
            return
        content = json.loads(response.text)
        try:
            all_data = content['data']['list']
        except:
            all_data = []
        if all_data:
            for data in all_data:
                try:
                    pid = data['pid']
                except:
                    pid = ''
                if pid:
                    if pid not in all_pids:
                        product_details(pid=pid)
                        print({"pid": pid})
                        all_pids.append({"pid": pid})
            page += 1
        else:
            break


def product_details(pid):
    headers = {
        'CJ-Access-Token': access_token,
    }
    params = {
        'pid': pid,
    }
    response = requests.get('https://developers.cjdropshipping.com/api2.0/v1/product/query', params=params,
                            headers=headers)
    if response.status_code != 200:
        return
    content = json.loads(response.text)
    try:
        Title = content['data']['productNameEn']
    except:
        Title = ''
    try:
        Handle = Title.lower().replace(',', '').replace(' ', '-').replace('--', '-')
    except:
        Handle = ''
    try:
        body = content['data']['description']
    except:
        body = ''
    try:
        Product_Category = content['data']['categoryName']
    except:
        Product_Category = ''
    try:
        Type = content['data']['productType']
    except:
        Type = ''
    try:
        Published = content['data']['createrTime']
    except:
        Published = ''
    try:
        Image_Src = content['data']['productImage']
    except:
        Image_Src = ''
    try:
        Image_Position = len(Image_Src)
    except:
        Image_Position = ''
    try:
        status = content['data']['status']
    except:
        status = ''
    try:
        Tags = ', '.join(content['data']['productProEnSet']).strip()
    except:
        Tags = ''
    try:
        listedNum = content['data']['listedNum']
    except:
        listedNum = ''
    if listedNum == 0:
        listedNum = ''
    try:
        ttl_variant = content['data']['variants']
    except:
        ttl_variant = []
    if ttl_variant:
        for variant in ttl_variant:
            try:
                Variant_SKU = variant['variantSku']
            except:
                Variant_SKU = ''
            try:
                Variant_Grams = variant['variantWeight']
            except:
                Variant_Grams = ''
            try:
                Variant_Price = variant['variantSellPrice']
            except:
                Variant_Price = ''
            try:
                vid = variant['vid']
            except:
                vid = ''
            try:
                logisticPrice = get_logisticPrice(vid)
            except:
                logisticPrice = ''
            details = {"Handle": Handle,
                       "Title": Title,
                       "Body": body,
                       "Product_Category": Product_Category,
                       "Type": Type,
                       "Tags": Tags,
                       "Published": Published,
                       "Image_Src": Image_Src,
                       "Image Position": Image_Position,
                       "Variant_SKU": Variant_SKU,
                       "Variant_Grams": Variant_Grams,
                       "Variant_Price": Variant_Price,
                       "status": status,
                       "Total_Price": logisticPrice,
                       "listedNum": listedNum,
                       "Vendor": '',
                       "Variant Inventory Tracker": '',
                       "Variant Inventory Policy": '',
                       "Variant Fulfillment Service": '',
                       "Variant Compare At Price": '',
                       "Variant Requires Shipping": '',
                       "Variant Taxable": '',
                       "Variant Barcode": '',
                       "Image Alt Text": '',
                       "Gift Card": '',
                       "SEO Title": '',
                       "SEO Description": '',
                       "Google Shopping / Google Product Category": ''}
            get_excel(items=details)
    else:
        try:
            logisticPrice = get_logisticPrice(pid)
        except:
            logisticPrice = ''
        details = {"Handle": Handle,
                   "Title": Title,
                   "Body": body,
                   "Product_Category": Product_Category,
                   "Type": Type,
                   "Tags": Tags,
                   "Published": Published,
                   "Image_Src": Image_Src,
                   "Image Position": Image_Position,
                   "Variant_SKU": '',
                   "Variant_Grams": '',
                   "Variant_Price": '',
                   "status": status,
                   "listedNum": listedNum,
                   "Total_Price": logisticPrice,
                   "Vendor": '',
                   "Variant Inventory Tracker": '',
                   "Variant Inventory Policy": '',
                   "Variant Fulfillment Service": '',
                   "Variant Compare At Price": '',
                   "Variant Requires Shipping": '',
                   "Variant Taxable": '',
                   "Variant Barcode": '',
                   "Image Alt Text": '',
                   "Gift Card": '',
                   "SEO Title": '',
                   "SEO Description": '',
                   "Google Shopping / Google Product Category": ''}
        get_excel(items=details)


def get_logisticPrice(vid):
    header = {
        'Content-Type': 'application/json',
        'CJ-Access-Token': access_token,
    }

    json_data = {
        'startCountryCode': 'US',
        'endCountryCode': 'US',
        'products': [
            {
                'quantity': 2,
                'vid': vid,
            },
        ],
    }

    response = requests.post(
        'https://developers.cjdropshipping.com/api2.0/v1/logistic/freightCalculate',
        headers=header,
        json=json_data,
    )
    content = json.loads(response.text)
    try:
        logisticPrice = content['data'][0]['logisticPrice']
    except:
        logisticPrice = ''
    return logisticPrice


def get_excel(items):
    filename = 'CJ_Dropshipping_Product_details.xlsx'
    if not os.path.exists(f'{filename}'):
        df = pd.DataFrame([items])
        df.to_excel(f'{filename}', index=False, sheet_name='Sheet1')
    else:
        existing_data = pd.read_excel(f'{filename}', engine='openpyxl')
        combined_data = pd.concat([existing_data, pd.DataFrame([items])], ignore_index=True)
        with pd.ExcelWriter(f'{filename}', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            combined_data.to_excel(writer, index=False, sheet_name='Sheet1')


if __name__ == '__main__':
    insert_col = []
    all_pids = []
    try:
        access_token = open("access_token.txt", "r").read()
    except:
        access_token = ''
    try:
        if access_token == '':
            print("Get Access Token")
        else:
            get_product_list(access_token=access_token)
    except Exception as e:
        print(e)
        pass
