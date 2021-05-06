from django.shortcuts import render, redirect
import oauth2 as oauth
import requests
import json


# Create your views here.
def index(request):
    response = track_request()
    context = {'response': response}
    if request.method == "POST":
        return redirect(request, 'index.html', context)
    else:
        return render(request, 'index.html', context)


def oAuth_magento(api_key, api_pass): 

    payload = json.dumps({'username': api_key, 'password': api_pass})    
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    response_auth = requests.request("POST", "https://stage.amsbio.com/index.php/rest/V1/integration/admin/token", data=payload, headers=headers).text
    return json.loads(response_auth)
    


def track_request():

    token = oAuth_magento("amsBioAPI", "dY0K9wAWxA4U5LjEea")

    url = "https://stage.amsbio.com/index.php/rest/V1/orders/?searchCriteria[filterGroups][0][filters][0][field]=status&searchCriteria[filterGroups][0][filters][0][value]=pending&searchCriteria[filterGroups][0][filters][0][conditionType]=eq"

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + token,
        'Accept': 'application/json',
        }

    # payload = json.dumps({"searchCriteria[filterGroups][0][filters][0][field]": "status",
    #                         "searchCriteria[filterGroups][0][filters][0][value]": "pending",
    #                         "searchCriteria[filterGroups][0][filters][0][conditionType]": "eq",
    #                     })

    response = requests.request("GET", url, headers=headers).text
    # with open('temp_files/magento_orders.json','w') as f:
    #     f.write(response)
    return json.loads(response)
    
    
    