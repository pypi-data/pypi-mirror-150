"""
These functions all have to do with anything and everything twitter!
"""
from datetime import datetime, timedelta
import random
import twint
import re
import uuid
import json
import nest_asyncio
import pandas as pd
import numpy as np
from collections import Counter
nest_asyncio.apply()

from functions import search_engine as search
from functions import general as gen
from blov_article.functions import web_content_extraction as web_ext

def generate_cutoff_and_search_date(cut_off_h_diff, search_h_diff):
    """
    This is designed for getting tweets within a time window less than 24 hours
    """
    # Subtract the search/cutoff diffs
    search_date = datetime.today() - timedelta(hours=search_h_diff)
    cutoff_date = datetime.today() - timedelta(hours=cut_off_h_diff)

    # Create the search date string
    search_dt = str(search_date.date())
    search_hr = search_date.hour
    search_date_str = '%s %s:00:00' % (search_dt, search_hr)

    # Create the cutoff date string
    cutoff_dt = str(cutoff_date.date())
    cutoff_hr = cutoff_date.hour
    cutoff_date_str = '%s %s:00:00' % (cutoff_dt, cutoff_hr)
    
    return search_date_str, cutoff_date_str

def twint_to_pandas(columns):
    return twint.output.panda.Tweets_df[columns]

def get_tweets_from_search_term(search_term, min_replies, verified, num_tweets, since_date_str):
    """
    This functionality get all tweets from a handle given a specific date
    and then gets the 2500 latest replies
    """
    c = twint.Config()
    if verified:
        c.Verified = True
    else:
        c.Verified = False
    c.Min_replies = min_replies
    c.Since = since_date_str
    c.Pandas = True
    c.Search = search_term # get replies to this twitter handle
    c.Hide_output = True
    c.Limit = num_tweets
    c.Store_csv = True
    twint.run.Search(c)
    replies_df = twint.storage.panda.Tweets_df
    
    return replies_df

def get_latest_tweets_from_handle(username, num_tweets):

    # Configure
    c = twint.Config()
    c.Verified = False
    c.Min_replies = 0
    c.Pandas = True
    c.Username = username
    c.Hide_output = True
    c.Limit = num_tweets

    # Run
    twint.run.Search(c)

    tweet_df = twint.storage.panda.Tweets_df
        
    return tweet_df

def get_latest_tweets_from_handle_from_date(username, num_tweets, date):

    c = twint.Config()
    c.Username = username
    c.Limit = num_tweets
    c.Pandas = True
    c.Since = date
    c.Hide_output = True

    twint.run.Search(c)
    tweet_df = twint.storage.panda.Tweets_df
    
#     try:
#         tweet_df = twint_to_pandas(['id', 'conversation_id', 'date', 'tweet', 'language', 'hashtags', 
#                'username', 'name', 'link', 'urls', 'photos', 'video',
#                'thumbnail', 'retweet', 'nlikes', 'nreplies', 'nretweets', 'source'])
#     except Exception as e:
#         print(e)
#         tweet_df = pd.DataFrame()
        
    return tweet_df

def get_tweet_df_urls(tweet_df):
    """
    This function takes a tweet_df from a twint search and then returns all the
    urls across all the tweets
    """
    # Build functionality that gets all the urls from a tweet_df
    url_list = []
    for i in range(len(tweet_df)):
        tweet_urls = tweet_df.iloc[i]['urls']
        url_list += tweet_urls

    return url_list


def get_last_24_tweets_for_handle(twitter_handle):
    """
    This function takes in a twitter handle and gets all the tweets generated in the last 24 hours
    * Later build a function that also does this for a search term as well
    """
    ## Get all the tweets from them in the last 24 hours 
    cutoff_dt = datetime.now() - timedelta(1)
    search_dt = datetime.now() - timedelta(2) # so we capture the content from yday as well
    search_date = datetime.strftime(search_dt, '%Y-%m-%d')
    num_tweets = 5000 
    tweet_df = get_latest_tweets_from_handle(twitter_handle, num_tweets, search_date)

    # Get tweets in the last 24 hours
    within_24_inds = []
    for i in range(len(tweet_df)):
        tweet_date = tweet_df.iloc[i]['date']
        tweet_date = datetime.strptime(tweet_date, '%Y-%m-%d %H:%M:%S')
        if tweet_date >= cutoff_dt:
            within_24_inds.append(i)
    last_24_tweet_df = tweet_df.iloc[within_24_inds]
    
    return last_24_tweet_df


