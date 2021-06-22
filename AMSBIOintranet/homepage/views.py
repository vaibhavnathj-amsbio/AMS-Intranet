from django.http.response import JsonResponse
import requests
import json

from django.shortcuts import render
from django.contrib import messages

from API.call import oAuth_magento


# Create your views here.
def index(request):
    """ Main function for rendering the homepage! """
    if request.method == "POST" and 'from_date' in request.POST: # Controls the filter button
        params = {'from_date': request.POST['from_date'], 'to_date': request.POST['to_date'], 'number_of_orders': request.POST['number_of_orders'], 'status': request.POST['status']}
        response = track_request(params)
        context = {'response': response[0], 'col_headers': format_cols(response[1]), 'flag': True}
        return render(request, 'index.html', context)
    
    elif request.method == "POST" and 'order_id' in request.POST: # Controls the search button
        response = searchOrder(request.POST['order_id'])
        if 'flag' in response.keys():    
            return render(request, 'index.html', response)
        else:
            context = {'response': response['result'], 'col_headers': format_cols(response['col_headers']), 'flag': True }
            return render(request, 'index.html', context)

    elif request.method == "POST" and 'comment' in request.POST: # Contrlols the edit shipment feature
        order_id = request.POST['reference_id']
        comment = request.POST['comment']
        notify = "true" if 'notify' in request.POST else "false"
        appendComment = "true" if len(request.POST['comment']) > 0 else "false"
        editShipment(order_id=order_id, comment=comment, appendComment=appendComment, notify=notify) # Uncomment to enable shipment creation feature 
        messages.success(request, 'Shipment Created!') # display a message after shipment creation
        response = track_request(params = {})
        context = {'response': response[0], 'col_headers': format_cols(response[1]), 'flag':True}
        return render(request, 'index.html', context)

    else: # renders the default view
        response = track_request(params = {})
        context = {'response': response[0], 'col_headers': format_cols(response[1]), 'flag':True}
        return render(request, 'index.html', context)


def track_request(params):

    """
    Function for handling filter requests from the user

    params(dict):   'number_of_orders' : Number of orders to be fetched,
                    'from_date' : Select 'from'/start date,
                    'to_date' : Select 'to'/end date,
                    'status': Status of the order,

    """

    if len(params) == 0:
        number_of_orders = "20"
        field = None
        from_date = None
        condition_1 = None
        to_date = None
        condition_2 = None
        status = None
        value = None
        condition_3 = None
    else:
        number_of_orders = params['number_of_orders'] if len(params['number_of_orders']) != 0 else "20"
        field = "created_at"
        from_date = params['from_date'] + " 00:00:00" if len(params['from_date']) != 0 else "2000-01-01 00:00:00" 
        condition_1 = "gteq"
        to_date = params['to_date'] + " 23:59:59" if len(params['to_date']) != 0 else "2100-12-31 23:59:59"
        condition_2 = "lteq"
        status = None if params['status'] == "None" else "status"
        value = None if params['status'] == "None" else params['status']
        condition_3 = None if params['status'] == "None" else "eq"

    generate_request = oAuth_magento()

    payload = { "searchCriteria[filter_groups][0][filters][0][field]": field,
                "searchCriteria[filter_groups][0][filters][0][value]": from_date,
                "searchCriteria[filter_groups][0][filters][0][condition_type]": condition_1,

                "searchCriteria[filter_groups][1][filters][0][field]": field,
                "searchCriteria[filter_groups][1][filters][0][value]": to_date,
                "searchCriteria[filter_groups][1][filters][0][condition_type]": condition_2,

                "searchCriteria[filter_groups][2][filters][0][field]": status,
                "searchCriteria[filter_groups][2][filters][0][value]": value,
                "searchCriteria[filter_groups][2][filters][0][condition_type]": condition_3,
                
                "searchCriteria[pageSize]": number_of_orders,
                "searchCriteria[sortOrders][0][field]":"created_at",
                "fields": "items[increment_id,base_currency_code,grand_total,created_at,status,billing_address[company]]",
            }

    response = requests.request("GET", url=generate_request[0], headers=generate_request[1], params=payload)
    # with open('temp_files/magento_orders_test.json','w') as f:
    #     f.write(response.text)
    json_response = json.loads(response.text)
    for ele in json_response['items']:
        for key, val in ele.items():
            if key == 'billing_address':
                ele['purchasing_institute'] = ele.pop(key)['company']
            else:
                pass
    col_headers = list((json_response['items'][0]).keys())
    return json_response['items'], col_headers
    
    
