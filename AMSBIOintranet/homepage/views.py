import requests
import json
import time

from django.shortcuts import render


# Create your views here.
def index(request):
    start = time.time()
    response = track_request(number_of_orders="50")
    end = time.time()
    print("Response time: ", end-start, "secs")
    context = {'response': response[0], 'col_headers': format_cols(response[1]), 'headers': response[1]}
    return render(request, 'index.html', context)


def oAuth_magento(api_key, api_pass): 

    payload = json.dumps({'username': api_key, 'password': api_pass})    
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    response_auth = requests.request("POST", "https://stage.amsbio.com/index.php/rest/V1/integration/admin/token", data=payload, headers=headers).text
    return json.loads(response_auth)


def track_request(number_of_orders):

    token = oAuth_magento("amsBioAPI", "dY0K9wAWxA4U5LjEea")

    url = "https://stage.amsbio.com/index.php/rest/V1/orders/"

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + token,
        'Accept': 'application/json',
        }

    payload = {"searchCriteria[filterGroups][0][filters][0][field]": "status",
                "searchCriteria[filterGroups][0][filters][0][value]": "pending",
                "searchCriteria[filterGroups][0][filters][0][conditionType]": "eq",
                "searchCriteria[pageSize]": number_of_orders,
                "searchCriteria[sortOrders][0][field]":"created_at",
                "fields": "items[increment_id,base_currency_code,base_grand_total,grand_total,store_name,created_at,customer_email,customer_firstname,customer_lastname,status]",
            }

    response = requests.request("GET", url, headers=headers, params=payload)
    # with open('temp_files/magento_orders.json','w') as f:
    #     f.write(response.text)
    json_response = json.loads(response.text)
    col_headers = list((json_response['items'][1]).keys())
    # data_list = []
    # for ele in json_response['items']:
    #     data_dict = {}
    #     for key,val in ele.items():
    #         if key in ["items","billing_address","payment", "extension_attributes", "status_histories"]:
    #             pass
    #         else:
    #             data_dict[key] = val
    #     data_list.append(data_dict)
    return json_response['items'][1:], col_headers
    
    
def format_cols(data):
    col_list = []
    for elem in data:
        new_str = ""
        for string in elem.split('_'):
            new_str += string.capitalize() + " "
        col_list.append(new_str[:-1])
    return col_list