def get_last_hour_tweets_for_handle(twitter_handle):
    """
    This function takes in a twitter handle and gets all the tweets generated in the last hour
    * Later build a function that also does this for a search term as well
    """
    ## Get all the tweets from them in the last hour
    cutoff_dt = datetime.now() - timedelta(hours=1)
    search_dt = datetime.now() - timedelta(hours=2) # so we capture the content from 2 hours ago as well
    search_date = datetime.strftime(search_dt, '%Y-%m-%d')
    num_tweets = 5000 
    tweet_df = get_latest_tweets_from_handle(twitter_handle, num_tweets, search_date)

    # Get tweets in the last hour
    within_24_inds = []
    for i in range(len(tweet_df)):
        tweet_date = tweet_df.iloc[i]['date']
        tweet_date = datetime.strptime(tweet_date, '%Y-%m-%d %H:%M:%S')
        if tweet_date >= cutoff_dt:
            within_24_inds.append(i)
    last_hour_tweet_df = tweet_df.iloc[within_24_inds]
    
    return last_hour_tweet_df


def get_engagement_scores(tweet_df):
    """
    This function gets the engagement scores (retweets*replies*likes) for an input df of tweets
    and then order by engagement score
    """
    engagement_score_list = []
    for i in range(len(tweet_df)):
        retweets = tweet_df.iloc[i]['nretweets']
        replies = tweet_df.iloc[i]['nreplies']
        likes = tweet_df.iloc[i]['nlikes']
        engagement_score = retweets*replies*likes
        engagement_score_list.append(engagement_score)

    tweet_df['engagement_score'] = engagement_score_list
    
    # Order in descending
    tweet_df = tweet_df.sort_values(by='engagement_score', ascending=False)
    
    return tweet_df


def get_twitter_handle_bio_details(twitter_handle):
    try:
        c = twint.Config()
        c.Username = twitter_handle
        c.Store_object = True
        c.User_full = False
        c.Pandas =True
        c.Hide_output = True

        twint.run.Lookup(c)
        user_df = twint.storage.panda.User_df.drop_duplicates(subset=['id'])

        try:
            user_id = list(user_df['id'])[0]
        except:
            user_id = 'NA'

        try:
            user_name = list(user_df['name'])[0]
        except:
            user_name = 'NA'

        try:
            user_bio = list(user_df['bio'])[0]
        except:
            user_bio = 'NA'

        try:
            user_profile_image_url = list(user_df['avatar'])[0]
        except:
            user_profile_image_url = 'NA'

        try:
            user_url = list(user_df['url'])[0]
        except:
            user_url = 'NA'

        try:
            user_join_date = list(user_df['join_date'])[0]
        except:
            user_join_date = 'NA'

        try:
            user_location = list(user_df['location'])[0]
        except:
            user_location = 'NA'

        try:
            user_following = list(user_df['following'])[0]
        except:
            user_following = 'NA'

        try:
            user_followers = list(user_df['followers'])[0]
        except:
            user_followers = 'NA'

        try:
            user_verified = list(user_df['verified'])[0]
        except:
            user_verified = 'NA'

    except Exception as e:
        print(e)
        user_name = 'NA'
        user_bio = 'NA'
        user_profile_image_url = 'NA'
        user_url = 'NA'
        user_join_date = 'NA'
        user_location = 'NA'
        user_following = 'NA'
        user_followers = 'NA'
        user_verified = 'NA'
    
    return user_name, user_bio, user_profile_image_url, user_url, user_location, user_following, user_followers, user_verified


def get_tweet_id_and_handle_from_url(tweet_url):
    """
    This function takes a tweet_url and then returns the tweet ID and tweet handle
    """
    split_list = tweet_url.split('/')
    twitter_handle = split_list[3]
    tweet_id = split_list[5]
    
    return tweet_id, twitter_handle

