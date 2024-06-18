import json
from flask import Flask, render_template, current_app, redirect, url_for, request
import aiohttp
import asyncio

app = Flask(__name__)

# Carregar configurações do arquivo config.json
with open('config.json') as f:
    config = json.load(f)

app.config.update(config)


@app.route("/")
def index():
    return render_template('index.html', name=__name__)


@app.route('/welcome', methods=['POST'])
def welcome():
    # Use asyncio.run para chamar uma função assíncrona dentro de uma função síncrona
    asyncio.run(send_message(get_text_message_input(app.config['RECIPIENT_WAID'], 'Welcome to the Flight Confirmation Demo App for Python!')))
    return redirect(url_for('index'))


async def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    async with aiohttp.ClientSession() as session:
        url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"
        try:
            async with session.post(url, data=data, headers=headers) as response:
                if response.status == 200:
                    print("Status:", response.status)
                    print("Content-type:", response.headers['content-type'])

                    html = await response.text()
                    print("Body:", html)
                else:
                    print("Failed to send message")
                    print("Status code:", response.status)
                    print("Response:", await response.text())
        except aiohttp.ClientConnectorError as e:
            print('Connection Error', str(e))


def get_text_message_input(recipient, text):
    return json.dumps({
        "messaging_product": "whatsapp",
        "preview_url": False,
        "recipient_type": "individual",
        "to": recipient,
        "type": "text",
        "text": {
            "body": text
        }
    })


if __name__ == '__main__':
    app.run(debug=True)
