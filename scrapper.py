import pandas as pd
import praw
from praw.models import MoreComments
import re
import os
from os import path
import datetime
from dotenv import load_dotenv
load_dotenv()

# uses datetime to create file name for today's csv file (if it exists)
today_csv = "{0}.csv".format(datetime.datetime.today().strftime('%Y-%m-%d'))
# check if we already saved stock symbols from an earlier post today
if path.exists(today_csv):
  # reads csv and creates a map (symbol (key) : count (value))
  symbols_df = pd.read_csv(today_csv)
  symbols = dict(zip(symbols_df.Symbol, symbols_df.Count))
else:
  # reads csv and creates a map (symbol (key) : count (value)) where count is set to 0
  symbols_df = pd.read_csv('symbols.csv', usecols=['Symbol'])
  symbols_df['Count'] = 0
  symbols = dict(zip(symbols_df.Symbol, symbols_df.Count))

# reddit api credentials (I don't want my account to get banned if some rando steals my secret key since the repo's public)
# instructions on how to create one is here
reddit = praw.Reddit(
  client_id=os.getenv('CLIENT_ID'),
  client_secret=os.getenv('CLIENT_SECRET'),
  user_agent=os.getenv('USER_AGENT')
)

# retrieve post from id (e.g. reddit.com/r/wallstreetbets/comments/l68y04/daily_discussion_thread)
# l68y04 is the post id from the example above you have to change this yourself for each post
postId = 'l6ea1b'
submission = reddit.submission(id=postId)

count = 0
# iterate through comments - increase the limit if you want it to look through more comments
# I found that 100 is a good balance between quantity and time it takes to run
# If the comment thread is too big you might get a 413 error so lower the limit to 0 if that happens
submission.comments.replace_more(limit=100)
for comment in submission.comments.list():
  count += 1
  # only count stock symbols once for each comment by creating a new set for each comment
  mentioned_stocks = set()
  # removes any non alpha numerical characters and makes the string all uppercase to match stock symbols
  comment = re.sub(r"[^a-zA-Z0-9 ]+", "", comment.body).upper()
  # creates an array of the words from the comment
  words = comment.split(' ')
  for word in words:
    # adds to count if word is a stock symbol and has not been counted for the comment already
    if word in symbols and word not in mentioned_stocks:
      symbols[word] = symbols[word] + 1
      mentioned_stocks.add(word)

# save new counts to today's csv file
pd.DataFrame(list(symbols.items()), columns=['Symbol', 'Count']).to_csv(today_csv, index=False)

# sort symbols based on count before printing
sorted_symbols = dict(sorted(symbols.items(), key=lambda item: item[1]))
print(sorted_symbols)
print(count)
