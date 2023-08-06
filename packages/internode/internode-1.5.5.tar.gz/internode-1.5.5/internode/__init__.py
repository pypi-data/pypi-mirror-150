"""Abstraction of the Internode API"""
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import Timeout
from xml.etree import ElementTree
from contextlib import contextmanager
import sys

@contextmanager
def disable_exception_traceback():
    """
    All traceback information is suppressed and only the exception type and value are printed
    """
    default_value = getattr(sys, "tracebacklimit", 1000)  # `1000` is a Python's default value
    sys.tracebacklimit = 0
    yield
    sys.tracebacklimit = default_value  # revert changes

class api:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.error = None
        self.url = 'https://customer-webtools-api.internode.on.net/api/v1.5'  
        api_adapter = HTTPAdapter(max_retries=2)
        
        """Create a session and perform all requests in the same session"""
        session = requests.Session()
        session.mount(self.url, api_adapter)
        session.headers.update({'Accept': 'application/json', 'User-Agent': 'Internode.py', 'Accept-Encoding' : 'gzip, deflate, br', 'Connection' : 'keep-alive' })
        self.session = session

    def connect(self):
        result = self.authenticate()
        if result:
            self.getserviceid()
            return True
        else:
            return False

    def getserviceid(self):
        """Get ServiceAgreementID"""
        servicexml = self.xml.find('api/services/service')
        self.serviceAgreementID = servicexml.text
            
    def authenticate(self):
        """Authenticate"""
        try:
            self.auth = (self.username, self.password)
            auth = self.session.get(self.url, auth=self.auth, timeout=(2, 5))
            if (auth.status_code == 200):
              self.xml = ElementTree.fromstring(auth.content)
              error = self.xml.find('error/msg')
              if (error is None):
                  return True
            elif (auth.status_code == 401):  
                self.error = 'Invalid username or password'
                return self.error
            elif (auth.status_code == 404):
                self.error = 'Not Found'  
                return self.error
        except Timeout:
            self.error = 'Auth request timed out' 
            return self.error
    
    def request(self, type): 
        try:
            request = self.session.get(self.url + '/' + self.serviceAgreementID + '/' + type, auth=self.auth)
            requestxml = ElementTree.fromstring(request.content)

            error = requestxml.find('error/msg')
            if (error is None):
                return request
            else:
                with disable_exception_traceback():
                    raise Exception('Data request failed: ' + request.reason)
        except Timeout:
            raise Exception('Data request timed out')

    def getservice(self):
        servicedata = self.request('service')
        self.service = servicedata.text

    def getusage(self):
        usagedata = self.request('usage')
        tree = ElementTree.fromstring(usagedata.content)
        usagexml = tree.find('api/traffic')
        usage = float(usagexml.text)/1000000000
        self.usage = "{:.2f}".format(usage)
        self.rollover = usagexml.get('rollover')
        self.planinterval = usagexml.get('plan-interval')
        self.quota = float(usagexml.get('quota'))/1000000000

    def gethistory(self):
        historydata = self.request('history')
        tree = ElementTree.fromstring(historydata.content)
        historyxml = tree.find('api/usagelist/usage/traffic')
        history = float(historyxml.text)/1000000000
        self.history = "{:.2f}".format(history)