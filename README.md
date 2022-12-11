# Cmpe133-Project
Webapp designed for users to easily manage their receipts and see all bank transactions at same place.
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [VENV Setup](#using-virtual-environment-is-recommended)
* [Setup and Run Application](#setup)



## General info
This webapp has been created/developed by students of SJSU as a part of class project for CMPE-133.

## Technologies
Project is created with:
* Flask Python
* Python 
* Flask-Login
* Flask-WTF
* SQLAlchemy
* Flask-Reuploaded
* Bootstraps
* CSS
* Plaid API
* React

## Setup
- Prerequisites: Python 3
    Python installation: [https://www.python.org/downloads/](https://www.python.org/downloads/)
    NPM Installation:  [https://docs.npmjs.com/downloading-and-installing-node-js-and-npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
# Using zip folder source code:
Extract the zip folder of the project and open terminal on your computer and navigate to project directory:

#### Start the react server for plaid api services:
```
cd frontend
rm -rf node_modules
rm -rf package-lock.json
npm install react-scripts
npm install
npm run start
```
#### Start the main server by creating virtual evn:
```
cd python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install flask_mail
pip install flask_uploads
pip install -U Werkzeug==0.16.0
python3 run.py
```


# Using Github
To run this project, install it locally using terminal with these commands:

    $ git clone git@github.com:jagz97/Cmpe133-Project.git
    $ cd Cmpe131-Team-6
    


To install all required dependencies, type this command inside the project directory:

### Using virtual Environment is Recommended:
On terminal after sucessfully cloning the repository navigate to the project directory:
- Make virtual environment using python3:

```linux
$ python3 -m venv venv
```  
    

- Activate the virtual environment:
```linux
$ . venv/bin/activate
```

- Install all the required dependencies:

```
$ pip install -r requirements.txt
```
    


- Once the app starts running, it can be accessed from the local host which is available at url for local host http://127.0.0.1:8000/




### Addresses:
- The home page is accessed through the local host post:5000 url http://127.0.0.1:8000/
- The sign up page can be accessed through the `/signUp` link.
- The login page can be accessed through the `/login` link.
- Plaid API services will be running on `localhost:3000`



