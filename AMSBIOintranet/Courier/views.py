import requests
import json

from django.shortcuts import render, redirect


# 'api_key': 'l76c7f058eed374645b8b860b19d778b07',
# 'password': 'be880a5f2a20429ebdb7c54afcc1acd3',
def oAuth():    
    token = 'grant_type=client_credentials&client_id=l76c7f058eed374645b8b860b19d778b07&client_secret=be880a5f2a20429ebdb7c54afcc1acd3'
    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
        }
    response_auth = requests.request("POST", "https://apis-sandbox.fedex.com/oauth/token", data=token, headers=headers).text
    json_response = json.loads(response_auth)
    return json_response


def track_request(track_id):
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
        'Authorization': "Bearer " + oAuth()['access_token'] 
        }

    response = requests.request("POST", url, data=payload, headers=tracking_headers).text
    # with open('tracking_info.json','w') as f:
    #     f.write(response)
    json_response = json.loads(response)
    return json_response


def index(request):
    return redirect('/')


def fedexUK(request):     
    if request.method == "POST":
        track_response = track_request(request.POST['track_num'])
        latest_status = track_response["output"]["completeTrackResults"][0]["trackResults"][0]["latestStatusDetail"]
        context = {'response' : latest_status}
        return render(request, 'fedex_UK.html', context)

    return render(request, 'fedex_UK.html',)


def fedexUSA(request):
    return render(request, 'fedex_USA.html')

