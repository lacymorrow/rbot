######

# Todo:

# Language processing
# Don't self repost on same sub
# Post Image
# Video/gif(v)


import os
import nltk
import praw
import time
import gensim
import random
import datetime
import requests
nltk.download('punkt')

# import configuration files
import config
import subs


##



## 1) REPOST OLD, POPULAR POSTS FROM SUBS EVERY <delay>
## 2) REPOST RELEVANT POPULAR COMMENT TO A REPOSTED QUESTION

# Check new posts in popular subs for something similar to a popular repost. Find a high comment from the original, paraphrase, and repost

# Find a hot post not on all and xrosspost to similar sub 
########### (first sub on sidebar?)

# check hottest posts of all-time, repost as new
########### Paraphrase
########### Change ownership

# random subreddits

# rply to comments



# If True, will CREATE LIVE REDDIT POSTS
SEND_FLAG = True

# Config
SORT_DATE = 'month' # 'week', 'month', etc. via reddit
POST_DELAY = 10 # seconds ; 600 === 10 mins
SEARCH_LIMIT = 50 # Posts within subs that  are searched Max 1000
AGE_THRESHOLD = 30 # Default 365 days (considered a month)
EXECUTION_TOTAL = 500 # TOTAL APPLICATION RUN COUNT
BANNED_WORDS = ['[OC]', 'hello']

# ACTIVE_SUBS = ['test']
ACTIVE_SUBS = subs.most_subscribed_subs # ['test', 'me_irl', 'lgbqt',] # 'askreddit', 'askwomen', 'askmen'] 

# 'Futurology' = 5 day old 
# 'technology' = 5 daays old
# 'youtubehaiku' = 5 daays old
BANNED_SUBS = ['gifs', 'bodyweightfitness', 'overwatch', 'hearthstone', 'tattoos', 'pokemon', 'futurology', 'technology', 'youtubehaiku']

preface = "I know it's been posted before but... "


# Skip banned subs
working_subs = [x for x in ACTIVE_SUBS if x not in BANNED_SUBS]


# Other Subs to consider to widen the net
## print "subscribed to " str(subscribed)
## print "most subscribers" + str(subs.most_subscribed_subs)
## print "most activity" + str(subs.most_active_subs)


# Monitors incoming submissions
# Get the newest submissions from a subreddit ('all')
# for submission in r.subreddit('askreddit').stream.submissions():
#     print(submission)


def bot_login():
    print "Logging in..."
    r = praw.Reddit(username = config.username,
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = config.user_agent)

    return r

def run_bot(r):
    
    # random.choice(ACTIVE_SUBS) # number is how far from top post to use (0 is default/top)
    ## Todo, active sub may be repeated/ not removed
    active_sub = random.choice(ACTIVE_SUBS) 
        
    # print 'Queue: ' + str(ACTIVE_SUBS)
    print 'TARGETING RANDOM SUB: ' + active_sub



    # get top OLD posts from working subs (default ALL TIME) (POSTS that stood test of time)
    posts = [] # posts old enough to consider for reposting
    top_posts = r.subreddit(active_sub).top(SORT_DATE, limit=SEARCH_LIMIT)
    for post in top_posts:
        if post.shortlink: 

            # get post age delta
            post.age = datetime.date.today() - datetime.date.fromtimestamp(post.created)
            # print max(post.age.days, key=lambda item: item[1])
            # check if post is old enough to warrant a repost (don't repost brand new posts, better for xposts)
            
            if(int(post.age.days) > AGE_THRESHOLD):
                post = restyle_post(post)
                posts.append(post)
    # if posts are old enough, create repost
    # optionally, randomize;
    create_posts(r, posts[:-1])

# POST

def create_posts(r, posts):
    for post in posts:
        # Truncate post title in console
        pretty_post_title = pretty_text(post.title)

        try:    

            # check if link or text post
            if post.selftext:
                # text post
                print "\n\n********Text Post:\n" + post.subreddit.display_name + "\nPost Title: \n" + post.title

                if(SEND_FLAG):
                    submission = r.subreddit(post.subreddit.display_name).submit(preface + post.title, post.selftext)
                    print "URL: " + submission.url
                    sleep(POST_DELAY)

                else:
                    debug('No data will be sent.')
            
            elif post.url: 
                # link post
                print "\n\n********Link Post: \n" + post.subreddit.display_name + "\nPost Title: " + pretty_post_title + "\nURL: " + post.url
                if(SEND_FLAG):
                    submission = r.subreddit(post.subreddit.display_name).submit(preface + post.title, url=post.url ) 
                    print "URL: " + submission.url
                    sleep(POST_DELAY)

                else:
                    debug('No data will be sent.')

            else:
                debug("NNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA!!!! \nyou broke me...")

            print "******\nReposting: " + pretty_post_title + "\nAge: " + str(post.age.days) + " days \nSubreddit: " + post.subreddit.display_name
            
            # credits
            print "#####" + str(post.author)


        except praw.exceptions.APIException as e:
            s = str(e)
            print "APIException PRAW: " + s
            next_post_delay = int(filter(str.isdigit, s))
            if not str(next_post_delay.isdigit()):
                exit(1)
            sleep(next_post_delay)
            continue;

        except AttributeError as e:
            print "AttributeError: " + str(e)
            exit(1)

        except AssertionError as e:
            print "AssertionError: " + str(e)
            exit(1)
        except:
            print "Uncaught Error"
            exit(1)



def restyle_post(post):
    for word in BANNED_WORDS:
        post.title = post.title.replace(word, '')

    return post

def pretty_text(text):
    return (text[:75] + '...') if len(text) > 75 else text

def sleep(mins):
    if mins > 11:
        mins = 2 #prevent seconds parsed as minutes
    if mins == 1:
        mins = 2
    print "Sleep " + str(mins) + " minutes..."
    time.sleep(mins * 60)

def debug(msg):
    print "DEBUGGING....\n" + msg
    print "NOT SENDING LIVE DATA"


execution_count = 0
r = bot_login()
while execution_count < EXECUTION_TOTAL:

    print "### Iteration ",  str(execution_count) + "  ###\n"
    run_bot(r)
    
    execution_count += 1


# get subscribed subreddits
# subscribed = list(r.user.subreddits(limit=None)) 