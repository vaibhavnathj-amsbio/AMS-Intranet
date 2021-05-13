import requests
import json
import time

from django.shortcuts import render


# Create your views here.
def index(request):
    if request.method == "POST":

        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        number_of_orders = request.POST['number_of_orders']

        start = time.time()
        params = {'from_date': from_date, 'to_date': to_date, 'number_of_orders': number_of_orders}
        response = track_request(params)
        end = time.time()

        print("Response time: ", end-start, "secs")
        context = {'response': response[0], 'col_headers': format_cols(response[1]), 'headers': response[1]}
        return render(request, 'index.html', context)

    else:

        start = time.time()
        response = track_request(params = {})
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

    response_auth = requests.request("POST", "https://www.amsbio.com/index.php/rest/V1/integration/admin/token", data=payload, headers=headers).text
    return json.loads(response_auth)


def track_request(params):

    """
    params(dict):   'number_of_orders' : Number of orders to be fetched
                    'field' : On which field the filter must be applied to, default "created_at"
                    'from_date' : Select 'from'/start date
                    'condition_1' : Select logical condition to be applied on 'from' date, default 'lteq'
                    'to_date' : Select 'to'/end date
                    'condition_2' : Select logical condition to be applied on 'to' date, default 'gteq'

    """

    if len(params) == 0:
        number_of_orders = "50"
        field = None
        from_date = None
        condition_1 = None
        to_date = None
        condition_2 = None
    else:
        number_of_orders = params['number_of_orders'] if len(params['number_of_orders']) != 0 else "50"
        field = params['field'] if 'field' in params.keys() else "created_at"
        from_date = params['from_date'] + " 00:00:00" if len(params['from_date']) != 0 else "2100-12-31 00:00:00" 
        condition_1 = params['condition_1'] if 'condition_1' in params.keys() else "lteq"
        to_date = params['to_date'] + " 00:00:00" if len(params['to_date']) != 0 else "2000-01-01 00:00:00"
        condition_2 = params['condition_2'] if 'condition_2' in params.keys() else "gteq"

    token = oAuth_magento("amsBioAPI", "Tg5fTysjobQFlDvYUf7")

    url = "https://www.amsbio.com/index.php/rest/V1/orders/"

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + token,
        'Accept': 'application/json',
        }

    payload = {"searchCriteria[filter_groups][0][filters][0][field]": "status",
                "searchCriteria[filter_groups][0][filters][0][value]": "pending",
                "searchCriteria[filter_groups][0][filters][0][conditionType]": "eq",
                "searchCriteria[filter_groups][1][filters][0][field]": field,
                "searchCriteria[filter_groups][1][filters][0][value]": from_date,
                "searchCriteria[filter_groups][1][filters][0][condition_type]": condition_1,
                "searchCriteria[filter_groups][2][filters][0][field]": field,
                "searchCriteria[filter_groups][2][filters][0][value]": to_date,
                "searchCriteria[filter_groups][2][filters][0][condition_type]": condition_2,
                "searchCriteria[pageSize]": number_of_orders,
                "searchCriteria[sortOrders][0][field]":"created_at",
                "fields": "items[increment_id,base_currency_code,grand_total,created_at,customer_firstname,status]",
            }

    response = requests.request("GET", url, headers=headers, params=payload)
    # with open('temp_files/magento_orders_test.json','w') as f:
    #     f.write(response.text)
    json_response = json.loads(response.text)
    col_headers = list((json_response['items'][0]).keys())

    return json_response['items'], col_headers
    
    
def format_cols(data):
    col_list = []
    for elem in data:
        new_str = ""
        for string in elem.split('_'):
            new_str += string.capitalize() + " "
        col_list.append(new_str[:-1])
    return col_list