
class FlightData:

    def __init__(self, price, origin_airport, destination_airport, out_date, return_date):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date

def encontrar_voo_mais_barato(self, data):

    primeiro_voo = data["data"][0]
    preco_mais_baixo = float(primeiro_voo["price"]["grandTotal"])
    origem = primeiro_voo["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    destino = primeiro_voo["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
    data_ida = primeiro_voo["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    data_volta = primeiro_voo["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

    voo_mais_barato = FlightData(preco_mais_baixo, origem, destino, data_ida, data_volta)

    for flight in data["data"]:
        preco = float(flight["price"]["grandTotal"])
        if preco < preco_mais_baixo:
            preco_mais_baixo = preco
            origem = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            destino = flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
            data_ida = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            data_volta = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
            voo_mais_barato = FlightData(preco_mais_baixo, origem, destino, data_ida, data_volta)
        
    return voo_mais_barato
        
