# Character AI telegram bot
This is a project consisting of a telegram bot, a small web app and postgreSQL.
In the telegram bot, you can select a character and chat with him. 
Character selection is done through the web app. 
The bot uses chat-gpt-3.5 to communicate. 
Also used by Amplitude to track user actions.


### Preinstallation Requirements 
 - Get API KEYS:
    * Telegram Bot Token
    * Amplitude Token
    * Open AI Token
- Rename `example_conf.yaml` to `conf.yaml` and fill it with:
    * Telegram Bot Token (BOT_TOKEN)
    * Amplitude Token (AMPLITUDE_API_KEY)
    * Open AI Token (OPEN_API_TOKEN)
    * Server host address (web_app_host): "127.0.0.1" for local test
    
### Installation Requirements
 - Docker      

### Getting Started  
To build and run the project, follow these steps:   

- Build the project: make build   
- Start the project: make start   
- Stop the project: make stop 
- Remove database artifacts: make clean   
- Restart the project (build and start): make restart 


