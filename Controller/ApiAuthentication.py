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
        'username': "Takenrapportage",
        'password': 'Z5Zz2myC7Wde3_93',
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


    def writeSession(self, session):
        with open('session.json', 'w') as f:
            json.dump(session, f)

    def login(self):
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