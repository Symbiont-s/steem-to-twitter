'''
        The settings file for the bot.
'''

# Steem RPC nodes
NODES =["https://api.steemit.com"]

# Base url to generate the URL to publish in the tweet
BASE_URL = "https://steemit.com/"

class Config:

    def __init__(self):

        # functionalities
        self.features = {
            # Allows you to monitor a list of custom accounts
            "personalized_accounts": {
                # Enable or disable functionality
                # If it is deactivated, the bot will be aware of all the accounts of the blockchain
                "activate": False,
                # List of accounts to watch
                "list_of_accounts_to_follow": ["account_name_1","account_name_2"],
            },
            # Every time a tweet is made, it is published with each of the accounts that have given prior authorization and whose token is registered in the file tokens.json inside the data .
            # If only one account has given authorization then only the tweet will be published from that account
            "tweet_from_multiple_accounts_at_once" : {
                # Enable or disable functionality
                "activate": False,
            },
            # Every time a tweet is made, it is published with one of the accounts that has been previously authorized and whose token is registered in the tokens.json file inside the folder. There is a rotation between registered accounts so tweets are posted by a different account with each iteration.
            # If only one account has given authorization then only the tweet will be published from that account
            "tweet_rotating_between_multiple_accounts" : {
                # Enable or disable functionality
                "activate": False,
            },
            # tweet with the account configured in the config.py file inside the settings folder
            "tweet_with_the_configured_account":{
                # Enable or disable functionality
                "activate": True,
            }
        }
        
        self.rules = {
            # If it is active, only the links that are from these communities will be published.
            "only_specific_communities" : {
                # Enable or disable functionality
                "activate" : True,
                # community list
                "values" : ["community1","community2"]
            },
            # If it is active, only the links that contain any of the labels will be published.
            "only_specific_tags" : {
                # Enable or disable functionality
                "activate" : True,
                # tag list
                "values" : ["tag1","tag2"]
            }
        }
        
        # List of accounts to ignore, in the event that any account in the blockchain is being listened to, this will allow ignoring a list of accounts.
        self.list_of_accounts_to_ignore=["account_name_1","account_name_2"]

        # List of tags that will cause a post to be ignored
        self.list_of_tags_to_ignore=["tag1","tag2"]

        # List of communities that will cause a post to be ignored
        self.list_of_communities_to_ignore=["community1","community2"]

        # Customizable tags to post on the tweet.
        self.custom_labels =["tag1","tag2"]

        # Initial part of the tweet
        self.start_comment = "start message"
        # Final part of the teew
        self.end_comment = "end message"