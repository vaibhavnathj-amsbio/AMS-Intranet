from django.shortcuts import render, redirect
import oauth2 as oauth
import requests


# Create your views here.
def index(request):
    if request.method == "POST":
        return redirect(request, 'index.html')
    else:
        return render(request, 'index.html')


def oAuth_magento(api_key, api_pass): 

    payload = {'username': api_key, 'password': api_pass}    
    
    headers = {
        'Content-Type': 'multipart/form-data',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=umef23v1foqhsmnb45ov1dbgme',
     }

    response_auth = requests.request("POST", "https://stage.amsbio.com/index.php/rest/V1/integration/admin/token", data=payload, headers=headers).text
    return response_auth


def track_request():

    token = oAuth_magento("amsBioAPI", "dY0K9wAWxA4U5LjEea")

    url = "https://stage.amsbio.com/index.php/rest/V1/orders/?searchCriteria[filterGroups][0][filters][0][field]=status&searchCriteria[filterGroups][0][filters][0][value]=pending&searchCriteria[filterGroups][0][filters][0][conditionType]=eq"

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + token,
        }
    response = requests.request("POST", url, headers=headers).text
    # with open('temp_files/tracking_info_new_ship.json','w') as f:
    #     f.write(response)
    json_response = json.loads(response)
    return json_response
    
    