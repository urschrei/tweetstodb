[![Tweets by day](example.png "Tweets per Day")](http://nbviewer.ipython.org/urls/raw.github.com/urschrei/tweetstodb/master/visualise_tweets_csv.ipynb "IPython Notebook viewer")

## Setup
*Not intended for production use*

- Install requirements using `pip install -r requirements.txt`
- Ensure a Postgres DB called `tweetstream` exists:
    - `u`: streamer
    - `p`: streamer
- Run DB migrations using `alembic upgrade head` to create the database table and indices
- Get Twitter API credentials: https://dev.twitter.com/apps/new
- Ensure you have a `keys.py` file containing the following string variables:
    - `con_key`: the API consumer key
    - `con_secret`: the API consumer secret
    - `acc_key`: the API access key
    - `acc_secret`: the API access secret
- In `main()`, change the `to_follow` variable to the Twitter user whose followers' Tweets you wish to retrieve
- Run `python getstream.py` from the command line

## How It Works
- The Tweepy library is used to connect to Twitter using OAuth
- The Twitter [firehose](https://dev.twitter.com/streaming/firehose) is then [filtered](https://github.com/urschrei/tweetstodb/blob/master/getstream.py#L98-114) to show only the tweets from accounts following a given account – in this case [@brockleycentral](https://twitter.com/brockleycentral).
- The tweets are streamed into a PostgreSQL database using the SQLAlchemy library and a [coroutine](https://github.com/urschrei/tweetstodb/blob/master/getstream.py#L56-76). This allows offline retrieval and analysis using e.g. the Pandas data analysis library (see below).

## Analysis
If you wish to visualise the data, an [IPython notebook](http://nbviewer.ipython.org/urls/github.com/urschrei/tweetstodb/raw/master/visualise_tweets.ipynb) is provided.

For offline analysis (using dumped CSV data), run [this IPython notebook](http://nbviewer.ipython.org/urls/github.com/urschrei/tweetstodb/raw/master/visualise_tweets_csv.ipynb).

A subset of tweets is available as a zipped database dump: `tweets.db.zip`. If you wish to use this for analysis, ensure your db exists with the correct credentials, but **do not run the alembic upgrade command**, as the structure will be created by the import – unzip the file, and import into Postgres.

### License
Copyright Stephan Hügel, 2014  
License: [MIT](license.txt)
