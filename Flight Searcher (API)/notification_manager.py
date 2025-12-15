from twilio.rest import Client
import requests
from dotenv import load_dotenv, find_dotenv
import os

dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self._ACCOUNT_SID = os.getenv("TWILLIO_ACCOUNT_ID")
        self._AUTH_TOKEN = os.getenv("TWILLIO_AUTH_TOKEN")

    def enviar_mensagem(self, body):
        message = self.client.messages.create(
            from_=f'whatsapp:{os.environ["TWILIO_WHATSAPP_NUMBER"]}',
            body= body,
            to=f'whatsapp:{os.environ["TWILIO_VERIFIED_NUMBER"]}'
        )
        print(message.sid)