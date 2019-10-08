#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 14:45:08 2019

@author: weetee
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re
import time
import math
from bs4 import BeautifulSoup
import os
import pickle
from tqdm import tqdm
import logging

logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', \
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logger = logging.getLogger('__file__')

def save_as_pickle(filename, data):
    completeName = os.path.join("./data/",\
                                filename)
    with open(completeName, 'wb') as output:
        pickle.dump(data, output)
        
def crawl_tripadvisor_reviews(search_query="changi+city+point", num_reviews=100):
    logger.info("Initialzing webdriver...")
    driver = webdriver.Chrome()
    timeout = 13
    
    # Search entity, then go to main entity reviews page (which opens in a new tab)
    driver.get("https://www.tripadvisor.com.sg/Search?q=" + search_query)
    time.sleep(7)
    element = driver.find_elements_by_xpath("/html/body/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[1]")
    element[0].click()

    ### Switch to reviews tab
    driver.switch_to.window(driver.window_handles[1])
    logger.info("Crawling...")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    reviews_total = int(re.search("of (\d+) reviews", \
                                  soup.find_all("div", class_="pagination-details")[0].text)[1])
    logger.info("Total %d reviews found." % reviews_total)
    
    reviews_list = []
    for i in tqdm(range(math.ceil(reviews_total/10))):
        # expand reviews
        elements = driver.find_elements_by_class_name('ulBlueLinks')
        for element in elements:
            for _ in range(3): # try 3 times per expansion element
                try:
                    element.click()
                    time.sleep(1)
                    #element_present = EC.presence_of_element_located((By.ID, element.id))
                    WebDriverWait(driver, timeout)
                except Exception as e:
                    print(e)
                
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        reviews_blocks = soup.find_all("div", class_="rev_wrap ui_columns is-multiline")
        
        for review_block in reviews_blocks:
            title = review_block.find_all("span", class_="noQuotes")[0].text
            review = review_block.find_all("p", class_="partial_entry")[0].text
            star = review_block.find_all("span", class_=re.compile("ui_bubble_rating bubble_.+"))[0]
            star = int(re.search("bubble_([\d+]+)", str(star))[1])/10
            reviews_list.append((title, review, star))
        
        # go to next page nav next taLnk ui_button primary
        next_page1 = driver.find_elements_by_class_name("nav")
        next_page2 = driver.find_elements_by_class_name("next")
        next_page = list(set(next_page1).intersection(set(next_page2)))
        
        try:
            next_page[0].click()
            WebDriverWait(driver, timeout)
        except Exception as e:
            print(e)
    
    driver.close()
    
    save_as_pickle("tripadvisor_reviews_%s.pkl" % search_query.replace("+", "_"), reviews_list)
    with open("./data/tripadvisor_reviews_%s.txt" % search_query.replace("+", "_"), "w", encoding="utf8") as f:
        for title, review, star in tqdm(reviews_list):
            f.write(title + " " + "\"" + review + "\"" + " %s" % str(star) + "\n")
    logger.info("Done and saved!")
    
    return reviews_list