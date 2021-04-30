from django.shortcuts import render, redirect
import oauth2 as oauth
import requests


# Create your views here.
def index(request):
    if request.method == "POST":
        return redirect(request, 'index.html')
    else:
        return render(request, 'index.html')

consumer_key = '4nudd11rnxipa8mhzmqydc2dpz5rnvop'
consumer_secret = 'zbwy1j2m6p6d1gfly78o01o8rur99igj'
access_token = 'nxztkazoekstc80zv8pkx82iu4ai678s'
secret = 'y16al5mphh9scxi8ua7enz2280hcb13j'


def track_request():
    url = "https://www.amsbio.com/rest/default/V1/integration/sales/token"

    tracking_headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer nxztkazoekstc80zv8pkx82iu4ai678s"
        }
    response = requests.request("POST", url, headers=tracking_headers).text
    # with open('temp_files/tracking_info_new_ship.json','w') as f:
    #     f.write(response)
    json_response = json.loads(response)
    return json_response
    
    