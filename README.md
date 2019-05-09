# database-project-spring2019
Database "Curriculum" Project Developer Manual- 2019

Authors: Jake Berns, Colin Burdine, Hunter Michalk

-----------------------------------------------------
# Developer's Manual
-----------------------------------------------------
# Software requirements: 

This application requires Python v3.6.5 or later to run as well as 
the following packages:
	
    pip 10.0.1
    Kivy v1.10.1
    Kivy-Garden v0.1.4
    certifi 2019.3.9
    chardet 3.0.4
    docutils 0.14
    idna 2.8
    kivy.deps.angle 0.1.7
    kivy.deps.glew 0.1.10
    kivy.deps.gstreamer 0.1.13
    kivy.deps.sdl2 0.1.18
    mysql-connector 2.2.9
    pypiwin32 223
    pywin32 224
    requests 2.21.0
    urllib3 1.24.1

Depending on the graphics capabilites of each system, additional
dependencies may need to be installed as indicated to run this project. 
For more information on the python libraries required to run kivy, see 
the kivy installation guide at:
<https://kivy.org/doc/stable/installation/installation.html>

 In addition, documentation and installation troubleshooting for the python mysql 
 connector can be found at:
<https://dev.mysql.com/doc/connector-python/en/connector-python-installation.html>

-----------------------------------------------------
In addition to the above software requirements,
it is required that you have a working MySQL server
that can be connected to. Credentials for login are
supplied directly to the application when it starts
-----------------------------------------------------

# Running the Application:

To run the application, be sure that you have installed all of
the packages listed above. This can be done by:

    pip --upgrade install <package_name>
    
Then, cd to the project folder with the launchapp.py script and 
run it from command line via:

    python launchapp.py

If any packages are not resolved or properly installed, the program 
should terminate with an error message indicating that the respective 
dependencies cannot be resolved.
    
