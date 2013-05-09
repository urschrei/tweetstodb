#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Process app stream events filtered by users it follows """

# first, install requirements using pip install -r requirements.txt
# run Alembic upgrade HEAD to create the DB and run migrations
# run in a terminal: python getstream.py

import sys
import tweepy
import traceback
import datetime
from models import sync, Tweets
from keys import con_key, con_secret, acc_key, acc_secret
from sqlalchemy.exc import IntegrityError, DataError


class StreamWatcherListener(tweepy.StreamListener):
    """ Watch the stream of an app, and respond to stream events """
    def __init__(self, adder, followers):
        super(StreamWatcherListener, self).__init__()
        self.adder = adder
        self.followers = followers
        print "Number of followers: %s" % len(self.followers)

    def on_status(self, status):
        if status.author.id not in self.followers:
             # don't add the status
             # we need this because Twitter's / Tweepy's filtering is dicky
            return
        try:
            self.adder.send(status)
        except UnicodeDecodeError:
            # Catch any unicode errors
            # and just ignore them, to avoid breaking the application.
            pass

    def on_error(self, status_code):
        """ Echo any errors """
        print 'An error has occured! Status code = %s' % status_code
        # sys.stdout.flush()
        if status_code == 420:
            print 'Exiting due to auth error - we have to respect a 420 error'
            raise
        # keep stream alive
        return True

    def on_timeout(self):
        """ Echo a timeout """
        print 'Snoozing Zzzzzz'
        # sys.stdout.flush()


def add_to_db():
    """ coroutine which adds tweets to our DB """
    session = sync()
    try:
        while True:
            tweet = (yield)
            to_add = Tweets(
                content=tweet.text.encode("utf-8"),
                username=tweet.author.screen_name.encode('utf-8'),
                coordinates=tweet.coordinates,
                tweet_id=str(tweet.id).encode('utf-8')
            )
            session.add(to_add)
            try:
                session.commit()
            except (IntegrityError, DataError):
                # discards the tweet in case of error, prob. a bit too brutal
                session.rollback()
                session.expunge_all()
    except GeneratorExit:
        session.flush()


def main():
    """ Main function """
    to_follow = "brockleycentral"

    def authorise(*args):
        """ Tweepy OAuth dance
        Accepts: consumer key, secret; access key, secret
        """
        auth = tweepy.OAuthHandler(
            args[0],
            args[1])
        auth.set_access_token(
            args[2],
            args[3])
        return auth

    twitter = authorise(con_key, con_secret, acc_key, acc_secret)

    twet = tweepy.API(twitter)
    follower_set = set(tweepy.Cursor(
        twet.followers_ids, screen_name=to_follow).items())
    follower_list = list(follower_set)[:5000]
    print len(follower_list)

    # initialise our DB writer coroutine
    adder = add_to_db()
    adder.next()
    print("We've retrieved all followers for %s" % (to_follow))
    swl = StreamWatcherListener(adder, follower_set)
    stream = tweepy.streaming.Stream(
        twitter,
        swl,
        timeout=None,
        secure=True)

    stream.filter(follow=[str(follower) for follower in follower_list])
    print 'Now monitoring filtered stream - %s' % datetime.datetime.now()
    # sys.stdout.flush()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        # actually raise these so it exits cleanly
        raise
    except Exception, error:
        # all other exceptions, so display the error
        print "Stack trace:\n", traceback.print_exc(file=sys.stdout)
        # sys.stdout.flush()
    else:
        pass
    finally:
        # exit cleanly once we've done everything else
        print 'Exiting.'
        # sys.stdout.flush()
        sys.exit(0)
