import requests
import json

from django.shortcuts import render, redirect


def index(request):
    return redirect('/')


FedEx = {'api_key': 'l76c7f058eed374645b8b860b19d778b07', 'api_pass': 'be880a5f2a20429ebdb7c54afcc1acd3'}
def oAuth(api_key, api_pass):    
    token = 'grant_type=client_credentials&client_id=' + api_key + '&client_secret=' + api_pass 
    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
        }
    response_auth = requests.request("POST", "https://apis-sandbox.fedex.com/oauth/token", data=token, headers=headers).text
    json_response = json.loads(response_auth)
    return json_response


def track_request(track_id, api_key, api_pass):
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
        'Authorization': "Bearer " + oAuth(api_key, api_pass)['access_token'] 
        }

    response = requests.request("POST", url, data=payload, headers=tracking_headers).text
    # with open('temp_files/tracking_info_new_ship.json','w') as f:
    #     f.write(response)
    json_response = json.loads(response)
    return json_response

def scanEvents(data1, data2):
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
          

def fedex(request):
    flag = True
    
    try:
        if request.method == "POST":
            track_response = track_request(request.POST['track_num'], FedEx['api_key'], FedEx['api_pass'])
            latest_status = track_response["output"]["completeTrackResults"][0]["trackResults"][0]["latestStatusDetail"]
            location = latest_status['scanLocation']
            latest_status.pop('scanLocation')
            weight = track_response["output"]["completeTrackResults"][0]["trackResults"][0]["packageDetails"]["weightAndDimensions"]["weight"][0]
            shipper_ref = track_response["output"]["completeTrackResults"][0]["trackResults"][0]["additionalTrackingInfo"]["packageIdentifiers"][0]["values"][0]
            scan_events = track_response["output"]["completeTrackResults"][0]["trackResults"][0]["scanEvents"]
            scan_events = scan_events[:-1]
            history = scanEvents(scan_events, location)
            context = {'status' : latest_status, 'location': location, 'weight': weight, 'flag': flag, 'track_num':request.POST['track_num'], 'ref': shipper_ref, 'history': history}
            return render(request, 'fedex.html', context)

    except:
        flag = False
        context = {'msg' : '*Please enter valid tracking number', 'flag': flag}
        return render(request, 'fedex.html', context)

    return render(request, 'fedex.html',)


def dhl(request):
    return render(request, 'dhl.html', {'msg': 'Coming Soon!'})