def get_digest_tweet_handles_and_ids_from_url(article_digest_tweet_urls):
    """
    This function takes in a set of digest tweet urls and then processes them to get the tweet IDs
    and tweet urls
    """
    twitter_handle_list = []
    tweet_id_list = []

    for i in range(len(article_digest_tweet_urls)):
        # Build an algo that takes in a tweet url and then gets the tweet_id and handle name
        tweet_url = article_digest_tweet_urls[i]

        tweet_id, twitter_handle = get_tweet_id_and_handle_from_url(tweet_url)
        twitter_handle_list.append(twitter_handle)
        tweet_id_list.append(tweet_id)
        
    return twitter_handle_list, tweet_id_list


def cleanup_tweet(tweet, twitter_handle, num_reply=0):
    """
    This function takes in a tweet and then cleans it up by removing non alphanumericals etc
    """
    tweet_tokens = tweet.split()[num_reply:] # we ignore the first token which will always be the handle
    text_list = []
    for token in tweet_tokens:
        temp = ''.join([i for i in token if (i.isalpha() or (i in ['.',',', '..', '…', ':', ';', '?', '"', '-']) or i.isdigit())])        
        if '#' not in temp:
            if twitter_handle not in temp:
                text_list.append(temp.strip())

    tweet_text = ' '.join(text_list)
    tweet_text = re.sub(r"http\S+", "", tweet_text)
    tweet_text = tweet_text.strip()

    return tweet_text

"""
Processing article tweets
"""
def get_twitter_handle_mentions(twitter_handle, search_date_str):
    """
    This function takes a twitter handle and gets up to 10k mentions within a certain timeframe
    """
    num_tweets = 10000

    # 2 - Get the article tweet details
    min_replies = 0
    verified = False
    search_term = '@%s' % twitter_handle
    mentions_df = get_tweets_from_search_term(search_term, min_replies, verified, num_tweets, search_date_str)
    
    return mentions_df

"""
Getting mentions of an article on twitter
"""


def get_twitter_mentions_for_rss_article(article_title, extraction_time):
    """
    This function takes an article title, then strips it to the noun chunks and searches twitter for how many
    tweets seem to be covering it 
    """
    cut_off_h_diff = 48
    search_h_diff = 48
    num_tweets = 5000
    min_replies = 0
    verified = False

    search_term = search.get_search_term_from_noun_chunks(article_title)

    if len(search_term) > 0:
        datetime_object = datetime.strptime(extraction_time, '%Y-%m-%d %H:%M:%S')

        search_date_str = str(datetime_object - timedelta(hours=24))
        
        replies_df = get_tweets_from_search_term(search_term, min_replies, verified, num_tweets, search_date_str)

        num_mentions = len(replies_df)
    else:
        num_mentions = 0
    
    return num_mentions


def get_num_twitter_hits_for_search_term(search_term, days):
    """
    This function takes in a search term and then gets the number of hits on twitter (max of 100)
    The idea is for this to just be a quick check of whether this entity is relevant enough to search for images
    """
    ## Build functionality to get how many mentions on twitter for an entity in the last 6 months
    search_date = datetime.today() - timedelta(days=days)

    # Create the search date string
    search_dt = str(search_date.date())
    search_hr = search_date.hour
    search_date_str = '%s %s:00:00' % (search_dt, search_hr)

    min_replies = 0
    verified = False
    num_tweets = 10000 # we want to do a max of 100 just to check if the entity is relatively popular to meet our minimum threshold of whether we look for 
    replies_df = get_tweets_from_search_term(search_term, min_replies, verified, num_tweets, search_date_str)
    num_twitter_hits = min(num_tweets,len(replies_df))
    
    return num_twitter_hits


"""
New Functions
"""
from IPython.utils import io
import pandas as pd
from datetime import datetime, timedelta


def get_last_7_days_tweets_for_handle(twitter_handle):
    ## Get all the tweets from them in the last 24 hours 
    search_dt = datetime.now() - timedelta(days=3) # so we capture the content from yday as well
    search_date = datetime.strftime(search_dt, '%Y-%m-%d')
    num_tweets = 50000 
    tweet_df = get_latest_tweets_from_handle(twitter_handle, num_tweets, search_date)

    return tweet_df


