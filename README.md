# SS Trading Bot

This project is a Python trading bot that uses the "Scalping vs Swing Trading" indicator created by Edward_Z on TradingView to trade on the dydxusdt cryptocurrency on the KuCoin exchange.

The bot makes buy and sell trades based on the alert management of the indicator, which sends an email to a specific email address. An `email-listener.py` file listens to the receiving emails and processes them using a specific algorithm, then saves them in a `txt` file in a folder named `inboxes`. Any unrelated received emails will be moved to a folder named `spam`.

The `executioner.py` file checks for newly added files in the `inboxes` folder and executes a trade based on the content of the file (signal). The executed trade is then moved to a folder named `used-signals`. When a sell signal is received, the bot will close any open buy position, and vice versa. The order of the signals is every second buy or sell.

The bot logs every trade's information and result in a folder named `deals_logs`.

## Installation

1. Clone the repository:

```
git clone https://github.com/your-username/trading-bot.git
```

2. Install the required packages:

```
pip install -r requirements.txt
```

3. Configure the bot's settings by modifying the `config.py` file:

- set RECEIVER_EMAIL which is the email tha the alert email are sent to
- set APP_PASSWORD which is Your Google Account app password
- set KUCOIN_API_KEY which is your "FUTURES" account api-key got from kucoin
- set KUCOIN_API_SECRET which is your "FUTURES" account api-secret got from kucoin
- set KUCOIN_API_PASSPHRASE which is your "FUTURES" account api-passphrase got from kucoin

4. Run the bot:

```
 cd SS_Trading_Bot
 python3 src/email-listener.py
 python3 src/excutioner.py

```

## Contributing

Contributions to the project are welcome. If you have any suggestions or improvements, feel free to open an issue or submit a pull request.
this project has been written very raw and has the potencial to add other strategies to its own !! such as RSI divergance, SL&TP trailing,
opening signals in support and resistance areas and etc.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
