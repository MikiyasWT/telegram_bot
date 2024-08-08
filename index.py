from flask import Flask, request
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


base_url = os.getenv("TELEGRAM_API_URL")



def send_message(chat_id, text):
    """Send a message to a Telegram user."""
    url = base_url + 'sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=payload)
### function for reading in the responses to the data quality questions sent
def read_msg():
  resp=requests.get(base_url+"getUpdates")
  data=resp.json()

  return data['result']


@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming updates from Telegram."""
    updates = read_msg()
    for update in updates:

        if 'message' in update:
            chat_id = update['message']['chat']['id']
            text = update['message'].get('text', '')

            if text.startswith('/'):
                command, *args = text.split()
                if command == '/register':
                    send_message(chat_id, "Welcome! Use /help to see available commands.")
                elif command == '/dq':
                    send_message(chat_id, "/start - Welcome message\n/help - List commands\n/echo [text] - Echo back text")
                elif command == '/dqstats':
                    if args:
                        send_message(chat_id, ' '.join(args))
                    else:
                        send_message(chat_id, "Usage: /echo [text]")
                else:
                    send_message(chat_id, "Unknown command. Use /help to see available commands.")
            else:
                send_message(chat_id, "I only respond to commands. Use /help to see available commands.")

    return 'OK', 200


if __name__ == '__main__':
    app.run(debug=True)
