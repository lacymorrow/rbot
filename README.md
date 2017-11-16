# rbot
Social Bot for generating ineractions


## Setup

A few packages are required:

```bash
brew install python

sudo easy_install pip

sudo pip install gensim --ignore-installed six

pip install nltk praw
```

#### Configuration

Create a `config.py` in the repo with the following variables:

```python
user_agent = 'MY_USER_AGENT 1.0'
username = 'REDDIT_USERNAME'
password = 'REDDIT_PASSWORD'
client_id = 'XXXXXXXXXXXXXX'
client_secret = 'XXXXXXXXXXXXXXXXXXXXX'
```

Run with: `python post_bot.py` or `python comment_bot.py`