#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 11:47:50 2020

@author: weetee
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import re
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
import logging

tqdm.pandas('prog_bar')


logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', \
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logger = logging.getLogger('__file__')

## Login credentials
user_txt_path = '../data/user.txt'

with open(user_txt_path, 'r', encoding='utf8') as f:
    username = f.readline()
    password = f.readline()

url = 'https://www.facebook.com/pg/ChannelNewsAsia/posts/?ref=page_internal'
keywords = ['coronavirus', 'covid', 'covid-19']

driver = webdriver.Chrome()
driver.get(url)

username_field = driver.find_element_by_id('email')
password_field = driver.find_element_by_id('pass')
username_field.send_keys(username)
password_field.send_keys(password)
submit_field = driver.find_element_by_id('u_0_3')
submit_field.send_keys(Keys.ENTER)

posts_data = []

time.sleep(5)
search_field = driver.find_element(by=By.CLASS_NAME, value='_58al')
search_field.send_keys('covid')
search_field.send_keys(Keys.ENTER)

time.sleep(5)
#comments_buttons = driver.find_elements(by=By.PARTIAL_LINK_TEXT, value='comment')
#comments_buttons[2].click()
soup = BeautifulSoup(driver.page_source, "html.parser")
comments = soup.find_all("span", class_='_3l3x')
for c in comments:
    print(c.text)

'''
# click open all comments & expand
comments_buttons = driver.find_elements(by=By.PARTIAL_LINK_TEXT, value='comment')
for b in comments_buttons:
    try:
        b.click()
    except:
        pass
 
soup = BeautifulSoup(driver.page_source, "html.parser")
posts = soup.find_all('div', class_='_4-u2 _4-u8')
comments = soup.find_all("span", class_='_3l3x')

post_title = posts[1].find_all('div', class_="_6ks")[0].a.get('aria-label')
post_summary = posts[1].find_all('div', class_="_5pbx userContent _3576")[0].text
post_data = {'title': post_title, 'comments': []}

if any([kw.lower() in post_title.lower() for kw in keywords]) or \
    any([kw.lower() in post_summary.lower() for kw in keywords]):

    comments_button = posts[1].find_all('a', class_='_3hg- _42ft')
    
    if len(comments_button) > 0:
        num_comments = int(re.search('\d+', comments_button[0].text)[0])
        posts[0].find_all("span", class_='_3l3x')
driver.close()
'''