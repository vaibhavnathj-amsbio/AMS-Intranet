import requests
import json


# Loading credentials from credentials.json
f = open('API/credentials.json') 
API_credentials = json.load(f) 


#/**************** Exchange Rate Section on Currency Values | Call made at myDatabase/models ********************/#

# Global dictionary to store Live Currency Exchange Rate
live_rate_dict = { "USD": {"USD": 1, "JPY": 0, "GBP": 0, "EUR": 0, "CHF": 0},
                    "JPY": {"USD": 0, "JPY": 1, "GBP": 0, "EUR": 0, "CHF": 0},
                    "GBP": {"USD": 0, "JPY": 0, "GBP": 1, "EUR": 0, "CHF": 0},
                    "EUR": {"USD": 0, "JPY": 0, "GBP": 0, "EUR": 1, "CHF": 0},
                    "CHF": {"USD": 0, "JPY": 0, "GBP": 0, "EUR": 0, "CHF": 1}}

def getCurrencyRate():
    """ Function to fetch exchange rates from API"""
    global live_rate_dict
    url = "https://currency-exchange.p.rapidapi.com/exchange"
    headers = API_credentials["RapidAPI"]
    for key, value in live_rate_dict.items():
        for inner_key, inner_value in value.items():
            if key == inner_key:
                pass
            else:
                querystring = {"from": key , "to": inner_key}
                response = requests.request("GET", url, headers=headers, params=querystring)
                live_rate_dict[key][inner_key] = round(float(response.text),3)
    return live_rate_dict

# getCurrencyRate() # Function call to fetch the rates

#/*********************** Section Ends ****************************************/#




#/**************** Magento Section on Homepage | Call made at homepage/views ********************/#

def oAuth_magento(api_credentials= API_credentials["magento_credentials_production"]): 
    """ Helper function for authenticating every API call made to Magento! """
    payload = json.dumps(api_credentials)    
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    response_auth = requests.request("POST", "https://www.amsbio.com/index.php/rest/V1/integration/admin/token", data=payload, headers=headers).text

    api_url = "https://www.amsbio.com/index.php/rest/V1/orders/"
    api_headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + json.loads(response_auth),
        'Accept': 'application/json',
        }
    return  api_url, api_headers

#/*********************** Section Ends ****************************************/#




#/**************** Courier Section for FedEx, DHL | Call made at Courier/views *******************/#

def oAuth_fedex(api_key= API_credentials["FedEx"]["api_key"], api_pass= API_credentials["FedEx"]["api_pass"]):
    """ 
    Function for authenticating API call to FedEx

    params: api_key - API key as provided by FedEx
            api_pass - API Password as provided by FedEx
    """
    token = 'grant_type=client_credentials&client_id=' + api_key + '&client_secret=' + api_pass 
    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
        }
    response_auth = requests.request("POST", "https://apis-sandbox.fedex.com/oauth/token", data=token, headers=headers).text
    json_response = json.loads(response_auth)
    return json_response


def track_request_fedex(track_id):
    """ 
    Function for handling API request from FedEX
    
    Params: track_id - Tracking ID of the parcel
            api_key - API KEY
            api_pass - API PASSWORD
    """
    url = "https://apis-sandbox.fedex.com/track/v1/trackingnumbers"

    payload = json.dumps({"trackingInfo": [
                    {
                    "trackingNumberInfo": {
                        "trackingNumber": track_id
                    }
                    }
                ],
                "includeDetailedScans": True
                })

    tracking_headers = {
        'Content-Type': "application/json",
        'X-locale': "en_US",
        'Authorization': "Bearer " + oAuth_fedex()['access_token'] 
        }

    response = requests.request("POST", url, data=payload, headers=tracking_headers).text
    # with open('helper_files/tracking_info_new_ship.json','w') as f:
    #     f.write(response)
    json_response = json.loads(response)
    return json_response


def track_request_dhl(track_num, api_key= API_credentials["DHL"]["api_key"]):
    """ 
    Function for handling API request from DHL
    
    Params: api_key - API KEY
            track_num - Tracking number of the parcel
                       
    """

    url = "https://api-eu.dhl.com/track/shipments"
    headers = {"DHL-API-Key": api_key}

    querystring = {"trackingNumber":  track_num}

    response = requests.request("GET", url, headers=headers, params=querystring).text
    # with open('temp_files/tracking_info_dhl.json','w') as f:
    #     f.write(response)
    json_response = json.loads(response)
    return json_response

#/*********************** Section Ends ****************************************/#