def get_last_hour_tweets_for_handle(twitter_handle):
    """
    This function takes in a twitter handle and gets all the tweets generated in the last hour
    * Later build a function that also does this for a search term as well
    """
    ## Get all the tweets from them in the last hour
    cutoff_dt = datetime.now() - timedelta(hours=1)
    search_dt = datetime.now() - timedelta(hours=2) # so we capture the content from 2 hours ago as well
    search_date = datetime.strftime(search_dt, '%Y-%m-%d')
    num_tweets = 5000 
    tweet_df = get_latest_tweets_from_handle(twitter_handle, num_tweets, search_date)

    # Get tweets in the last hour
    within_24_inds = []
    for i in range(len(tweet_df)):
        tweet_date = tweet_df.iloc[i]['date']
        tweet_date = datetime.strptime(tweet_date, '%Y-%m-%d %H:%M:%S')
        if tweet_date >= cutoff_dt:
            within_24_inds.append(i)
    last_hour_tweet_df = tweet_df.iloc[within_24_inds]
    
    return last_hour_tweet_df


def get_twitter_handles_of_similar_headline_tweets(article_title, twitter_handle):
    """
    This function takes an article headline and then scours through twitter to get the handles
    of tweets that have similar text to the headline
    """
    # Create the search date string
    search_date = datetime.today() - timedelta(days=1)

    search_dt = str(search_date.date())
    search_hr = search_date.hour
    search_date_str = '%s %s:00:00' % (search_dt, search_hr)

    num_tweets = 5000
    min_replies = 0
    verified = True

    search_term = search.get_search_term_from_noun_chunks(article_title)

    if len(search_term) > 0:
        similar_df = get_tweets_from_search_term(search_term, min_replies, verified, num_tweets, search_date_str)
    else:
        similar_df = {}

    ## Create a dictionary of the similar handles and the metadata around it
    similar_handles_dict = {}
    total_score = 0
    significant_score_count = 0
    num_similar = 0
    
    skip_tweet_ids = []
    for i in range(len(similar_df)):
        tweet_id = similar_df.iloc[i]['id']
        tweet = similar_df.iloc[i]['tweet']
        username = similar_df.iloc[i]['username']
        
        if username != twitter_handle:
            date = similar_df.iloc[i]['date']
            nlikes = similar_df.iloc[i]['nlikes']
            nreplies = similar_df.iloc[i]['nreplies']
            nretweets = similar_df.iloc[i]['nretweets']
            score = round(nlikes*nreplies*nretweets/1000, 3)
            skip_tweet_ids.append(tweet_id)
            num_similar += 1

            if score >= 1:
                significant_score_count += 1
            total_score += score
            temp_dict = {
                'tweet' : tweet,
                'tweet_id' : tweet_id,
                'username' : username,
                'date' : date,
                'score' : score,
            }
            similar_handles_dict.update({username:temp_dict})
        
    similar_handles_dict['total_score'] = total_score
    similar_handles_dict['num_similar'] = num_similar
    similar_handles_dict['num_significant'] = significant_score_count
    similar_handles_dict['skip_tweet_ids'] = skip_tweet_ids
    
    return similar_handles_dict


def get_relevance_for_latest_articles(last_hour_news_df):
    skip_id_list = [] # These are the twitter IDs for tweets that have already been identified as similar so we don't bother engaging with them
    similar_handles_dict_list = []
    related_handles_list = []
    num_significant_list = []
    total_score_list = []

    for i in range(len(last_hour_news_df)):
        tweet_id = last_hour_news_df['id'].iloc[i]
        tweet = last_hour_news_df['tweet'].iloc[i]
        twitter_handle = last_hour_news_df['username'].iloc[i]
        article_title = cleanup_tweet(tweet, twitter_handle, num_reply=0)
        if i%50 == 0:
            print(i)
            print(article_title)
            print(twitter_handle)
            print()
        if tweet_id not in skip_id_list:
            with io.capture_output() as captured:
                similar_handles_dict = get_twitter_handles_of_similar_headline_tweets(article_title, twitter_handle)
                related_handles = list(similar_handles_dict.keys())
                related_handles = related_handles[:-4]
                total_score = similar_handles_dict['total_score']
                num_similar =  similar_handles_dict['num_similar']
                num_significant = similar_handles_dict['num_significant']
                skip_tweet_ids = similar_handles_dict['skip_tweet_ids']
                skip_id_list += skip_tweet_ids
                
                if num_similar < 30: # The odds of having more than 30 are crazy low, so we assume its a glitch if this happens
                    similar_handles_dict_list.append(similar_handles_dict)
                    related_handles_list.append(related_handles)
                    num_significant_list.append(num_significant)
                    total_score_list.append(total_score)
                else:
                    similar_handles_dict_list.append({})
                    related_handles_list.append([])
                    num_significant_list.append(0)
                    total_score_list.append(0)
        else:
            similar_handles_dict_list.append({})
            related_handles_list.append([])
            num_significant_list.append(0)
            total_score_list.append(0)

    # Save the new variables to the DF
    last_hour_news_df['similar_handles_dict'] = similar_handles_dict_list
    last_hour_news_df['related_handles'] = related_handles_list
    last_hour_news_df['num_significant_handles'] = num_significant_list
    last_hour_news_df['total_score'] = total_score_list
    
    return last_hour_news_df


