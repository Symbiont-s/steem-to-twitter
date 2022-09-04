'''
        A file to handle exceptions and responses

        The attributes of the Exception_Handling class represent a function of discordbot.py.

        Each attribute is a dictionary, where the keys are the errors and the values of those keys the responses that you want to print.
'''


class Exception_Handling:

    def __init__(self):

        self.stream={
            " ":"-"
        }
        
        self.twet={
            " ":"-"
        }
        
        self.make_a_twet={
            " ":"-"
        }
        
        self.register_token={
            " ":"-"
        }
     
        self.callback={
            "401 Unauthorized\nUnauthorized":"Error 401: Credentials are invalid - Unauthorized\nReview the credentials and regenerate them if necessary"
        }
        
        self.send_tweet = {
            "401 Unauthorized\nUnauthorized":"Error 401: Credentials are invalid - Unauthorized\nReview the credentials and regenerate them if necessary"
        }
        
        self.manage_tweets = {
            " ":"-"
        }
        
        self.verify_limit_of_requests = {
            " ":"-"
        }
        
        self.register_or_update = {
            " ":"-"
        }
        
        self.hard_pause = {
            " ":"-"
        }