## Running Local development Server

1.	Go to the path where project is saved, there should be a file named “manage.py”. The path in this case is: <code>G:\Vaibhav\new_intranet\AMS-Intranet\AMSBIOintranet</code>.
2.	Here, open command prompt by typing “cmd” in the address bar.
3.	In the command prompt, enter: <code>C:\ProgramData\Anaconda3\Scripts\activate test_env</code> to activate the python environment.
4.	Once activated enter the command, <code>python manage.py runserver</code> to run the tests.
5.	The local server will start and could be visited at https://127.0.0.1:8000.
6.  On closing the command prompt the server will stop.

*Note: Open the available run_DevServer.bat file to start the server*

## Testing Procedures

1.	Go to the path where project is saved, there should be a folder named “functional_tests”. The path in this case is: <code>G:\Vaibhav\new_intranet\AMS-Intranet\AMSBIOintranet</code>.
2.	Here, open command prompt by typing “cmd” in the address bar.
3.	In the command prompt, enter: <code>C:\ProgramData\Anaconda3\Scripts\activate intranetenv</code> to activate the python environment.
4.	Once activated enter the command, <code>python manage.py test -n functional_tests</code> to run the tests.
5.	The testing should take about 30-35 seconds to finish.

## Required Libraries

_requirements.txt_ contains all the essential libraries required in order to run the intranet.

## FedExSelenium.py

Python script for automatically downloading the FedEx shipment records for both UK and USA accounts.

## Deployment on IIS

1.  Install Python(ver=3.7.5) for all users on Windows
2.  Create a virtual environment for Django web application, activate it, and install all requirements mentioned in _requirements.txt_ using <code>pip install -r requirements.txt</code>.
3.  Install _wfastcgi_ library as well, <code>pip install  _wfastcgi_</code>
4.  Install *IIS* on Windows

##### Setting up FastCGI 

5.  Add a new application under the actions pane after opening the FastCGI Settings.
6.  Under *Full Path:* enter the location of Python interpreter when a virtual environment for the Project is created
7.  In the argument box, add the  *wfastcgi.py* file from the virtual environment

##### Adding New Member in Environment Variables

8.   *Name*: <code>DJANGO_SETTINGS_MODULE</code>
9.  *Value*: <code>AMSBIOintranet.settings</code>

10. *Name*: <code>WSGI_HANDLER</code>
11. *Value*: <code>AMSBIOintranet.wsgi.application</code>

10. *Name*: <code>PYTHONPATH</code>
11. *Value*: <code>"filepath of directory where manage.py resides"</code>

##### Django Web Application settings

12. Open IIS Manager and add a Website
13. For Physical Path, enter the location of the directory where manage.py resides
14. Change the port to 81

##### Handler Mappings

15. Open your Website in IIS Manager.
16. Add new Module mapping after navigating to Handler mapping
17. After that Type * in Request Path
18. Then Select FastCgiModule in Module Textbox.
19. And In “Executable(Optional)” section write the following with a pipe separator, <code>"filepath to virtual environment's python interpreter"| "filepath_to_\wfastcgi.py"</code>
20. Finally In the “Name” Section write anything.
21. Click the “Request Restrictions” button and uncheck the “Invoke handler only if request is mapped to” checkbox

##### Updating settings.py file

22. Open <code>settings.py</code>
23. Enter the hostname in the <code>ALLOWED_HOSTS</code> list like this, <code>ALLOWED_HOSTS = ['localhost', 'server_ip']</code>

##### Adding Static files

24. Right click the web site and choose Add Virtual Directory
25. Configure the following settings:
  Alias - This will be the name specified for STATICURL in your project’s settings file.
  Physical Path - This will be name specified for STATICROOT in your project’s setting file.
  Click ok to close the Add Virtual Directory dialog box
26. Select the newly created virtual directory
27. Open Handler Mappings
28. Click View Ordered List (located in actions pane on the right side)
29. Select StaticFile and click Move Up until the entry is at the top of the list.
30. Click Yes on the Handler Mappings warning dialog box informing you that changing made at the parent level will no longer be inherited at this level.

#### Find your website at <code>http://localhost:81</code>
