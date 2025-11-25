import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv

dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

class FlightSearch:
    
    def __init__(self):
        self._AMADEUS_GET_ENDPOINT = os.getenv("AMADEUS_GET_ENDPOINT")
        self._AMADEUS_POST_ENDPOINT = os.getenv("AMADEUS_POST_ENDPOINT")
        self._AMADEUS_IATA_ENDPOINT = os.getenv("AMADEUS_IATA_ENDPOINT")
        self._AMADEUS_KEY = os.getenv("AMADEUS_KEY")
        self._AMADEUS_SECRET = os.getenv("AMADEUS_SECRET")
        self._TOKEN = self.get_new_token()

    def get_new_token(self):
        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        body = {
            "grant_type": "client_credentials",
            "client_id": self._AMADEUS_KEY,
            "client_secret": self._AMADEUS_SECRET
        }
        response = requests.post(url = self._TOKEN_ENDPOINT, headers = header, data = body)
        
        return response.json()["access_token"]

    def encontrar_iata_code(self, city_name):
        headers = {
            "Authorization": f"Bearer {self._TOKEN}",
            "Content-Type": "application/json"
        }
        query = {
            "keyword": city_name,
            "max": 2,
            "include": "AIRPORTS"
        }
        response = requests.get(url=self._AMADEUS_IATA_ENDPOINT, headers = headers, params = query)
        try:
            code = response.json()["data"][0]["iataCode"]
        except KeyError:
            print(f"Nenhum aeroporto encontado na cidade {city_name}.")
        except IndexError:
            print(f"Nenhum aeroporto encontrado na cidade {city_name}.")
        
        return code
    
    def search_flights(self, origin_city_code, destination_city_code, data_ida, data_volta):
        headers = {
            "Authorization": f"Bearer {self._TOKEN}",
            "Content-Type": "application/json"
        }
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": data_ida.strftime("%Y-%m-%d"),
            "returnDate": data_volta.stftime("%Y-%m-%d"),
            "adults": 1,
            "currencyCode": "GBP",
            "nonStop": False
        }

        response = requests.get(url = self._AMADEUS_GET_ENDPOINT, headers = headers, params = query)

        if response.status_code != 200:
            print(f"Erro ao buscar voos: {response.status_code} - {response.text}")
            return None
        
        return response.json()