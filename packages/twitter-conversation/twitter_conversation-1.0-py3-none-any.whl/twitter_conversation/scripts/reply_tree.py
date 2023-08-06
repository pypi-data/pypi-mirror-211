import argparse
import datetime
import os
import time
from pathlib import Path

import pandas as pd
import tweepy as tweepy

from twitter_conversation.obtain import ReplyTree, Moisturizer


def main():
    # todo: add an option to skip the obtainment reply-tweets
    # todo: let the other scripts also save the file and test this
    parser = argparse.ArgumentParser(description="Yet another python script to obtain Twitter conversations.\n"
                                                 "This script also need the following env-variables:\n"
                                                 "  1. BEARER_TOKEN: To access the Twitter-API\n",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-s", "--start", type=datetime.datetime.fromisoformat,
                        default=datetime.datetime(tzinfo=datetime.timezone.utc,
                                                  year=2006, month=3, day=21,
                                                  hour=0, minute=0, second=0, microsecond=0),
                        # The first day of the Twitter-database records
                        help="The utc-time in the past where to start the search (default today 0 o'clock).")

    parser.add_argument("-e", "--end", type=datetime.datetime.fromisoformat,
                        default=datetime.datetime.utcnow() - datetime.timedelta(seconds=10),
                        # This day but at now.
                        help="The utc-time where to end the search (default today).")

    parser.add_argument("-p", "--path", type=Path,
                        default='./reply_tree.csv',
                        help="The path to the named csv-file where the obtained tweets should be written to.")

    parser.add_argument("-or", "--only-root", type=bool,
                        default=False,
                        action=argparse.BooleanOptionalAction,
                        help="By using this flag the root-tweets will be obtained and the reply-tweets are skipped.")

    subparsers = parser.add_subparsers(help='The mode for obtaining conversations.', required=True, dest="mode")

    # Conversation by one single conversation_id
    parser_conversation_id = subparsers.add_parser('single_conversation',
                                                   help='Use if a single conversation should be reconstructed while \
                                                   providing only one conversation_id.')

    parser_conversation_id.add_argument("-c", "--conversation", type=int,
                                        required=True,
                                        help="A single conversation_id of the conversation which should \
                                            be reconstructed")

    # Conversations by a csv-file having the IDs of conversation-starting Tweets.
    parser_conversation_starting_tweets = subparsers.add_parser('multiple_conversations',
                                                                help='Use if multiple conversations should be \
                                                                    reconstructed while providing a csv-file holding \
                                                                    the conversation_ids of interest.')

    parser_conversation_starting_tweets.add_argument("-s", "--starting_tweets", type=Path,
                                                     required=True,
                                                     help="A path to a csv-file having all IDs of conversation-starting\
                                                         Tweets in a column twitter_id.")
    parser_conversation_starting_tweets.add_argument("-i", "--index", type=str,
                                                     required=False,
                                                     default='tweet_id',
                                                     help="Name of the index column in the csv-file handed over. ")

    # Search for conversation starting Tweets
    parser_search_conversations = subparsers.add_parser('search_conversations',
                                                        help='Use if conversations should be obtained by searching\
                                                            for root-tweets by their topic.')

    parser_search_conversations.add_argument("-t", "--topic", type=str, default='abortion',
                                             help="The topic-word (hashtag eg. #<abortion>) of which to be present\
                                                 in the root-tweets.")

    # moisturize tweets with text.
    parser_moisturize_tweets = subparsers.add_parser('moisturize_tweets',
                                                     help='Use if there is a csv-file with reply-trees (tweets)\
                                                             to be hydrated with text.')

    parser_moisturize_tweets.add_argument("-d", "--dry_tweets", type=Path,
                                          required=True,
                                          help="A path to a csv-file having all IDs of dry (dehydrated)\
                                                             tweets in a column twitter_id.")
    parser_moisturize_tweets.add_argument("-i", "--index", type=str,
                                          required=False,
                                          default='tweet_id',
                                          help="Name of the index column in the csv-file handed over. ")

    args = parser.parse_args()
    args_config = vars(args)

    print('########## CONFIGURATION ##########')
    for argument, value in args_config.items():
        print(argument, ':', value)

    print('########## SETUP ##########')
    # setup tweepy-client
    client = tweepy.Client(
        bearer_token=os.environ['BEARER_TOKEN'],
        wait_on_rate_limit=True  # Tweepy does not handle 429 as it should. Have a look at your code for this problem.
        # what is in the header of response?
    )

    print('########## OBTAIN ##########')
    # Decide how to obtain conversations
    if args_config.get('mode') == "single_conversation":
        single_reply_tree: ReplyTree = ReplyTree(client,
                                                 conversation_id=args_config.get('conversation'),
                                                 start_time=args_config.get('start'),
                                                 max_results=500)
        single_reply_tree.obtain(only_root=args_config.get('only_root'))
        single_reply_tree.write_to_csv(path=args_config.get('path'))

    elif args_config.get('mode') == "multiple_conversations":
        conversation_starting_tweets: pd.DataFrame = pd.read_csv(args_config.get('starting_tweets'),
                                                                 index_col=args_config.get('index'))
        # Drop duplicated indices and keep only the unique ones
        conversation_starting_tweets = conversation_starting_tweets[~conversation_starting_tweets.index.duplicated()]
        for conversation_starting_tweet in conversation_starting_tweets.index:
            multiple_reply_tree: ReplyTree = ReplyTree(client,
                                                       conversation_id=conversation_starting_tweet,
                                                       start_time=args_config.get('start'),
                                                       max_results=500)
            multiple_reply_tree.obtain(only_root=args_config.get('only_root'))
            multiple_reply_tree.write_to_csv(path=args_config.get('path'))
    elif args_config.get('mode') == "search_conversations":
        t0_global: float = time.time()
        for page in tweepy.Paginator(
                client.search_all_tweets,
                query=f"(#{args_config.get('topic')}) lang:en -is:reply -is:retweet -is:quote",
                tweet_fields=['conversation_id'],
                max_results=500,
                start_time=args_config.get('start'),
                end_time=args_config.get('end'),
                sort_order='relevancy'
        ):
            t0: float = time.time()
            if not page.data:
                # in the case there is no conversation present because there is only a Root-Tweet.
                time.sleep(round(1 - (time.time() - t0) % 1))
                continue
            for tweet in page.data:
                search_reply_tree: ReplyTree = ReplyTree(client,
                                                         conversation_id=tweet.conversation_id,
                                                         start_time=args_config.get('start'),
                                                         max_results=500)
                search_reply_tree.obtain(only_root=args_config.get('only_root'))
                search_reply_tree.write_to_csv(path=args_config.get('path'))
            time.sleep(round(1 - (time.time() - t0) % 1))
        print('####################################')
        print("Took total:", str(datetime.timedelta(seconds=time.time() - t0_global)))
    elif args_config.get('mode') == "moisturize_tweets":
        t0_global: float = time.time()
        df_dry_tweets: pd.DataFrame = pd.read_csv(args_config.get('dry_tweets'),
                                                  index_col=args_config.get('index'))
        moisturizer: Moisturizer = Moisturizer(client, df_dry_tweets)
        moisturizer.hydrate()
        moisturizer.write_to_csv(path=args_config.get('path'))
        print('####################################')
        print("Took total:", str(datetime.timedelta(seconds=time.time() - t0_global)))

    print('########## CONGRATULATION ##########')


if __name__ == '__main__':
    main()
