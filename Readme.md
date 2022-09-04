### Steem-Twitter 

Steem-to-Twitter is a bot designed to listen to the Steem blockchain, identify the publications that users are making and share them as links on Twitter. The bot can listen to all accounts on the blockchain or a list of specific accounts. You can also configure the message of the tweet, as well as configure the tags and other things.

## Main Features

The bot has three main functionalities to publish tweets and can only be activated one at a time in the configuration file.

### Post every tweet from multiple accounts

This functionality allows multiple accounts to post the same tweet. Accounts must authorize the app. The bot has a section that you can execute to authorize the application and for the bot to store the tokens of each Twitter account, to do this check the server.md file.

Note: If only one account has given authorization, then the tweets will be published from that account only.

### Post each tweet with a different account (rotating between different accounts)

This functionality allows multiple accounts to be rotated, allowing each new tweet to be posted by a new account. Accounts must authorize the app. The bot has a section that you can execute to authorize the application and for the bot to store the tokens of each account, to do this check the server.md file.

Note: If only one account has given authorization, then the tweets will be published from that account.

### Post tweets from a single account

Post tweets from a single account. To do this, you must provide the 'ACCESS_TOKEN' and 'ACCESS_TOKEN_SECRET' in the config.py file inside the settings folder.

### Main Requirements  

* Python "3.8";
* beem;
* tweepy;
* screen;
* tinydb.

### How to get Twitter app keys?

First of all, it is necessary to have a Twitter account, this account must have a verified phone. Below is a link on how to add a phone number to your Twitter account.

<a href="https://help.twitter.com/en/managing-your-account/how-to-add-a-phone-number-to-your-account">(How to add a phone number on twitter)</a> 

After adding the phone, you need to request a developer account by sending an application and be able to use the Twitter API.

<a href="https://developer.twitter.com/en/portal/petition/essential/basic-info">(How to create an app to use the Twitter API)</a> 

Once the Twitter team approves your app, you only need to obtain the keys. To get them, you need to go to the following <a href="https://developer.twitter.com/en/apps">link</a>  and then to the "keys and token" section (a key icon will appear in your app).

By default the token is read-only, to change this you must change the configuration so that it is read and write. In the following link, you will find a step-by-step tutorial to do it.

<a href="https://stackoverflow.com/questions/10567305/why-does-my-twitter-application-access-level-is-read-only-and-how-can-i-change/70586595#70586595">(How to allow read and write for your app)</a>

NOTE: It is essential that you configure the "Callback URI / Redirect URL" of the Twitter app in the following way:

Syntax
```
http://[SERVER_IP]:5120/callback
```

Example:
```
http://http://999.999.999.999:5120/callback
```

This is mandatory to activate and use the webserver to authorize accounts.

# Configure and run the bot

## Configure the bot

To configure the bot you must place the corresponding information in the general.py file inside the settings folder. There you will find several options that you must configure. You must also create a file called config.py inside the settings folder and copy all the code from the configExample.py file, then you must complete several options inside the config.py file just as you did in the general.py file.

### Start the Bot and Leave it Running on Your Server

* You need to install the proper Python system packages to run your bot on your server.

* Install python3, python3-venv, and screen:

```
sudo apt update && sudo apt install python3 python3-venv screen
```

* Ater populating the 'config.py' and 'general.py' files inside the setting folder with the proper data, you are going to use a tool called screen to create a virtual terminal.
  
* Without this tool, if you were to exit your terminal while the bot was running, the process would terminate, and your bot would go offline. With this tool, you can connect and disconnect to sessions so your code remains running. So, you are going to start a screen session with the name ```steem-twitter```(can be any name):

```
screen -R steem-twitter
```

* Screen will prompt you with a license agreement. Press Return to continue.

* To use the bot you need to have pipenv installed.

* Inside the screen session, navigate to the bot directory ````cd Steem-Twitter```, then install it with the command (you must have python installed previously).

* Create the virtual environment and install the dependencies:

```
pipenv shell
```

```
pipenv install
```

* Finally, run your bot:

```
python3 main.py
```

or

```
python main.py
```

* You can disconnect from the screen session using the key combination ```CTRL+A+D```, the bot will keep running.

* To reconnect to the bot session:

```
screen -r steem-twitter
```

* The bot inside the screen session can be stopped by doing ```CTRL+C```.

* By typing ```exit``` you will exit the virtual environment, and executing again ```exit``` you will exit the screen session and close it. ```CTRL+A+K``` can also be used to kill the session.

### License

GNU GENERAL PUBLIC LICENSE Version 3.

Brought to you by the Symbionts Team.
