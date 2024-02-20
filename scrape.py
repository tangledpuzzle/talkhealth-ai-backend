from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
from organize_outlook_result import organize_outlook
import os

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def init():
    create_directory('temp')
    create_directory('result')
    chrome_options = Options()
    # chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--disable-application-cache")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1366, 768)

    return driver

def login(driver):

    # driver.get(link)
    try:
        WebDriverWait(driver, 99999).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="People"]'))
        )
        return 1
    except Exception as e:
        return 0

def scrape_users(driver, log_data):
    people_button = driver.find_element(By.XPATH, '//button[@aria-label="People"]')
    people_button.click()

    all_users_button = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@title='All Users']"))
    )
    all_users_button.click()
    
    scroll_panel = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.zNwRz"))
    )

    driver.execute_script("arguments[0].scrollTop += arguments[1];", scroll_panel, log_data['scroll_position'])

    count = log_data['count']
    page_index = log_data['page_index']
    while page_index < 99999:
        
        try:
            if page_index % 100 == 0 and page_index != 0:
                driver.execute_script("caches.keys().then(function(names) { for (let name of names) { caches.delete(name); } });")
                # driver.delete_all_cookies()
                organize_outlook(page_index)

            users = driver.find_elements(By.CSS_SELECTOR, "div.DXpY5")
            users = users[2:] if page_index > 0 else users

            for user in users:
                try:
                    user.click()
                    side_element = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, '//div[contains(@class, "dcv0y") and contains(@class, "PQm58")]'))
                    )

                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.TAG_NAME, 'h1'))
                    )
                    time.sleep(0.1)
                    html_content = side_element.get_attribute("innerHTML")

                    info_panel = BeautifulSoup(html_content, 'html.parser')

                    name = info_panel.find('h1').text.strip()

                    user_info = {'name': name}

                    contact_info_panel = info_panel.select('div[class^="list-"]')[-1]

                    contact_info_list = contact_info_panel.select('div[class^="listItemHorizontal"]')

                    for contact_info in contact_info_list:
                        key_tag = contact_info.find('h3')
                        value_tag = key_tag.find_next_sibling('span')
                        key = key_tag.text.strip()
                        value = value_tag.text.strip()
                        user_info[key] = value
                    
                    with open(f"./temp/{count}.json", 'w', encoding= 'utf-8') as f:
                        json.dump(user_info, f, indent= 4)


                    count += 1
                    scroll_position = driver.execute_script("return arguments[0].scrollTop;", scroll_panel)
                    with open("log.json", "w") as f:
                        json.dump(
                            {
                                'count': count, 
                                'scroll_position': scroll_position, 
                                'page_index': page_index
                            }, 
                            f, 
                            indent= 4
                        )
                
                except Exception as e:
                    pass

            driver.execute_script("arguments[0].scrollTop += arguments[0].offsetHeight;", scroll_panel)
            time.sleep(2)
            page_index += 1

        except Exception as e:
            print(e)
            organize_outlook(page_index)
            return

try:
    with open("log.json", "r") as f:
        log_data = json.load(f)
except Exception as e:
    log_data = {
        'count': 0, 
        'scroll_position': 0, 
        'page_index': 0
    }
    
print(log_data)
    
driver = init()
if login(driver):
    scrape_users(driver, log_data)