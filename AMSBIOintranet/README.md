# AMSBIOintranet

1. <strong>AMSBIOIntranet</strong>: Contains main settings files for Django. To setup server, apps and manage deployment
2. <strong>Courier</strong>: Application to handle pages related to courier services
3. <strong>assets</strong>: Contains javascript and css styling sheets for properly rendering the intranet
4. <strong>functiona_tests</strong>: Separate test files for testing every individual page on the intranet
5. <strong>homepage</strong>: Application to render the homepage(index.html) of the intranet
6. <strong>myDatabase</strong>: Application for rendering pages related to Database queries
7. <strong>static</strong>: Exact copy of <i>assets</i> folder, The <i>assets</i> folder fetches all the data from here.
8. <strong>templates</strong>: Directory containing all the html file responsible for front-end
9. <strong>Testing_Procedure.txt</strong>: Guide to run the included functional tests
10. <strong>manage.py</strong>: Main file for interacting with django thru terminal, MUST NOT BE DELETED

Any <strong>app</strong> directory:
1. __init.py__ : file for informing the python interpreter an app is here
2. admin.py: file for controlling the admin panel in django-admin view
3. apps.py: file for maintaing the particular app
4. forms.py<i>(optional)</i>: file for generating forms for considered model
5. models.py: file for creating and updating database tables as models for django
6. tables.py<i>(optional)</i>: for generating tables for a particular model
7. urls.py: for controlling the URL for the considered APP
8. views.py: for rendering html templates for the particular app

## Required Libraries

_requirements.txt_ contains all the essential libraries required in order to run the intranet.

## FedExSelenium.py

Python script for automatically downloading the FedEx shipment records for both UK and USA accounts.