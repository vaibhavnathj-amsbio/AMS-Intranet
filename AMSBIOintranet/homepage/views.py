from django.shortcuts import render, redirect
import oauth2 as oauth
import requests
import json


# Create your views here.
def index(request):
    response = track_request()
    context = {'response': response[0], 'headers': response[1]}
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

    payload = json.dumps({"searchCriteria[filterGroups][0][filters][0][field]": "status",
                            "searchCriteria[filterGroups][0][filters][0][value]": "pending",
                            "searchCriteria[filterGroups][0][filters][0][conditionType]": "eq",
                        })

    response = requests.request("GET", url, headers=headers).text
    # with open('temp_files/magento_orders.json','w') as f:
    #     f.write(response)
    json_response = json.loads(response)
    headers = list((json_response['items'][10]).keys())[:58]
    data_list = []
    for ele in json_response['items']:
        data_dict = {}
        for key,val in ele.items():
            if key in ["items","billing_address","payment", "extension_attributes", "status_histories"]:
                pass
            else:
                data_dict[key] = val
        data_list.append(data_dict)
    return data_list[1:], headers
    
    
    