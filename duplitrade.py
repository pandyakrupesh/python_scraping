from db_config import *
from datetime import datetime, date
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import random
import re
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('main.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def scroll_till_visible(driver, element_xpath):
    element = driver.find_element(By.XPATH, element_xpath)
    initial_height = driver.execute_script("return document.body.scrollHeight")

    while not element.is_displayed():
        driver.execute_script("window.scrollBy(0, 100);")

        time.sleep(2)  # Import time module for this

        current_height = driver.execute_script("return document.body.scrollHeight")

        if current_height == initial_height:
            break

        initial_height = current_height
    return driver


def get_driver():
    user = 'Duplitrade'
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument(f"user-data-dir=C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
    driver = webdriver.Chrome(options=options)
    return driver


def login_fun(driver):
    username = ''
    password = ''

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//li[@class="Navigation-item TopBar-authorization"]//a[contains(text(),"Login")]'))).click()
    except:
        pass
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="email"]'))).send_keys(username)
    except:
        pass

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))).send_keys(password)
    except:
        pass

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"Login")]'))).click()
        logger.info('click on login')

    except Exception as e:
        print(e)
    time.sleep(random.uniform(2, 10))


def main_fun():
    website = 'https://www.duplitrade.com/strategy-providers/'
    driver = get_driver()
    driver.get(website)
    try:
        login = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li[@class="Navigation-item TopBar-authorization"]//a[contains(text(),"Login")]')))
    except:
        login = ''
    if login:
        login_fun(driver)
    time.sleep(random.uniform(2, 10))
    ttl_links = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH,
                                             '//li/a[contains(text(),"Strategy Providers")]/following-sibling::div/ul/li/a')))
    if ttl_links:
        logger.info("Found all stratergy link and name")
        all_strategy_link = []
        for ttl in ttl_links[1:]:
            strategy_link = ttl.get_attribute('href')
            provider_name = ttl.accessible_name
            all_strategy_link.append([provider_name, strategy_link])
        for lnks in all_strategy_link:
            get_strategy(driver=driver, strategy_data=lnks)
            time.sleep(5)
    else:
        logger.info("couldn't find stratergy links")
    driver.quit()


def get_strategy(driver, strategy_data):
    provider_name = strategy_data[0]
    strategy_link = strategy_data[1]
    driver.get(strategy_link)
    logger.info(f"Movving to {strategy_link} stratergy")
    time.sleep(random.uniform(2, 10))

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"Historical Performance")]'))).click()
    except:
        pass

    try:
        trades_per_page = '//select[@id="trades_per_page"]'
        driver = scroll_till_visible(driver, trades_per_page)
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, trades_per_page)))
        except:
            element = None
        if element:
            element.click()
    except:
        pass

    try:
        select_value_per_page = '//select[@id="trades_per_page"]/option[@value="250"]'
        driver = scroll_till_visible(driver, select_value_per_page)

        per_page_limit = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, select_value_per_page)))
    except:
        per_page_limit = None
    if per_page_limit:
        per_page_limit.click()

    try:
        trades_per_page = '//select[@id="trades_per_page"]'

        driver = scroll_till_visible(driver, trades_per_page)
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, trades_per_page)))
        except:
            element = None
        if element:
            element.click()
    except:
        pass

    try:
        select_value_per_page = '//select[@id="trades_per_page"]/option[@value="25"]'
        driver = scroll_till_visible(driver, select_value_per_page)

        per_page_limit = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, select_value_per_page)))
    except:
        per_page_limit = None
    if per_page_limit:
        per_page_limit.click()

    try:
        trades_per_page = '//select[@id="trades_per_page"]'

        driver = scroll_till_visible(driver, trades_per_page)
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, trades_per_page)))
        except:
            element = None
        if element:
            element.click()
    except:
        pass

    try:
        select_value_per_page = '//select[@id="trades_per_page"]/option[@value="250"]'
        driver = scroll_till_visible(driver, select_value_per_page)

        per_page_limit = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, select_value_per_page)))
    except:
        per_page_limit = None
    if per_page_limit:
        per_page_limit.click()

    while True:
        time.sleep(random.uniform(2, 10))
        try:
            ttl_tr = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH,
                                                     '//a[@name="history-table"]/following-sibling::div//table/tbody/tr')))
        except:
            ttl_tr = None
        if ttl_tr:
            for tr in ttl_tr:
                data = get_details(tr=tr, provider_name=provider_name, strategy_link=strategy_link)
                if not data:
                    return False
        time.sleep(5)
        # break
        try:
            next_page = '//li[@class="Pagination-item Pagination-rarr"]'
            driver = scroll_till_visible(driver, next_page)
            move_to_next_page = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, next_page)))
        except:
            move_to_next_page = None
        if move_to_next_page:
            move_to_next_page.click()
            logger.info("Moving to next page")
        else:
            break


