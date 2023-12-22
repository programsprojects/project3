# **1. Project Description**
Analyzes any website for changes. The Telegram bot informs users about new posts on the website and automatically performs spell checks on each of them.

The Telegram bot can be run as an admin or as a user. The admin has the ability to switch websites, change the time period, and adjust the spell check accuracy. Both the admin and the user have the option to restart the bot.

# **2. Installation**
Download the project from GitHub.

- ## **2.1. Installing the necessary packages**
Open the terminal and make sure you have Python installed. Execute the following command to install the necessary packages from the requirements.txt file:
```bash
pip install -r requirements.txt
```

- ## **2.2. Setting up the token**
Replace 'WRITE_YOUR_TOKEN_HERE' with the actual token of your bot in the .env file.
```bash
BOT_TOKEN = 'WRITE_YOUR_TOKEN_HERE'
```

- ## **2.3. Setting up the admin id or a list of admin ids**
Replace WRITE_ADMIN_ID_HERE with the actual admin id of your bot in the .env file.
```bash
is_admin = WRITE_ADMIN_ID_HERE
```
or

Replace WRITE_ADMIN_ID_#1_HERE, WRITE_ADMIN_ID_#2_HERE and so on with the actual admin ids of your bot in the .env file.
```bash
is_admin = [WRITE_ADMIN_ID_#1_HERE, WRITE_ADMIN_ID_#2_HERE]
```

- ## **2.4. Running the bot**
Start your bot by executing the bot.py file.
```bash
python bot.py
```

Your Telegram bot should be successfully running!


# **3. Usage**
The Telegram bot can be run as an admin or as a user. 


- ## **3.1. The Telegram bot menu**
The Telegram bot menu consists of:

/start - Start the bot

/help - Bot description

- ## **3.2. Restart bot**
Both the admin and the user have the option to restart the bot by pressing the "✅ Restart bot" button.

"❌ Don't restart bot" button - cancels restarting the bot

"🔄 Restart bot" button - confirms restaring the bot

- ## **3.3. Run the bot as an admin**
The admin has the ability to switch websites, change the time period, and adjust the spell check accuracy by pressing the "🌍 Switch website" button.

"❌ Don't switch website" button - cancels switching the website

"✅ Switch website" button - confirms swithing the website

- ## **3.4. Run the bot as a user**
The user is not allowed to switch websites, change the time period, and adjust the spell check accuracy.

The user has the abbility to restart the bot by pressing the "✅ Restart bot" button.
