"""
This bot listens to port 5002 for incoming connections from Facebook. It takes
in any messages that the bot receives and echos it back.
"""
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)

ACCESS_TOKEN = "EAAbv6kggGtYBAI6X6TxqjZCKxjuJidZAzBzqD3A4yGjQ3quRTVgJCYcEyGvZAPl0tSUgHxghL3j5fbZAMzqLYbKqDTEao13ZBFDghTGwW1qYkmPPZCRnvTephwl6TEBrLsmxp8LIuCnoHKYq5mzwxkDmm9PD1uP0HR7ZCpClTveBZCTKUHSFtjyr"
VERIFY_TOKEN = "TESTINGTOKEN"
bot = Bot(ACCESS_TOKEN)


@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return 'Invali'

    if request.method == 'POST':
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for x in messaging:
                if x.get('message'):
                    recipient_id = x['sender']['id']
                    if x['message'].get('text'):
                        message = x['message']['text']
                        bot.send_text_message(recipient_id, message)
                else:
                    pass
        return "Success"


if __name__ == "__main__":
    app.run(port=1337, debug=False)