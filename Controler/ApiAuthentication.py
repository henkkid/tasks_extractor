import datetime
import json
from pathlib import Path
import requests as r


class ApiAuthentication: 

    def __init__(self):
        self.session = self.getSession()
        if(self.session['token'] == ''):
            self.login()
        if self.isExpired():
            self.login()
            
    config = {
        "apiurl": 'https://portal.everyoffice.nl/api',
        'username': "",
        'password': '',
    }

    session = {
        'token': '',
        'expires':''
    }

    def isExpired(self):
        expires = datetime.datetime.fromisoformat(self.session['expires'])
        now = datetime.datetime.now(datetime.timezone.utc)
        now = now.replace(tzinfo=None)
        expires = expires.replace(tzinfo=None)

        if now > expires:
            return True
        else:
            return False

    def getSession(self):
        if Path('./session.json').is_file(): 
            with open('session.json', 'r') as f:
                session = json.load(f)
            return session
        else:
            return {
                'token': '',
                'expires':''
            }
        
    def getCredentials(self):
        if Path('./credentials.json').is_file():
            with open('credentials.json', 'r') as f:
                credentials = json.load(f)
            return credentials
        
    def create_config(self):
        credentials = self.getCredentials()

        self.config['apiurl'] = credentials['apiurl']
        self.config['username'] = credentials['username']
        self.config['password'] = credentials['password']


    def writeSession(self, session):
        with open('session.json', 'w') as f:
            json.dump(session, f)

    def login(self):
        self.create_config()
        
        requestURL = self.config['apiurl'] + '/auth/login'
        requestBody = {
            "user": self.config['username'],
            "password": self.config['password']
        }
        loginresponse = r.post(url=requestURL, json=requestBody)
        self.session['token'] = loginresponse.json()['token']
        self.session['expires'] = loginresponse.json()['expires_at']
        self.writeSession(self.session)
        
    def getToken(self):
        if self.isExpired():
            self.login()
        return 'Bearer ' + self.session['token']
    
    def getAPIBaseUrl(self):
        return self.config['apiurl']