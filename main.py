__author__ = "Ian Chan"
__copyright__ = "Copyright 2020, Ian Chan"
__credits__ = ["Ian Chan"]
__license__ = "GPL v3"
__version__ = "1"
__maintainer__ = "Ian Chan"
__email__ = "me@ian-chan.me"
__status__ = "Production"

from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
import covid19
from twilio.rest import Client
import os, time
from multiprocessing import Process

import configparser

config = configparser.ConfigParser()

if os.path.isfile('config.ini'):
    pass
else:
    config['Settings'] = {'Twilio SID': '',
                      'Authentication Token': '',
                      'Phone Numbers': '+18005555551, +18005555552',
                      'From Number' : '+8005555555',
                      'Country': 'US',
                      }
    
    with open('config.ini', 'w+') as configfile:
        config.write(configfile)
    
    print("Configuration file created")
    print("Edit configuration file then run again")
    print("Press ENTER key to exit")
    input()
    exit()

config.read('config.ini')

settings = config['Settings']
sid = settings.get('Twilio SID')
auth = settings.get('Authentication Token')
fromNumber = settings.get('From Number')
phoneNumbers = settings.get('Phone Numbers')
phoneNumbers = phoneNumbers.split(',')
phoneNumbers = [x.strip(' ') for x in phoneNumbers]
country = settings.get('Country')
country = country.lower()
altAPI = False #Does nothing



app = Flask(__name__)

@app.route('/')
def main():
    return(covid19.getData('page', country, False, altAPI))

def update():
    while True:
        time.sleep(60)
        if covid19.getData('message', country, True, altAPI) == 'No Change':
            pass
        else:
            config.read('config.ini')
            phoneNumbers = settings.get('Phone Numbers')
            phoneNumbers = phoneNumbers.split(',')
            phoneNumbers = [x.strip(' ') for x in phoneNumbers] 
            client = Client(sid, auth)
            for currentNumber in phoneNumbers:
                print("Sending message to: "+currentNumber)
            message = client.messages.create(
            to=currentNumber,
            from_= fromNumber,
            body=covid19.getData('message', country, False, altAPI))
            print(message.sid)
        #return(covid19.getData('page', country, False, altAPI))


    
@app.route('/config.ini')
def block():
  return Response(status=403)

@app.route('/sms', methods=['POST'])
def sms():
    print("Received text")
    resp = MessagingResponse()
    body = request.values.get('Body', None)
    body = body.lower()

    if ('hi' in body) or ('hello' in body) or ('help' in body):
        resp.message("Hello! Thanks for your interest in keeping updated with COVID-19 statistics. Ask me for the latest covid-19 cases or to give you an update, and you will receive the latest statistics.")
    elif ('update' in body) or ('latest' in body):
        resp.message(covid19.getData('message', country, False, altAPI))

    elif ('thank' in body):
        resp.message("No problem!")

    elif 'stop' in body:
        print('working')
        config.read('config.ini')
        phoneNumbers = settings.get('Phone Numbers')
        numberToRemove = request.values.get('From', None)
        newPhone = phoneNumbers.replace(", "+numberToRemove, "")
        config.set('Settings', 'Phone Numbers', newPhone)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        resp.message("Remove from list")
    
    elif 'start' in body:
        print('Subscribing...')
        config.read('config.ini')
        phoneNumbers = settings.get('Phone Numbers')
        numberToAdd = request.values.get('From', None)
        newPhone = phoneNumbers + ', '+numberToAdd
        config.set('Settings', 'Phone Numbers', newPhone)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    elif ('world' in body):
        resp.message(covid19.getWorld('message', altAPI))
    else:
        try:
            currentCountry = covid19.convertCountry(body)
            resp.message(covid19.getData('message', currentCountry, False, False))
        except:
            resp.message("Sorry, I don't understand. If you'd like to find a country, reply with your country name.")
    return str(resp)



@app.route('/call', methods=['POST'])
def call():
    print("Received call")
    resp = VoiceResponse()
    resp.say(covid19.getData('call', country, False, altAPI))
    return str(resp)

if __name__ == "__main__":
    Process(target=update).start()
    app.run(host='0.0.0.0', port='8080',debug=False)