# import requests
# from flask import Flask, request, jsonify

# app = Flask(__name__)

# TELEGRAM_BOT_TOKEN = '6176422429:AAHpWNC6B_rmnRVpoF1ueIhtiD3JOs2twDI'
# TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/'

# # Store received messages and user data
# user_data = {}

# def send_message(chat_id, text):
#     url = f"{TELEGRAM_API_URL}sendMessage"
#     payload = {
#         'chat_id': chat_id,
#         'text': text
#     }
#     response = requests.post(url, json=payload)
#     return response.json()

# @app.route('/read_msg', methods=['GET'])
# def read_msg():
#     update_id = request.args.get('update_id', type=int)
#     # if update_id is None:
#     #     return jsonify({'error': 'update_id parameter is required'}), 400
    
#     base_url = "https://api.telegram.org/bot6176422429:AAHpWNC6B_rmnRVpoF1ueIhtiD3JOs2twDI/"
#     # parameters = {
#     #     'offset': update_id
#     # }

#     response = requests.get(f"{base_url}getUpdates")
#     if response.status_code == 200:
#         return jsonify(response.json())
#     else:
#         return jsonify({'error': 'Failed to fetch updates'}), response.status_code

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     update = request.json
#     if 'message' in update:
#         chat_id = update['message']['chat']['id']
#         message_text = update['message']['text']
        
#         if chat_id not in user_data:
#             user_data[chat_id] = {}
        
#         # If message contains an email, store it
#         if '@' in message_text:
#             user_data[chat_id]['email'] = message_text
#             send_message(chat_id, "Thanks! Please provide your name.")
#         elif 'email' in user_data[chat_id]:
#             # Store the name if email is already provided
#             user_data[chat_id]['name'] = message_text
#             send_message(chat_id, "Thank you for providing your name!")
#         else:
#             send_message(chat_id, "Please provide your email first.")
        
#     return 'OK'

# @app.route('/user/<int:chat_id>', methods=['GET'])
# def get_user_info(chat_id):
#     if chat_id in user_data and 'email' in user_data[chat_id]:
#         return jsonify({'name': user_data[chat_id].get('name'), 'email': user_data[chat_id]['email']})
#     else:
#         return jsonify({'error': 'User not found or email not provided'}), 404

# if __name__ == '__main__':
#     app.run(debug=True)



import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = '6176422429:AAHpWNC6B_rmnRVpoF1ueIhtiD3JOs2twDI'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/'

# Store user data and their current state
user_data = {}
user_state = {}

def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=payload)
    return response.json()

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.json
    if 'message' in update:
        chat_id = update['message']['chat']['id']
        message_text = update['message']['text']
        
        if chat_id not in user_state:
            user_state[chat_id] = 'waiting_for_name'
            send_message(chat_id, "Please provide your name.")
        
        current_state = user_state[chat_id]
        
        if current_state == 'waiting_for_name':
            user_data[chat_id] = {'name': message_text}
            user_state[chat_id] = 'waiting_for_address'
            send_message(chat_id, "Thanks! Please provide your address.")
        
        elif current_state == 'waiting_for_address':
            user_data[chat_id]['address'] = message_text
            user_state[chat_id] = 'waiting_for_gender'
            send_message(chat_id, "Thank you! Please provide your gender.")
        
        elif current_state == 'waiting_for_gender':
            user_data[chat_id]['gender'] = message_text
            user_state[chat_id] = 'completed'
            send_message(chat_id, "Thank you for providing all the information!")
        
        else:
            send_message(chat_id, "You have already provided all the information.")

    return 'OK'

@app.route('/user/<int:chat_id>', methods=['GET'])
def get_user_info(chat_id):
    if chat_id in user_data:
        return jsonify(user_data[chat_id])
    else:
        return jsonify({'error': 'User data not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)



