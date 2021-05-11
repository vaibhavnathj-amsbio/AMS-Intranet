import requests
import json
import time

from django.shortcuts import render


# Create your views here.
def index(request):
    if request.method == "POST":
        from_date = request.POST['from_date'] + " 00:00:00"
        to_date = request.POST['to_date'] + " 00:00:00"
        start = time.time()
        response = track_request(number_of_orders=None, field="created_at", to_date=to_date, condition_1="gteq", from_date=from_date, condition_2="lteq")
        end = time.time()
        print("Response time: ", end-start, "secs")
        context = {'response': response[0], 'col_headers': format_cols(response[1]), 'headers': response[1]}
        return render(request, 'index.html', context)
    else:
        start = time.time()
        response = track_request(number_of_orders="50", field=None, to_date=None, condition_1=None, from_date=None, condition_2=None)
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


def track_request(number_of_orders, field, to_date, condition_1, from_date, condition_2):

    token = oAuth_magento("amsBioAPI", "dY0K9wAWxA4U5LjEea")

    url = "https://stage.amsbio.com/index.php/rest/V1/orders/"

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + token,
        'Accept': 'application/json',
        }

    payload = {"searchCriteria[filter_groups][0][filters][0][field]": "status",
                "searchCriteria[filter_groups][0][filters][0][value]": "pending",
                "searchCriteria[filter_groups][0][filters][0][conditionType]": "eq",
                "searchCriteria[filter_groups][1][filters][0][field]": field,
                "searchCriteria[filter_groups][1][filters][0][value]": to_date,
                "searchCriteria[filter_groups][1][filters][0][condition_type]": condition_1,
                "searchCriteria[filter_groups][2][filters][0][field]": field,
                "searchCriteria[filter_groups][2][filters][0][value]": from_date,
                "searchCriteria[filter_groups][2][filters][0][condition_type]": condition_2,
                "searchCriteria[pageSize]": number_of_orders,
                "searchCriteria[sortOrders][0][field]":"created_at",
                "fields": "items[increment_id,base_currency_code,base_grand_total,grand_total,store_name,created_at,customer_email,customer_firstname,customer_lastname,status]",
            }

    response = requests.request("GET", url, headers=headers, params=payload)
    # with open('temp_files/magento_orders_test.json','w') as f:
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
    return json_response['items'], col_headers
    
    
def format_cols(data):
    col_list = []
    for elem in data:
        new_str = ""
        for string in elem.split('_'):
            new_str += string.capitalize() + " "
        col_list.append(new_str[:-1])
    return col_list