import requests

# Global dictionary to store Live Currency Exchange Rate
live_rate_dict = { "USD": {"USD": 1, "JPY": 0, "GBP": 0, "EUR": 0, "CHF": 0},
                    "JPY": {"USD": 0, "JPY": 1, "GBP": 0, "EUR": 0, "CHF": 0},
                    "GBP": {"USD": 0, "JPY": 0, "GBP": 1, "EUR": 0, "CHF": 0},
                    "EUR": {"USD": 0, "JPY": 0, "GBP": 0, "EUR": 1, "CHF": 0},
                    "CHF": {"USD": 0, "JPY": 0, "GBP": 0, "EUR": 0, "CHF": 1}}


def getCurrencyRate():
    global live_rate_dict
    url = "https://currency-exchange.p.rapidapi.com/exchange"
    headers = {
        'x-rapidapi-key': "9b7191561emshf73238a9c9be76cp1eb370jsnc687d527eeee",
        'x-rapidapi-host': "currency-exchange.p.rapidapi.com"
        }
    for key, value in live_rate_dict.items():
        for inner_key, inner_value in value.items():
            querystring = {"from": key , "to": inner_key}
            response = requests.request("GET", url, headers=headers, params=querystring)
            live_rate_dict[key][inner_key] = round(float(response.text),3)
    return live_rate_dict