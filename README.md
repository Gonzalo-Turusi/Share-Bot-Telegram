# Telegram Bot

## Project Description

This project is a Telegram bot designed to provide various functionalities, including alert management, subscription to notifications, and financial information retrieval. The bot is built using `python-telegram-bot` and integrates with several APIs and services to offer a comprehensive and useful experience.

## Architecture

The architecture of the bot is modular and follows a clear separation of concerns. Here are the main components:

1. **Command Handlers**: These handle the various commands that users can send to the bot. Each command has its own handler class.
2. **Managers**: These classes manage different aspects of the bot's functionality, such as subscriptions, alerts, and database interactions.
3. **Database**: The bot uses SQLite for storing user data, subscriptions, and other persistent information.
4. **APIs**: The bot integrates with external APIs to fetch financial data and other information.
5. **Logging**: All activities and errors are logged to a file for easy monitoring and debugging.

## Requirements

### Necessary Files and Folders

1. **File `ADMITTED_AD_USERS.txt` in the `/temp` folder**:
   This file should contain a list of users authorized to interact with the bot. Each line of the file should contain a username.

2. **Folder `/encryption` with the file `secret.key`**:
   The `/encryption` folder should contain the `secret.key` file, which is used for encrypting and decrypting sensitive data in the configuration file.

### Configuration

1. **Configuration File `config.yaml`**:
   The `config.yaml` file must be correctly configured with the necessary credentials and paths. Here is an example of what it should look like:

   ```yaml
 DESA:
     BOT:
       TOKEN: "your-telegram-bot-token"
     PATHS:
       SCRIPTS_PATH: ".\\scripts\\"
       RESOURCES_PATH: ".\\temp\\"
     AUTH:
       CREDENTIAL_VALIDITY_DAYS: 90
       VALIDATION_KEY: "your-validation-key"
     LOGS:
       LOG_PATH: "logs\\bot.log"
       LOG_LEVEL: "DEBUG"
     DATABASES:
       BOT_TELEGRAM:
         SERVER: ".\\"
         SOURCE: "Bot_Telegram.db"
     APIKEYS:
       ALPHA_VANTAGE: "your-alpha-vantage-api-key"
       BCRA: "your-bcra-api-key"
     EMAIL:
       SMTP_SERVER: "smtp.gmail.com"
       SMTP_PORT: 587
       EMAIL_SENDER: "your-email@gmail.com"
       EMAIL_PASSWORD: "your-email-password"
       INTERVAL_FOR_SEND: 1
     ALERTS:
       TEST_ACTIVATED: True
       WORKER_INTERVAL: 1800
       RECIPIENTS: "recipient-email@gmail.com"

## Deployment
To deploy this application, first connect to the server.
1. Stop the Windows service "Telegram_BOT".
2. Copy the files, excluding those ignored in the `.gitignore` (e.g., temp, venv, logs, pycache, Bot_Telegram.db, etc.).
3. Replace the environment name on the server, which is done in the `config.py` file (DESA, TEST, PROD).
4. If new dependencies have been installed, follow these steps on the server:
    - Open a CMD in administrator mode.
    - Type `E:` to navigate to the E drive.
    - Type the command `E:\Telegram_BOT\venv\Scripts\activate` to activate the virtual environment. Now `(venv)` will appear before each line.
    - Then, run the command to install the new dependencies: `pip install -r .\requirements.txt`. For this to work, you should have run `pip freeze > requirements.txt` in your local environment.
5. Finally, restart the service.
6. You can check the logs to see any application output.

## Service Creation
If the service does not already exist, it needs to be created using the `nssm` application. Navigate to the folder where the executable is located (usually in `C:\nginx` on servers). Once the terminal is positioned in the `nssm` path, run the following command:
```sh
nssm install Telegram_BOT "E:\Telegram_BOT\venv\Scripts\python.exe" "E:\Telegram_BOT\app.py"