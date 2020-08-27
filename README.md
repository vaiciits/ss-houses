# Crawler for houses on SS.com
Crawls and parses new ads for house sellings.
## Setup
### Windows
Setup virtual enviornment for python:
```
python -m venv ./
```
For activation run PowerShell as admin and execute:
```
Set-ExecutionPolicy RemoteSigned
```
Activate the virtual enviornment:
```
.\Scripts\Activate
```
Execute in PowerShell:
```
Set-ExecutionPolicy Restricted
```
Upgrade pip:
```
python -m pip install --upgrade pip
```
Setup configuration:
```
cp dist\params.json params.json
```
Packages:
```
pip install requests
pip install bs4
pip install SQLAlchemy
pip install psycopg2pip install pylint-flask
pip install pylint-flask-sqlalchemy
```
### Ubuntu
Setup virtual enviornment for python and activate it:
```
apt-get install python3-venv
python3 -m venv ./
```
Activation:
```
. ./bin/activate
```
Setup configuration:
```
cp dist/params.json params.json
```
```
Packages:
```
pip install requests
pip install bs4
pip install SQLAlchemy
pip install psycopg2
```