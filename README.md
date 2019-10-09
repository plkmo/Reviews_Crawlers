# Review Web Crawler

## Overview
Crawls the web for social media comments of specific entity

## Contents
1) Google reviews crawler

## Requirements
Requirements: Python (3.6+), Selenium (https://selenium-python.readthedocs.io/installation.html#downloading-python-bindings-for-selenium), Selenium chromedriver (https://selenium-python.readthedocs.io/installation.html#drivers), Google Chrome browser

## Google reviews crawler
This crawler crawls through google reviews, tripadvisor for a particular search entity (search_query) and extracts the review and corresponding rating (out of 5)

Usage:
```bash
main crawler.py --search_query [default: changi+city+point]  
		--mode [google_reviews, tripadvisor]
		--num_reviews [default: 6000] 
```
Results output file will be saved in ./data/ folder.



