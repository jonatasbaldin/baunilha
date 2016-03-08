# -*- coding: UTF-8 -*-

import twitter


class BaunilhaTwitter(object):
    """
    To instanciate a twitter connection.
    """

    def __init__(self):
        """
        Let's init it!
        """

    def Connect(self, consumer_key, consumer_secret, access_token_key,
                access_token_secret):
        """
        Authenticate to Twitter's API.
        All parameters are from Twitter's Dev Application and in the
        application is configured in instace/config.py
        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret
        self.auth = False

        # tries to connect
        try:
            self.conn = twitter.Api(consumer_key=self.consumer_key,
                                    consumer_secret=self.consumer_secret,
                                    access_token_key=self.access_token_key,
                                    access_token_secret=self.access_token_secret)
        except:
            error = True
            message = u'Parece que o Baunilha está fora! Tente novamente em alguns instantes!'

        else:
            self.auth = True
            error = False
            message = ''

        ret = {'error': error, 'message': message}
        return ret

    def GetTweets(self, user):
        """
        Returns a list of Tweets and its IDs from a determined user.
        Parameters:
        user: Twitter's username
        """
        self.user = user

        if self.auth:
            try:
                # get last 50 tweets from usre
                timeline = self.conn.GetUserTimeline(screen_name=user,
                                                     count=50)

                # get username
                username = self.conn.GetUser(screen_name=user)

                # get username profile image
                # removes '_normal', which brings a bigger/better image
                user_img = str(username._profile_image_url).replace('_normal', '')

                tweets = set()

                # generate a set with tweet ID and tweet text
                for i in timeline:
                    # tweets[0] = text
                    # tweets[1] = id
                    tweets.add((i.id, i.text))

            except:
                error = True
                message = u'Desculpe, mas este usuário não existe :( Tente outro!'
                ret = {'error': error, 'message': message}
                return ret

            ret = {
                'error': False,
                'tweets': tweets,
                'user_img': user_img,
                'user': user
            }

            return ret

    def GetSingleTweet(self, user, id):
        """
        Returns a single tweet determined by its ID.
        Parameters:
        user: Twitter's username
        id: Tweet's ID
        """
        self.user = user
        self.id = id

        if self.auth:
            try:
                # get username
                username = self.conn.GetUser(screen_name=user)

                # get username profile image
                # removes '_normal', which brings a bigger/better image
                user_img = str(username._profile_image_url).replace('_normal', '')

                #  populate single_tweet
                single_tweet = self.conn.GetStatus(id=id).text

            except:
                error = True
                message = u'Desculpe, mas este usuário não existe :( Tente outro!'
                ret = {'error': error, 'message': message}
                return ret

            ret = {
                'error': False,
                'single_tweet_id': self.id,
                'single_tweet': single_tweet,
                'user_img': user_img,
                'user': user
            }

            return ret
