import pandas as pd
from django.http import JsonResponse

from django.shortcuts import render, redirect

from API.call import track_request_dhl, track_request_fedex


def index(request):
    return redirect('/')


def scanEvents_fedex(data1):
    """ Helper function for formatting the API response from FedEx """
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
    """ Main function for rendering the FedEx UK/USA pages """
    flag = True
    page = list(request.path.split("/"))[2] + '.html'
    try:
        if request.method == "POST":
            track_response = track_request_fedex(request.POST['track_num'])
            latest_status = track_response["output"]["completeTrackResults"][0]["trackResults"][0]["latestStatusDetail"]
            if "receivedByName" in track_response["output"]["completeTrackResults"][0]["trackResults"][0]["deliveryDetails"].keys():
                latest_status['Signed for by'] = track_response["output"]["completeTrackResults"][0]["trackResults"][0]["deliveryDetails"]["receivedByName"]
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


def scanEvents_DHL(data):
    """ Helper function for formatting the API response from DHL """
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
    """ Main function for rendering the FedEx UK/USA pages """
    flag = True
    try:
        if request.method == "POST":
            tracking_number = request.POST['track_num']
            track_response = track_request_dhl(tracking_number)
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


def loadCSVtoHTML(request):
    """ Function for handling the Ajax call made to load the FedEx shipment tables  """
    page = list(request.path.split("_"))[1] + '.csv'
    data = pd.read_csv('helper_files/'+ page, header=0, index_col=0)
    data.drop(columns=data.columns[-1],  axis=1, inplace=True)
    data.index.name = None
    data_inb = data.drop(data[data['Direction '] == 'Outbo'].index)
    data_outb = data.drop(data[data['Direction '] == 'Inbou'].index)
    data_inb.drop(columns=['Direction '], axis=1, inplace=True)
    data_outb.drop(columns=['Direction '], axis=1, inplace=True)
    parse_string_inb = data_inb.to_html(classes="table table-striped roundedTable", table_id="Ordertable1", border=0)
    parse_string_outb = data_outb.to_html(classes="table table-striped roundedTable", table_id="Ordertable2", border=0)
    return JsonResponse({'table_in':parse_string_inb, 'table_out': parse_string_outb})