def format_cols(data):
    """ Helper function for getting the col headers to desired state """
    col_list = []
    for elem in data:
        new_str = ""
        for string in elem.split('_'):
            new_str += string.capitalize() + " "
        col_list.append(new_str[:-1])
    return col_list


def searchOrder(order_id):
    """
    Function for controling search feature and request from the user

    params(dict):   'order_id': Increment - Id of Magento Order
    """
    flag = True
    generate_request = oAuth_magento()

    payload = {"searchCriteria[filter_groups][0][filters][0][field]": "increment_id",
                "searchCriteria[filter_groups][0][filters][0][value]": order_id,
                "searchCriteria[filter_groups][0][filters][0][conditionType]": "eq",
                "fields": "items[increment_id,base_currency_code,grand_total,created_at,status,billing_address[company]]",
            }

    try:
        response = requests.request("GET", url=generate_request[0], headers=generate_request[1], params=payload)
        # with open('temp_files/magento_search_orders.json','w') as f:
        #     f.write(response.text)
        json_response = json.loads(response.text)
        for ele in json_response['items']:
            for key, val in ele.items():
                if key == 'billing_address':
                    ele['purchasing_institute'] = ele.pop(key)['company']
                else:
                    pass
        col_headers = list((json_response['items'][0]).keys())
        context = {'result': json_response['items'], 'col_headers': col_headers}
        return context
    
    except:
        flag = False
        context = {'msg': "*Please enter a valid Order ID!", 'flag': flag}
        return context


def shipmentDetails(request):
    """ Function for fetching shipment details from Magento sales """
    order_id = request.GET.get('order_id')
    generate_request = oAuth_magento()

    payload = {"searchCriteria[filter_groups][0][filters][0][field]": "increment_id",
                "searchCriteria[filter_groups][0][filters][0][value]": order_id,
                "searchCriteria[filter_groups][0][filters][0][conditionType]": "eq",
                "fields": "items[status,base_currency_code,grand_total,items[name,sku],extension_attributes[shipping_assignments[shipping[address[city,company,country_id,firstname,lastname,postcode,region,telephone]]]]]",
            }
    response = requests.request("GET", url=generate_request[0], headers=generate_request[1], params=payload)
    # with open('temp_files/magento_get_order_select.json','w') as f:
    #     f.write(response.text)
    json_response = json.loads(response.text)
    context = {'result': json_response['items'][0]['extension_attributes']['shipping_assignments'][0]['shipping']['address'], 
                'status': json_response['items'][0]['status'],
                'item_name': json_response['items'][0]['items'],
                'price': json_response['items'][0]['base_currency_code'] + ' ' + str(json_response['items'][0]['grand_total']),
            }
    return JsonResponse(context)


def editShipment(order_id, comment, appendComment, notify):
    """ 
    Function for creating new shipments
    
    Params: order_id - Increment ID for Magento orders
            comment - if user wants to add a comment while creating the shipment
            appendComment - (bool) flag if user wants to add comment or not
            notify - (bool) flag if user wants to notify the customer by email or not 
    """
    generate_request = oAuth_magento()

    payload = {"searchCriteria[filter_groups][0][filters][0][field]": "increment_id",
                "searchCriteria[filter_groups][0][filters][0][value]": order_id,
                "searchCriteria[filter_groups][0][filters][0][condition_type]": "eq",
                "fields": "items[entity_id]"}

    response = requests.request("GET", url=generate_request[0], headers=generate_request[1], params=payload)
    json_response = json.loads(response.text)
    entity_id = json_response['items'][0]['entity_id']

    if appendComment == "true": 
        payload = {"appendComment": "true",
                    "notify": notify,
                    "comment": {
                        "extension_attributes": {},
                        "comment": comment,
                        "is_visible_on_front": 1
                    }
            }
    
    else:
        payload = {"notify": notify}

    shipment_response = requests.request("POST", url="https://www.amsbio.com/index.php/rest/V1/order/" + str(entity_id) + "/ship", headers=generate_request[1], data=json.dumps(payload))
    return json.loads(shipment_response.text)
