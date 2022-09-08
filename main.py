# Standar library
import json
import threading
# Third party library
from beem.blockchain            import Blockchain
from beem                       import Steem
# Local
from features.tweets            import manage_tweets
from error.exception_handling   import exception_handling
from error.exceptions           import Exception_Handling
from settings.general           import *
from utils.const                import *
from utils.rate_limits          import verify_limit_of_requests
from utils.utils                import from_list_to_str, build_url, category_is_empty, required_tags, empty_json

# Settings
cfg = Config()
# Exceptions
excpt = Exception_Handling()

def stream(feature):
    '''
    Listen to the Blockchain Steem
    '''
    try:
        chain = Steem(node=NODES)
        # blockchain instance
        blockchain = Blockchain(blockchain_instance=chain, mode="head")
        stream = blockchain.stream(opNames=['comment'])  # stream comments only
        print('Searching...')
        for post in stream:
            try:
                if feature == "tweet_with_the_configured_account":
                    if verify_limit_of_requests(MINUTES, LIMIT_RATE_FOR_15_MINUTES, TIME_IN_MINUTES_OF_THE_RATE_LIMIT,"default"):
                        continue
                    if verify_limit_of_requests(HOURS, LIMIT_RATE_FOR_3_HOURS, TIME_IN_HOURS_OF_THE_RATE_LIMIT,"default"):
                        continue
                author = post['author']
                permlink = post['permlink']
                category = post['parent_permlink'] if post['parent_permlink'] and not post['parent_author'] else ""
                json_metadata = json.loads(post["json_metadata"] if post["json_metadata"] else '{ }')
                try:
                    tags = [] if not "tags" in json_metadata.keys() else json_metadata["tags"]
                except AttributeError:
                    tags = []
                if author in cfg.list_of_accounts_to_ignore:
                    continue
                if cfg.list_of_tags_to_ignore and required_tags(tags,cfg.list_of_tags_to_ignore):
                    continue
                if category in cfg.list_of_communities_to_ignore:
                    continue
                if post['parent_permlink'] and post['parent_author']:
                    continue
                if cfg.rules["only_specific_communities"]["activate"] and not category in cfg.rules["only_specific_communities"]["values"]:
                    continue
                if cfg.rules["only_specific_tags"]["activate"] and not required_tags(tags,cfg.rules["only_specific_tags"]["values"]):
                    continue
                if cfg.features["personalized_accounts"]["activate"]:
                    # start action thread
                    make_a_twet(author, permlink, tags,category, feature)
                    continue
                make_a_twet(author, permlink, tags,category, feature)
            except Exception as e:
                dict_exceptions = excpt.twet
                exception_handling(e,"twet",dict_exceptions) 
    except Exception as e:
        dict_exceptions = excpt.stream
        exception_handling(e,"stream",dict_exceptions) 

def make_a_twet(author, permlink, tags, category, feature):
    try:
        twet = ""
        category = category_is_empty(category,tags)
        url = build_url(BASE_URL,author,permlink,category if category else "")
        end = f'{from_list_to_str(tags)} {from_list_to_str(cfg.custom_labels)}'
        twet += f'{cfg.start_comment} \n{url} \n{end} \n{cfg.end_comment}'
        response = manage_tweets(feature,twet)
    except Exception as e:
        if response:
            print(response)
        dict_exceptions = excpt.make_a_twet
        exception_handling(e,"make_a_twet",dict_exceptions) 


if __name__ == '__main__':
    try:
        empty_json("data/hard_pause.json")
        empty_json("data/rate_limit.json")
        count_f = {"count":0,"feature":""}
        for feature in FEATURES:
            if cfg.features[feature]["activate"]:
                count_f["count"] += 1
                count_f["feature"] = feature
        if count_f["count"] == 1:
            print("The bot has started with the feature: " + count_f["feature"])
            stream(count_f["feature"])
        elif count_f["count"] > 1:
            print("The bot could not start because there is more than one feature to publish tweets activated")
        else:
            print("The bot could not start because there is no activated feature")
    except (KeyboardInterrupt, SystemExit):
        print("--------------------------------------------------")
        print("The bot has stopped.")
