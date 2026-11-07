# news parser
'''

'''


import file_manipulators.generic_file_operators
import file_manipulators.json_file_operators
from cust_logging.logger import Log
Log = Log('news_parser.py')
import os
import global_vars

import feedparser

import requests
from bs4 import BeautifulSoup




# news parser
'''
    list all the entries in an rss feed
'''
def news_parser(source):
    NewsFeed = feedparser.parse(source)

    Log.log(f'number of entries {len(NewsFeed.entries)} {NewsFeed.keys()} at {source}')

    return NewsFeed



# read the content of a webpage
def read_page_body(url):
    r1 = requests.get(url)


    # Soup creation
    soup = BeautifulSoup(r1.content, 'html.parser')

    # Extract main text (selector varies by site)
    # todo update data extractor
    paragraphs = soup.find_all('p')
    if paragraphs:
        content = '\n'.join([p.get_text(strip=True) for p in paragraphs])
    else:
        # Try common article containers if <p> fails
        article_body = soup.find('div', class_='article-content') or soup.find('article')
        content = article_body.get_text(strip=True) if article_body else "Content not found"


    #Log.log(f"first bit of content = {content.rstrip()[:200]}")
    return content




# push all into news entries db
'''

'''
def push_all_into_news_entries_db():

    # get all sources from source file
    feeds = file_manipulators.generic_file_operators.read_file(global_vars.rss_feeds_file)
    feeds = [feed.strip('\n') for feed in feeds]
    Log.log(f"feeds : {feeds}")
    for feed in feeds:
        Log.log(f"pushing into news entries {feed}")
        push_into_news_entries_db(feed)

    return 1




# identify topic
'''
    identify the topic of a headline
    because a headline can span several topics, return the results as an array
'''
def identify_topic(headline):

    # parameter string santiation
    if not isinstance(headline, str):
        Log.error(f"this ({headline}) of type {type(headline)} is not a str type")
        return ["other"]

    topics = []
    Log.log(f"headline = {headline}")
    # convert to lower
    headline = headline.lower()

    ''' for each word in the headline, check the topic keywords db for what topic they would fall under'''
    headline_words = headline.split()
    for word in headline_words:
        # check the topic keywords db; comprehensive scan, since the same word could appear in several toipcs?
        Log.log(f"finding headline value for {word}")
        file_manipulators.json_file_operators.single_match_multiple_return(global_vars.topic_keywords_file, word)



        pass

    return ["other"]




#
'''
    enter entries to news db      
'''
def push_into_news_entries_db(source):

    NS = news_parser(source)

    # iterate over feeds
    ''' pull list of entries; get topic of entry; create Stories TOpic obj; add to news entries db'''

    for entry in NS.entries:
        Log.log(f"entry : {entry.title}")

        # identify the topic
        identify_topic(entry.title)

        #quit(-1)
