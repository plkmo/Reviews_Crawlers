#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 12:35:00 2019

@author: weetee
"""
from src.crawl_google_reviews import crawl_google_reviews
from src.crawl_tripadvisor import crawl_tripadvisor_reviews
import logging
from argparse import ArgumentParser

logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', \
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logger = logging.getLogger('__file__')

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--search_query", type=str, default="changi+city+point", help="Search query")
    parser.add_argument("--mode", type=str, default="google_reviews", \
                        help="Options: google_reviews, tripadvisor, facebook_posts")
    parser.add_argument("--num_results", type=int, default=6000, help="Number of results to return.")
    args = parser.parse_args()
    
    if args.mode == "google_reviews":
        reviews_list = crawl_google_reviews(search_query=args.search_query, num_reviews=args.num_results)
    elif args.mode == "tripadvisor":
        reviews_list = crawl_tripadvisor_reviews(search_query=args.search_query, num_reviews=args.num_results)