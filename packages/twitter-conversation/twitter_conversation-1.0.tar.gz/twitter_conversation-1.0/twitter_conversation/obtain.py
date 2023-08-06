import csv
import datetime
import os
import time
from pathlib import Path
from typing import List, Optional

import numpy as np
import pandas as pd
import tweepy
from tqdm import tqdm
from tweepy import ReferencedTweet


class Moisturizer:
    """
    This class is for hydrating tweets.
    """

    def __init__(self, client: tweepy.Client, df_tweets: pd.DataFrame):
        """
        This class hydrates tweets with their text if it is available.
        Hence, it is necessary to provide the following.
        :param client: The client for to connect to Twitter API.
        :param df_tweets: A dataframe where the index are tweet ids.
        """
        self.df_tweets = df_tweets
        self.client = client
        self.tweets = {}

    def _add_tweet(self, tweet_id: int, text: str) -> Optional[dict]:
        """
        This method is used to add a tweet to all tweets of the particular reply-tree.

        :param tweet_id: The id of the tweet.
        :param text: The text of the tweet.
        :return: The tweet as a dict or None if the tweet was already obtained.
        """
        if tweet_id not in self.tweets.keys():
            self.tweets[tweet_id] = {'tweet_id': tweet_id, 'text': text}
            return self.tweets[tweet_id]
        return None

    def hydrate(self) -> None:
        """
        This method hydrates the handed over dataframe df_tweets by calling the Twitter API.
        By calling this method each tweet is hydrated with its text if available.
        Notice that this method splits the provided dataframe into chunks of size 100.

        :return: Nothing
        """
        batch_size = 100
        tweets_to_look_up = self.df_tweets.index.to_numpy()
        batch_wise_tweets_to_look_up = np.split(tweets_to_look_up,
                                                np.arange(batch_size, len(tweets_to_look_up), batch_size))
        for batch_of_tweets_to_look_up in tqdm(batch_wise_tweets_to_look_up):
            twitter_ids_to_look_up = ','.join(map(lambda twitter_id: str(twitter_id), batch_of_tweets_to_look_up))

            response = self.client.get_tweets(ids=twitter_ids_to_look_up)
            if response.data:
                for tweet in response.data:
                    self._add_tweet(tweet.id, tweet.text)

    def write_to_csv(self, path: Path = './hydrated_tweets.csv') -> None:
        """
        This method writes the hydrated tweets of the calling Moisturizer to a designated csv-file.

        It is important to first run .hydrate() since the methods depends on the tweets being looked-up.
        Furthermore, each row will be appended to the specified csv-file.
        If this file is already existing, then the header-line will not be written again.

        :param path: Path to where the file should be written.
        :return: Nothing
        """
        fieldnames: list[str] = ['tweet_id', 'text']
        file_exists = os.path.exists(path)
        with open(path, 'a', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerows(self.tweets.values())


class ReplyTree:
    """
    This class is to write structural Reply-Trees, as they are specified by nodes having only the id of the associated
    Tweet and the corresponding conversation_id as well as the reply-Relation as edges, to a running Neo4j instance.
    """

    def __init__(self, client: tweepy.Client, conversation_id: int, **kwargs) -> object:
        """
        This method initializes the ReplyTree class.
        It is important to provide the initialized client of tweepy for calling the Twitter-API v2.
        Furthermore, the conversation_id is to be given to this class for reconstructing the associated Reply-Tree.
        To specify the search option of tweepy.search_all_tweets, which is used for obtaining Reply-Trees, kwargs can
        be used.
        :param client: The initialized tweepy client to call Twitter-API v2.
        :param conversation_id: The conversation who's Reply-Tree should be reconstructed.
        :param kwargs: Additional search options for client.search_all_tweets.
        """
        self.client = client
        self.conversation_id = conversation_id
        self.kwargs = kwargs
        self.tweets = {}

    def _add_tweet(self, tweet_id: int, conversation_id: int, parent_id: Optional[int]) -> Optional[dict]:
        """
        This method is used to add a tweet to all tweets of the particular reply-tree.

        :param tweet_id: The id of the tweet.
        :param conversation_id: The conversation where this tweet belongs to.
        :param parent_id: The id of the tweets the tweet at hand is replying to (if it is replying to any tweet).
        :return: The tweet as a dict or None if the tweet was already obtained.
        """
        if tweet_id not in self.tweets.keys():
            self.tweets[tweet_id] = {'tweet_id': tweet_id, 'conversation_id': conversation_id, 'parent_id': parent_id}
            return self.tweets[tweet_id]
        return None

    def obtain(self, only_root: bool = False) -> None:
        """
        This method must be used to obtain the Reply-Trees by the used conversation_id and all additional attributes.

        By calling this method the Reply-Tree fills and stores the tweets in self.tweets.

        The conversation can be obtained since Twitter associates a Reply-Tree to each particular conversation_id and
        writes the structural Reply-Tree to a specified csv-file.

        Therefore, if the conversation-starting Tweet is known the conversation can be reconstructed.

        Furthermore, it should be noticed that this method only obtains Reply-Trees.
        This is a simplification for conversations since Retweets would always refer to the original Tweet where
        all Replys to the Retweet would also be added to the conversation of the original Tweet.
        Quotes (Retweet + text), on the other side, would create a different context if a Tweet of the conversation is
        cited to be forwarded. This would create a new side-conversation with another conversation_id. Otherwise, if a
        Tweet of the same conversation is quoted as a Reply the conversation_id stays the same. The same holds if the
        Reply quotes a Tweet of another conversation. In this case the quoted Tweet is added as a URL to the quoting
        Reply.

        :return: Nothing.
        """
        t0_global: float = time.time()
        print("Obtain Reply-Tree for: ", self.conversation_id)

        root_tweet: dict = self._add_tweet(tweet_id=self.conversation_id,
                                           conversation_id=self.conversation_id,
                                           parent_id=self.conversation_id)
        if not only_root:
            for page in tweepy.Paginator(
                    self.client.search_all_tweets,
                    # conversation with error (1469222907477962753), conversation with quote (1455259652300566530)
                    # Quote of Tweet in 1455259652300566530 with own conversation (1550189058059653122)
                    query=f'conversation_id:{self.conversation_id}',
                    # these fields are mandatory because they minimally describe a Reply-Tree.
                    tweet_fields=['conversation_id', 'referenced_tweets'],
                    **self.kwargs
            ):
                # Each page is the Response(data, includes, errors, meta) of size max_results.
                # Data will contain the requested Tweets holding the information defined in tweet_fields.
                # Includes provide all further information for the Tweets in Data which was specified in expansions.
                # Error will show all minimal information to reconstruct Tweets leading to error because of deletion etc...
                t0: float = time.time()
                if not page.data:
                    # in the case there is no conversation present because there is only a Root-Tweet.
                    time.sleep(round(1 - (time.time() - t0) % 1))
                    continue
                for tweet in page.data:
                    # <Response>.data contains all resulting Tweets having the requested information in data.
                    # The nodes in <Response>.data are accessible and can therefore be directly written into the database.
                    reply_tweet_data: dict = {'tweet_id': tweet.id,
                                              'conversation_id': tweet.conversation_id,
                                              'parent_id': None}

                    # If a Tweet holds the field referenced_tweets then there exists at least one other Tweet referenced.
                    if tweet.referenced_tweets:
                        # The referenced Tweets can be accessed and provide the type
                        # (Reply, Retweet, Quote (Retweet + text)).
                        # A Quote can also be a Reply in a conversation but with a Link to the original Tweet.
                        # Furthermore, if Quote is used as a Reply by quoting a Tweet of another conversation the
                        # conversation_id of the referenced_tweet is taken and not the one of the quoted (original) Tweet.
                        # A Reply binds a Tweet to a conversation (Reply-tree)
                        references: List[ReferencedTweet] = tweet.referenced_tweets
                        # The conversation (reply-tree) is reconstructed by using the conversation_id.
                        # Therefor, if a Tweets has a non-empty reference_tweets-field, it can be assumed to have at least
                        # one Reply-Tweet.
                        referenced_tweet: ReferencedTweet = next(
                            filter(lambda ref: ref.type == "replied_to", references))
                        # If a Tweet references to another Tweet via the replied_to-relation the referencing Tweets is a
                        # Reply to the referenced Tweet in the same conversation (Reply-tree).
                        reply_tweet_data['parent_id'] = referenced_tweet.id
                    reply_tweet: dict = self._add_tweet(tweet_id=reply_tweet_data['tweet_id'],
                                                        conversation_id=reply_tweet_data['conversation_id'],
                                                        parent_id=reply_tweet_data['parent_id'])
                time.sleep(round(1 - (time.time() - t0) % 1))
        print("Took:", str(datetime.timedelta(seconds=time.time() - t0_global)))
        print("Obtained Tweets:", len(self.tweets))

    def write_to_csv(self, path: Path = './reply_tree.csv') -> None:
        """
        This method writes the obtained tweets of the calling ReplyTree to a designated csv-file.

        It is important to first run .obtain() since the methods depends on the obtained tweets.
        Furthermore, each row will be appended to the specified csv-file.
        If this file is already existing, then the header-line will not be written again.

        :param path: Path to where the file should be written.
        :return: Nothing
        """
        fieldnames: list[str] = ['tweet_id', 'conversation_id', 'parent_id']
        file_exists = os.path.exists(path)
        with open(path, 'a', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerows(self.tweets.values())
