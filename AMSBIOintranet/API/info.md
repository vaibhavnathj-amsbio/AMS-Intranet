## Info on all API services used through out the Project

Credentials for every API is maintained in "credentials.json" . The aforementioned json file is then loaded in _call.py_ in order to make the API calls

### Magento

There are two sets of IDs. One for _Stage_ website and another for th _Production_ website. Keys are as provided by Erik mork-barrett.

### FedEx

FedEX API is managed from [FedEx developer portal](https://developer.fedex.com/api/en-us/home.html).<br>
Same set of ID is used for both FedEx UK and USA account.<br>
Normal FedEx login will get the user inside FedEx developer portal.<br>
There is no need to put Project in production. Also, at the time of making this document the production feature for FedEx was not available.

### DHL

DHL API is managed from [DHL API Developer Portal](https://developer.dhl.com/).<br>
The following are the credentials for logging in to the portal.<br>
Username: _vjha_ and Password: _Amsbio2021_
DHL are providing a limit of 250 requests/day. This limit seems to be enough but option for an upgrade is available.

### RapidAPI

Currency Exchange Rates are managed from [Rapid API](https://rapidapi.com/developer/apps). <br>
The following are the credentials for logging in to the portal. <br>
Email: _vaibhavnathj@amsbio.com_ and Password: _Amsbio@2021_<br><br>
_Note: If the Currencies are not being populated on Currency value page then most likely the API key ("x-rapidapi-key") needs to be updated in the credentials.json. This can be done from the Rapid API, [Developer Portal](https://rapidapi.com/developer/apps) . After navigating to My Apps/Live-Rate-API/Security. Replace the new key with the old one ("x-rapidapi-key") in credentials.json_