import os
import sys
import json
from datetime import datetime
from pymessenger import Bot
import requests
from flask import Flask, request
import sqlite3
import json

app = Flask(__name__)

def check_id (uniqueid):
    try:
        cur.execute('SELECT * FROM students WHERE name={wn}'.format(wn=uniqueid))
        if cur.fetchone():
            return True
        else:
            return False
    except:
        pass

def check_word( word_name):
    cur.execute('SELECT addr FROM students WHERE name = {wn}'.format(wn=word_name))
    data = cur.fetchone()
    return data
    # if data is not None:
    #     cur.execute(
    #         'UPDATE students SET addr=(12345) WHERE name=(5)')
    #     return True
    # return False

conn = sqlite3.connect("C:\\Project\pythonsqlite.db")
cur=conn.cursor()
# print "Opened database successfully"

# # conn.execute("INSERT INTO students VALUES ('Boliang',NULL,NULL,NULL)")

# #  conn.execute("UPDATE students SET addr =('Hi World') WHERE name=(5)")

# check_id(4)

# conn.commit()




bot = Bot(os.environ["PAGE_ACCESS_TOKEN"])


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events

    data = request.get_json()
    # log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]  # the facebook ID of the person sending you the message
                    if check_id(sender_id):
                        cur.execute('SELECT addr FROM students WHERE name = ?',[sender_id])
                        data = cur.fetchone()[0]
                        cur.execute('SELECT city FROM students WHERE name = ?',[sender_id])
                        data1 = cur.fetchone()[0]
                        cur.execute('SELECT pin FROM students WHERE name = ?',[sender_id])
                        data2 = cur.fetchone()[0]
                        if data is None:
                            bot.send_text_message(sender_id,"Such a wonderful name!!! Now, could you give me your number?")
                            message_text = messaging_event["message"]["text"]
                            conn.execute('UPDATE students SET addr= ? WHERE name= ?', [message_text,sender_id])
                            conn.commit()
                        elif data1 is None:
                            bot.send_text_message(sender_id,"Got your number!")
                            message_text = messaging_event["message"]["text"]
                            conn.execute('UPDATE students SET city= ? WHERE name= ?', [message_text,sender_id])
                            conn.commit()
                            bot.send_location(sender_id)
                        elif data2 is None:
                            bot.send_text_message(sender_id,"Nice! I have got everything I need. I am on my way!")
                            # attachments = messaging_event["message"].get("attachments")
                            if messaging_event["message"].get("attachments"):
                                for att in messaging_event['message'].get('attachments'):
                                    lat=att['payload']["coordinates"]["lat"]
                                    longti=att['payload']["coordinates"]["long"]
                                    location=','.join((str(lat),str(longti)))
                                    conn.execute('UPDATE students SET pin= ? WHERE name= ?', [location,sender_id])
                                    conn.commit()
                            # conn.execute('UPDATE students SET pin= ? WHERE name= ?', [att["payload"]["coordinates"]["lat"],sender_id])
                            # conn.commit()
                            # attachment =json.loads(attachments)
                            # print attachment['url']
                            # location=attachments[0]
                            # print location
                            # location=attachments["payload"]["coordinates"]["lat"]
                            
                        else:
                            pass
                    else:
                        cur.execute("INSERT INTO students VALUES ({id},NULL,NULL,NULL)".format(id=sender_id))
                        bot.send_text_message(sender_id,"What's your name?")
                    # recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    # message_text = messaging_event["message"]["text"]  # the message's text
                    # if messaging_event["message"].get("text"):
                    #     bot.send_location(sender_id)
                    # if messaging_event["message"].get("attachments"):
                    #     bot.send_text_message(sender_id,"Got it")
                else:
                    pass
    conn.commit()
    return "ok", 200


if __name__ == '__main__':
    app.run(port=5000, debug=False)
