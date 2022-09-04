# Third party library
from flask                      import redirect, request,render_template
from tinydb                     import TinyDB, Query
import flask
import tweepy
# Local
from error.exception_handling   import exception_handling
from error.exceptions           import Exception_Handling
from settings.config            import CONSUMER_KEY, CONSUMER_SECRET

# TinyDB
tokensDB = TinyDB("data/tokens.json")
User = Query()
# Flask
app = flask.Flask(__name__)

def register_token(account, access_token, access_token_secret):
    try:
        exist = tokensDB.search((User.account == account))
        if not exist:
            tokensDB.insert({
                "account": account,
                "token": {
                    "access_token": access_token,
                    "access_token_secret": access_token_secret
                }
            })
            return f"Success registering {account} token <br> access-token={access_token}<br>access-token-secret={access_token_secret}"
        else:
            update_token(account, access_token, access_token_secret)
    except Exception as e:
        try:
            dict_exceptions = Exception_Handling().register_token
            exception_handling(e, "register_token", dict_exceptions)
        except Exception as error:
            print(error)
        return f"Failed to register token"

def update_token(account, access_token, access_token_secret):
    try:
        tokensDB.update({
            "token": {
                "access_token": access_token,
                "access_token_secret": access_token_secret
            }
        }, (User.account == account))
        return f"Success to update {account} token <br> access-token={access_token}<br>access-token-secret={access_token_secret}"
    except Exception as e:
        try:
            dict_exceptions = Exception_Handling().register_token
            exception_handling(e, "register_token", dict_exceptions)
        except Exception as error:
            print(error)
        return f"Failed to register token"

@app.route('/')
def index():
    try:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        return redirect(auth.get_authorization_url())
    except Exception as e:
        try:
            dict_exceptions = Exception_Handling().callback
            exception_handling(e, "callback", dict_exceptions)
        except Exception as error:
            print(error)
        e = e if not e is None else ""
        return f"Failed to redirect to authorization url <br> Error: {str(e)}"

@app.route('/callback', methods=['GET', 'POST'])
def callback():
    try:
        args = request.args
        oauth_token = args['oauth_token']
        oauth_verifier = args['oauth_verifier']
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.request_token = {'oauth_token': oauth_token,
                              'oauth_token_secret': oauth_verifier}
        auth.get_access_token(oauth_verifier)
        client = tweepy.Client(consumer_key=CONSUMER_KEY,
                               consumer_secret=CONSUMER_SECRET,
                               access_token=auth.access_token,
                               access_token_secret=auth.access_token_secret)
        account = client.get_me().data.username
        response = register_token(
            account, auth.access_token, auth.access_token_secret)
        return render_template("success.html", msg=response)
    except Exception as e:
        try:
            dict_exceptions = Exception_Handling().callback
            exception_handling(e, "callback", dict_exceptions)
        except Exception as error:
            print(error)
        return render_template("error.html", msg=f"Failed to register token")
    
