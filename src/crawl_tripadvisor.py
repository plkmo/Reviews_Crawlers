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
import re
import time
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
    
    driver.get("https://www.tripadvisor.com.sg/Search?q=" + search_query)
    element = driver.find_elements_by_xpath("/html/body/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[1]")
    element[0].click()
    time.sleep(3)
    
    logger.info("Crawling...")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    reviews = soup.find_all("p", class_="partial_entry")
    return driver