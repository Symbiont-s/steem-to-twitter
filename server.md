### Server

A small Web server that will allow you to obtain the authorization of different accounts and store them.

### Web server links

The initialpage that will redirect you to the link to authorize the Twitter app.

Syntax
```
http://[SERVER_IP]:5120
```

Example:
```
http://999.999.999.999:5120
```

### Main Requirements  

* Python "3.8";
* gunicorn;
* tweepy;
* screen;
* tinydb.

# Configure and run the server

## Configure the server

To configure the server you must create a file called config.py inside the settings folder and copy all the code from the configExample.py file, then you must complete several options inside the config.js file.

The 'CONSUMER_KEY' and 'CONSUMER_SECRET' are required to access the Twitter app.

### Start the Web server and Leave it Running on Your Server

* You need to install the proper Python system packages to run your bot on your server.

* Install python3, python3-venv, and screen:

```
sudo apt update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
sudo apt install python3-venv
sudo apt install pipenv
```

* You must open one of the server ports so that the web application listens to requests through this port, in this case, we will use 5120. Execute the following command.

```
sudo ufw allow 5120
```

 
* Without this tool, if you were to exit your terminal while the bot was running, the process would terminate, and your Web server would go offline. With this tool, you can connect and disconnect to sessions so your code remains running. So, you are going to start a screen session with the name ```webserver```(can be any name):

```
screen -R webserver
```

* Screen will prompt you with a license agreement. Press Return to continue.

* To use the Web server you need to have pipenv installed.

* Inside the screen session, navigate to the bot directory ````cd Steem-Twitter```, then install it with the command (you must have python installed previously):

* Create the virtual environment and install the dependencies:

```
pipenv shell
```

```
pipenv install
```

* To use the Web server you need to have gunicorn installed and have opened port 5120.

* Finally, run your Web server:

```
gunicorn --bind 0.0.0.0:5120 wsgi:app
```

* You can disconnect from the screen session using the key combination ```CTRL+A+D```, the bot will keep running.

* To reconnect to the bot session:

```
screen -r regbot
```

* The bot inside the screen session can be stopped by doing ```CTRL+C```.

* By typing ```exit``` you will exit the virtual environment, and executing again ```exit``` you will exit the screen session and close it. ```CTRL+A+K``` can also be used to kill the session.
