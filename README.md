# wsb-scrapper
Reddit comments scrapper

Need to install python3 (If you have mac I would recommend using homebrew - there are guides online)

Need to install the following python libraries (You can use pip to do so, might have to use pip3)
 - pandas
 - praw
 - regex (re)
 - os (might already be installed)
 - datetime (might already be installed)
 - python-dotenv (dotenv)

You then need to create a ".env" file which will store your reddit credentials
The .env file will just have 3 lines with the following format
This link tells you how to get those keys using your reddit account https://www.storybench.org/how-to-scrape-reddit-with-python/

CLIENT_ID="client_id"

CLIENT_SECRET="client_secret"

USER_AGENT="user_agent"

To run the script you just need to run "python3 scrapper.py" or "python scrapper.py" depending on your python alias

Make sure you grab the post id from the thread whose comments you want to scrape (I explain what this is in scrapper.py)

The program will save a csv file in the format yyyy-mm-dd.csv with the results
If you want to scrape comments from multiple posts in one day (e.g. daily discussion and moves tomorrow)
it will save the combined results so you can scrape as many posts as you would like.

Feel free to fork it if you want to make your own changes.
