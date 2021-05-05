import requests
import json
import pandas as pd
from django.http import JsonResponse

from django.shortcuts import render, redirect


FedEx = {'api_key': 'l76c7f058eed374645b8b860b19d778b07', 'api_pass': 'be880a5f2a20429ebdb7c54afcc1acd3'}
DHL = {'api_key': '8C9yOAvIXeYK6xGhTLx8SmsSPISMFy5V', 'api_pass': 'UX1WCKfQaa98xSNl'}


def index(request):
    return redirect('/')


def oAuth_fedex(api_key, api_pass):    
    token = 'grant_type=client_credentials&client_id=' + api_key + '&client_secret=' + api_pass 
    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
        }
    response_auth = requests.request("POST", "https://apis-sandbox.fedex.com/oauth/token", data=token, headers=headers).text
    json_response = json.loads(response_auth)
    return json_response


def track_request_fedex(track_id, api_key, api_pass):
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
        'Authorization': "Bearer " + oAuth_fedex(api_key, api_pass)['access_token'] 
        }

    response = requests.request("POST", url, data=payload, headers=tracking_headers).text
    # with open('temp_files/tracking_info_new_ship.json','w') as f:
    #     f.write(response)
    json_response = json.loads(response)
    return json_response


def scanEvents_fedex(data1):
    data_list = []
    for ele in data1:
        data_dict = {}
        for key, val in ele.items():
            if key in ["date", "derivedStatus", "eventDescription"]:
                data_dict[key.upper()] = val
            elif key == "scanLocation":
                data_dict["CITY"] = val["city"]
                data_dict["COUNTRY"] = val["countryName"]
            else:
                pass
        data_list.append(data_dict)
    return data_list


def loadCSVtoHTML(request):
    page = list(request.path.split("_"))[1] + '.csv'
    data = pd.read_csv('temp_files/'+ page, header=0, index_col=0)
    data.drop(columns=data.columns[-1],  axis=1, inplace=True)
    data.index.name = None
    parse_string = data.to_html(classes="table table-bordered rounded table-hover", table_id="Ordertable")
    return JsonResponse({'table':parse_string})


def fedex(request):
    flag = True
    page = list(request.path.split("/"))[2] + '.html'
    try:
        if request.method == "POST":
            track_response = track_request_fedex(request.POST['track_num'], FedEx['api_key'], FedEx['api_pass'])
            latest_status = track_response["output"]["completeTrackResults"][0]["trackResults"][0]["latestStatusDetail"]
            location = latest_status['scanLocation']
            latest_status.pop('scanLocation')
            weight = track_response["output"]["completeTrackResults"][0]["trackResults"][0]["packageDetails"]["weightAndDimensions"]["weight"][0]
            shipper_ref = track_response["output"]["completeTrackResults"][0]["trackResults"][0]["additionalTrackingInfo"]["packageIdentifiers"][0]["values"][0]
            scan_events = track_response["output"]["completeTrackResults"][0]["trackResults"][0]["scanEvents"]
            scan_events = scan_events[:-1]
            history = scanEvents_fedex(scan_events)
            context = {'status' : latest_status, 'location': location, 'weight': weight, 'flag': flag, 'track_num':request.POST['track_num'], 'ref': shipper_ref, 'history': history}
            return render(request, page, context)

    except:
        flag = False
        context = {'msg' : '*Please enter valid tracking number', 'flag': flag}
        return render(request, page, context)

    return render(request, page)


def track_request_dhl(api_key, track_num):
    url = "https://api-eu.dhl.com/track/shipments"
    headers = {"DHL-API-Key": api_key}

    querystring = {"trackingNumber":  track_num}

    response = requests.request("GET", url, headers=headers, params=querystring).text
    # with open('temp_files/tracking_info_dhl.json','w') as f:
    #     f.write(response)
    json_response = json.loads(response)
    return json_response


def scanEvents_DHL(data):
    data_list = []
    for ele in data:
        data_dict = {}
        for key, val in ele.items():
            if key in ["timestamp", "description"]:
                data_dict[key.upper()] = val
            elif key == "location":
                data_dict["LOCATION"] = val["address"]["addressLocality"]
            else:
                pass
        data_list.append(data_dict)
    return data_list


def dhl(request):
    flag = True
    try:
        if request.method == "POST":
            tracking_number = request.POST['track_num']
            track_response = track_request_dhl(DHL['api_key'], tracking_number)
            status = track_response["shipments"][0]["status"]
            location = status["location"]["address"]
            status.pop("location")
            events = track_response["shipments"][0]["events"]
            history = scanEvents_DHL(events)
            context = {'status': status, 'flag': flag, 'track_num': tracking_number, "location": location, 'history': history}
            return render(request, 'dhl.html', context)
    
    except:
        flag = False
        context = {'msg': '*Please enter valid tracking number', 'flag': flag}
        return render(request, 'dhl.html', context)
    
    return render(request, 'dhl.html')