def get_engagement_metrics_for_twitter_handle(twitter_handle):
    """
    This takes any twitter handle and then calculates the following engagement metrics
    - avg daily posts
    - perc of significant posts (>5 likes and replies)
    - avg sig likes
    - avg sig replies
    """
    # Get tweets in the last week
    latest_tweet_df = get_last_7_days_tweets_for_handle(twitter_handle)

    # Get the unique_dates for the dataset
    date_list = []
    for i in range(len(latest_tweet_df)):
        date_string = latest_tweet_df.iloc[i]['date'][0:10]
        date_list.append(date_string)
    latest_tweet_df['date_string'] = date_list

    unique_dates = list(set(list(latest_tweet_df['date_string'])))
    unique_dates = unique_dates[1:-1]
    unique_dates = sorted(unique_dates)

    day_articles_list = []
    for date in unique_dates:
        date_df = latest_tweet_df[latest_tweet_df['date_string'] == date]
        day_articles_list.append(len(date_df))
        
    try:
        avg_daily_post = int(np.average(day_articles_list))

        ## Now filter out all the posts with less than 5 likes and comments, and get a percentage
        ## Then calculate the avg likes and comments for the posts that pass this threshold
        sig_content_counter = 0
        replies_list = []
        likes_list = []
        for i in range(len(latest_tweet_df)):
            nlikes = latest_tweet_df.iloc[i]['nlikes']
            nreplies = latest_tweet_df.iloc[i]['nreplies']

            if (nlikes > 5) and (nreplies > 5):
                sig_content_counter += 1
                replies_list.append(nreplies)
                likes_list.append(nlikes)


        perc_sig = int((sig_content_counter/len(latest_tweet_df)) * 100)
        try:
            avg_sig_likes = int(np.average(likes_list))
        except:
            avg_sig_likes = 0
        try:
            avg_sig_replies = int(np.average(replies_list))
        except:
            avg_sig_replies = 0
    except:
        avg_daily_post = perc_sig = avg_sig_likes = avg_sig_replies = 0

    return avg_daily_post, perc_sig, avg_sig_likes, avg_sig_replies

def process_tweet_url_list(url_list):
    """
    This function processes all the urls extracted from a twitter handle and generates a frequency dict
    of their domains
    """
    domain_list = []
    cleaned_url_list = []
    num_shortened = 0
    num_processed = 0

    for url in url_list:
        # Check if we have processed enough URLs
        if num_processed > 19:
            break
        if num_shortened >  9:
            break

        # Check if the url is shortened or normal
        if len(url) > 30:
            pass
        else:
            url = web_ext.process_shortened_content_url(url)
            num_shortened += 1

        # Get the domain
        domain = web_ext.get_domain_url_from_article_url(url)
        cleaned_url_list.append(url)
        domain = domain[4:]
        num_processed += 1

        # Deal with the case where they were sharing a twitter link
        if domain != 'twitter.com': # this excludes the cases where they are sharing twitter urls
            domain_list.append(domain)

    # Get a frequency dict of all the domains found
    domain_freq_dict = Counter(domain_list)
    norm_domain_freq_dict = gen.normalise_dict_values(domain_freq_dict)

    return cleaned_url_list, norm_domain_freq_dict