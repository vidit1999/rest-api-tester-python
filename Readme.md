# REST Api Tester in Python

### Features
* Live reload.
* Keep alive connections.
* Specify request params and others in simple json format.

### Setup
```
$ python -m venv venv
$ venv/Scripts/activate
(venv) $ pip install -r requirements.txt
```

### Usage
* For help run,
```
(venv) $ python rest_api_tester.py --help
```
* Example,
```
(venv) $ python rest_api_tester.py --generate request.json
Request file request.json generated.
Check the file for more information.


Expected Request JSON File : request.json
Expected Response JSON File : response.json
Do you want live reload? [Y/n] y

Watching for changes in file request.json .....
Press Ctrl+C to quit
```
