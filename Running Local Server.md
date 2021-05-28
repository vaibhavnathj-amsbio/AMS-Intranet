After installing Python at <code>C:\Program Files\Python37</code>


###### Setting up the environment

1.  Open CMD where you want to execute the code by typing CMD in address bar
2.  Then type in <code>C:\Program Files\Python37\python</code> and hit enter. Python Interpreter should open at that location
3.  Enter the following <code>pip install virtualenv</code>, This will install necessary files for creating a virtual enivronment
4.  After this, Enter <code>virtualenv test_env</code>, this will create a virtual env called 'test_env'
5.  Type in <code>test_env\bin\activate</code>, If you see '(test_env)' infront of the CMD command line that means the virtual env is activated.

###### Installing required libraries

1.  Once the virtual env. is up and running, type in <code>pip install -r requirements.txt</code> The *requirements.txt* file should be present in the same directory
2.  Previous step will install all the dependencies.

###### Running the server

1.  Make sure the virtual env. is up and running then type in <code>python manage.py runserver</code>. This wil start the development server.
2.  Server can be visited at <code>http://127.0.0.1:8000</code>