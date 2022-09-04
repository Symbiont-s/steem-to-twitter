# Third party library
from tinydb                     import TinyDB, Query
from tweepy.errors              import TooManyRequests, Forbidden
import tweepy
# Local
from error.exception_handling   import exception_handling
from error.exceptions           import Exception_Handling
from settings.config            import *
from utils.const                import *
from utils.rate_limits          import register_or_update, verify_limit_of_requests, hard_pause

tokensDB = TinyDB("data/tokens.json")
currentAccount = TinyDB("features/account.json")
User = Query()

def send_tweet(token,twet ):
    response = ""
    try:
        # Initializing the Twitter API
        client = tweepy.Client(consumer_key=CONSUMER_KEY,
                            consumer_secret=CONSUMER_SECRET,
                            access_token=token["token"]["access_token"],
                            access_token_secret=token["token"]["access_token_secret"],
                            wait_on_rate_limit = True)
        response = client.create_tweet(text=twet)
        register_or_update(MINUTES,token["account"])
        register_or_update(HOURS,token["account"])
    except TooManyRequests as too_many:
        if too_many:
            print(str(too_many))
        print("Forced pause")
        hard_pause(token["account"])
    except KeyError as keyerror:
        print("The token has an incorrect structure")
        print(token, "current token")
        dict_exceptions = Exception_Handling().send_tweet
        exception_handling(keyerror,"send_tweet",dict_exceptions)    
    except Forbidden as duplicate:
        if duplicate is not None and str(duplicate) == "403 Forbidden\nYou are not allowed to create a Tweet with duplicate content.":
            pass
        else:
            print(response)
            dict_exceptions = Exception_Handling().send_tweet
            exception_handling(duplicate,"send_tweet",dict_exceptions) 
    except Exception as e:
        print(response)
        dict_exceptions = Exception_Handling().send_tweet
        exception_handling(e,"send_tweet",dict_exceptions) 
    finally:
        return response

def manage_tweets(feature, twet):
    try:
        # tweet_from_multiple_accounts_at_once
        response = ""
        if FEATURES.index(feature) == 0:
            tokens = tokensDB.all()
            for token in tokens:
                if verify_limit_of_requests(MINUTES, LIMIT_RATE_FOR_15_MINUTES, TIME_IN_MINUTES_OF_THE_RATE_LIMIT,token["account"]):
                    return response
                if verify_limit_of_requests(HOURS, LIMIT_RATE_FOR_3_HOURS, TIME_IN_HOURS_OF_THE_RATE_LIMIT,token["account"]):
                    return response
                response = send_tweet(token,twet)
        # tweet_rotating_between_multiple_accounts
        elif FEATURES.index(feature) == 1:
            tokens = tokensDB.all()
            # If there are tokens
            if tokens:
                current = currentAccount.all()
                # If the last account that sent a tweet has been registered
                if len(currentAccount) >= 1:
                    current = current[0]
                    # If it is the last account
                    if current["position"] >= len(tokens) - 1:
                        currentAccount.update({"position":0}, (User.account == "current"))
                        if verify_limit_of_requests(MINUTES, LIMIT_RATE_FOR_15_MINUTES, TIME_IN_MINUTES_OF_THE_RATE_LIMIT,tokens[0]["account"]):
                            return response
                        if verify_limit_of_requests(HOURS, LIMIT_RATE_FOR_3_HOURS, TIME_IN_HOURS_OF_THE_RATE_LIMIT,tokens[0]["account"]):
                            return response
                        response = send_tweet(tokens[0],twet)
                    # If it is not the last account
                    else:
                        currentAccount.update({"position":current["position"] + 1}, (User.account == "current"))
                        if verify_limit_of_requests(MINUTES, LIMIT_RATE_FOR_15_MINUTES, TIME_IN_MINUTES_OF_THE_RATE_LIMIT,tokens[current["position"] + 1]["account"]):
                            return response
                        if verify_limit_of_requests(HOURS, LIMIT_RATE_FOR_3_HOURS, TIME_IN_HOURS_OF_THE_RATE_LIMIT,tokens[current["position"] + 1]["account"]):
                            return response
                        response = send_tweet(tokens[current["position"] + 1],twet)
                else:
                    currentAccount.insert({"position":0, "account": "current"})
                    if verify_limit_of_requests(MINUTES, LIMIT_RATE_FOR_15_MINUTES, TIME_IN_MINUTES_OF_THE_RATE_LIMIT,tokens[0]["account"]):
                        return response
                    if verify_limit_of_requests(HOURS, LIMIT_RATE_FOR_3_HOURS, TIME_IN_HOURS_OF_THE_RATE_LIMIT,tokens[0]["account"]):
                        return response
                    response = send_tweet(tokens[0],twet)
        # tweet_with_the_configured_account
        elif FEATURES.index(feature) == 2:
            token = {
                "account": "default",
                "token": {
                    "access_token": ACCESS_TOKEN,
                    "access_token_secret": ACCESS_TOKEN_SECRET
                }
            }
            response = send_tweet(token,twet)
        return response
    except Exception as e:
        dict_exceptions = Exception_Handling().manage_tweets
        exception_handling(e,"manage_tweets",dict_exceptions) 