def get_details(tr, provider_name, strategy_link):
    currency_symbol = ''
    try:
        symbol = tr.find_element(By.XPATH, './td[1]').text
    except:
        symbol = ''
    try:
        Type = tr.find_element(By.XPATH, './td[2]').text
    except:
        Type = ''
    try:
        size = tr.find_element(By.XPATH, './td[3]').text
    except:
        size = ''
    try:
        open_time_gmt = tr.find_element(By.XPATH, './td[4]').text
    except:
        open_time_gmt = ''
    try:
        Open = tr.find_element(By.XPATH, './td[5]').text
    except:
        Open = ''
    try:
        close_time_gmt = tr.find_element(By.XPATH, './td[6]').text
    except:
        close_time_gmt = ''
    try:
        Close = tr.find_element(By.XPATH, './td[7]').text
    except:
        Close = ''
    try:
        swap = tr.find_element(By.XPATH, './td[8]').text
    except:
        swap = ''
    try:
        pips = tr.find_element(By.XPATH, './td[9]').text
    except:
        pips = ''
    try:
        new_p_l = tr.find_element(By.XPATH, './td[10]').text
        new_pl, currency_symbol = clean_value(input_string=new_p_l)
    except:
        new_pl = ''
    try:
        balance = tr.find_element(By.XPATH, './td[11]').text
        new_bal, currency_symbol = clean_value(input_string=balance)
    except:
        new_bal = ''
    check_date = check_today_date(input_date_str=close_time_gmt)
    if check_date:
        data = {
            "Provider_Name": provider_name,
            "Provider_Link": strategy_link,
            "Symbol": symbol,
            "Type": Type,
            "Size": size,
            "Open_Time_GMT": open_time_gmt,
            "Open": Open,
            "Close_Time_GMT": close_time_gmt,
            "Close": Close,
            "Swap": swap,
            "Pips": pips,
            "Net_PL": new_pl,
            "Balance": new_bal,
            "Currency_Symbol": currency_symbol}
        insert_into_table(item=data, table_name=table_name)
        print(data)
        return True
    else:
        return False


def clean_value(input_string):
    pattern = r'^([-+]?\D+)'

    match = re.search(pattern, input_string)

    currency_symbol = None

    if match:
        currency_symbol = match.group(1)

    cleaned_string = re.sub(pattern, '', input_string).strip()
    if currency_symbol:
        if "-" in currency_symbol:
            currency_symbol = currency_symbol.replace("-", "").strip()
            cleaned_string = "-" + cleaned_string.strip()
        else:
            currency_symbol = currency_symbol.strip()
            cleaned_string = cleaned_string.strip()
    else:
        currency_symbol = ""
        cleaned_string = input_string.strip()
    # print("Value:", cleaned_string)
    # print("Currency Symbol:", currency_symbol)
    return cleaned_string, currency_symbol


def check_today_date(input_date_str):
    input_datetime = datetime.strptime(input_date_str, '%Y-%m-%d %H:%M:%S')

    today_date = date.today()

    if input_datetime.date() == today_date:
        return True
    else:
        return False


if __name__ == '__main__':
    create_database()
    create_table()
    main_fun()
