import os
import requests
from dotenv import load_dotenv, find_dotenv

dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")
        self.SHEETY_USERNAME = os.getenv("SHEETY_USERNAME")
        self.SHEETY_PASSWORD = os.getenv("SHEETY_PASSWORD")
        self.SHEETY_PUT_ENDPOINT = os.getenv("SHEETY_PUT_ENDPOINT")

    def get_data(self):
        response = requests.get(url = self.SHEETY_ENDPOINT, auth = (self.SHEETY_USERNAME, self.SHEETY_PASSWORD))
        data = response.json()
        return data
    
    def update_data(self, city):
        row_id = city["id"]
        response = requests.put(url = f"{self.SHEETY_PUT_ENDPOINT}{row_id}", json = {"price": city}, auth = (self.SHEETY_USERNAME, self.SHEETY_PASSWORD))
