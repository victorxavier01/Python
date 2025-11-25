import requests
import os
from pprint import pprint
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager


#Carregando variável de ambiente
dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

#AEROPORTO DE ORIGEM
ORIGIN_CITY_IATA = "MCZ"

#Objetos
sheet = DataManager()
flight_search = FlightSearch()
flight_data = FlightData()
notification_manager = NotificationManager()

#Obtendo dados da planilha
sheet_data = sheet.get_data()

#Verificando código IATA de cada cidade
for cidade in sheet_data["prices"]:
    
    #Buscando código IATA
    if cidade["iataCode"] == "":
        cidade["iataCode"] = flight_search.encontrar_iata_code(city_name = cidade["city"])

        #Atualizando o código IATA na planilha
        sheet.update_data(cidade)

# ==================== Procurando voos ====================

amanha = datetime.now() + timedelta(days = 1)
seis_meses_depois = datetime.now() + timedelta(days = (6 * 30))


for destino in sheet_data:
    voos = flight_search.search_flights(origin_city_code = ORIGIN_CITY_IATA, destination_city_code = destino["iataCode"], data_ida = amanha, data_volta = seis_meses_depois)

    voo_mais_barato = flight_data.encontrar_voo_mais_barato(voos)

    if voo_mais_barato.price < destino["lowestPrice"]:
        print(f"Voo encontrado: {voo_mais_barato.price} de {voo_mais_barato.origin_airport} para {voo_mais_barato.destination_airport} de {voo_mais_barato.out_date} a {voo_mais_barato.return_date}")

        #Enviando notificação
        notification_manager.enviar_mensagem(
            message_body=f"Alerta de preço baixo! Apenas£{voo_mais_barato.price}! "
                         f"de {voo_mais_barato.origin_airport} para {voo_mais_barato.destination_airport}, "
                         f"no dia {voo_mais_barato.out_date} até {voo_mais_barato.return_date}."
        )