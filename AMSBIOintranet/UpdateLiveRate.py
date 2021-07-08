import sqlite3
import requests
import json


# Loading credentials from credentials.json
f = open('API/credentials.json') 
API_credentials = json.load(f)

connection = sqlite3.connect("db.sqlite3")
cursor = connection.cursor()

live_rate_dict = { "USD": {"USD": 1, "JPY": 0, "GBP": 0, "EUR": 0, "CHF": 0},
                    "JPY": {"USD": 0, "JPY": 1, "GBP": 0, "EUR": 0, "CHF": 0},
                    "GBP": {"USD": 0, "JPY": 0, "GBP": 1, "EUR": 0, "CHF": 0},
                    "EUR": {"USD": 0, "JPY": 0, "GBP": 0, "EUR": 1, "CHF": 0},
                    "CHF": {"USD": 0, "JPY": 0, "GBP": 0, "EUR": 0, "CHF": 1}}

def fetchLiveRates(url,headers,template):
    # counter = 1
    for key, value in template.items():
            for inner_key, inner_value in value.items():
                if key == inner_key:
                    pass
                else:
                    querystring = {"from": key , "to": inner_key}
                    response = requests.request("GET", url, headers=headers, params=querystring)
                    rate = round(float(response.text),3)
                    # target_values = (counter, key, inner_key, rate)
                    cursor.execute("UPDATE homepage_livecurrencyrate SET live_rate = ? WHERE base_currency = ? and to_currency = ?", (rate,key,inner_key))
                    connection.commit()
                    # counter += 1

try:
    fetchLiveRates(url = "https://currency-exchange.p.rapidapi.com/exchange", headers= API_credentials["RapidAPI"], template=live_rate_dict)
    print("Successfully updated currency live rates!")
except Exception as e:
    print("Error occurred ", e)