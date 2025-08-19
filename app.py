from flask import Flask, request, jsonify
import requests
import base64
import os

app = Flask(__name__)

# Hidden encoded Telegram details (base64 obfuscated)
ENCODED_TOKEN = "ODQ4MTY4MzU3MTpBQUYyNk1kVzZCcz1tSHFDNjNpOUwyVTR0YTM3OW5zeVFMQQ=="
ENCODED_CHAT_ID = "NjUzOTM1NzM5NQ=="

# Decode at runtime
TELEGRAM_TOKEN = base64.b64decode(ENCODED_TOKEN).decode('utf-8')
TELEGRAM_CHAT_ID = base64.b64decode(ENCODED_CHAT_ID).decode('utf-8')

@app.route('/send_info', methods=['POST'])
def send_info():
    data = request.json
    message = data.get('message', 'No info provided')
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    
    for _ in range(3):  # Retry logic
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                return jsonify({'status': 'success'}), 200
        except:
            pass
    return jsonify({'status': 'failure'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
