# xkcd-comics-telegram-bot
telegram bot for publishing xkcd comics

## Getting Started
Run main.py script

### Prerequisites
1. Crete a bot in telegram using https://t.me/BotFather.
2. Create a channel in telegram.
3. Add your bot to your channel as administrator.
4. Create environment variables in "your_project_folder\.env" file:
   TG_BOT_TOKEN= <- token for your telegram bot
   TG_CHANNEL_ID= <- id of your tg channel
   
   optional:
   POST_PERIOD= <- default period of posting images, hours. Default value = 4. 
   
5. Python3 should be already installed.
   Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
   -> packages, listed in requirements should be successfully installed. 

### Usage
If you want to publish a random comic, just run main.py:'
```
$ python main.py
``` 
Then, if everything was successful, you will see the following output: 
Start posting comics to the tg channel.

