"""
These functions have to do with getting content from the web, for example taking in a web url and extracting all the text
"""
import requests
from bs4 import BeautifulSoup
import bs4
import nltk

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
"""
Add timeout functionaltiy
"""
from functools import wraps
import errno
import os
import signal

class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator

@timeout(20, os.strerror(errno.ETIMEDOUT))
def get_content_p_tags_from_content_url(content_url):
    """
    This function extracts paragraph tags from the article HTML info
    """
    response = requests.get(content_url, headers=headers)
    soup = bs4.BeautifulSoup(response.text,'lxml')
    
    # get text
    paragraphs = soup.find_all(['p', 'strong', 'em'])

    txt_list = []
    tag_list = []
    
    for p in paragraphs:
        if p.href:
            pass
        else:
            if len(p.get_text()) > 20: # this filters out things that are most likely not part of the core content
                if '•' in p.get_text()[0]: # This excludes any bulletpoints that have been merged into a P tag
                    pass
                else:
                    tag_list.append(p.name)
                    txt_list.append(p.get_text())

    ## This snippet of code deals with duplicate outputs from the html, helps us clean up the data further
    count = 0
    article_p_tag_list = []
    for txt in txt_list:
        if txt not in article_p_tag_list:
            if len(txt) < 200:
                article_p_tag_list.append(txt)
            else:
                temp_list = nltk.sent_tokenize(txt)
                for tmp in temp_list:
                    article_p_tag_list.append(tmp)
                    
        count += 1
    return article_p_tag_list

def extract_text_from_content_url(content_url):
    ## 2 - Now get the content p-tags and combine to get the content body
    content_p_tag_list = get_content_p_tags_from_content_url(content_url)

    content_p_tag_list2 = []
    for tag in content_p_tag_list:
         if len(tag) > 75:
            content_p_tag_list2.append(tag.strip())

    content_body = ' '.join(content_p_tag_list2)
    
    return content_body