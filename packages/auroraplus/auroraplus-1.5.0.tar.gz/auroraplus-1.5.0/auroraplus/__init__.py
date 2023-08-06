"""Abstraction of the Aurora+ API"""
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import Timeout

class api:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.error = None
        self.token = None
        self.url = 'https://api.auroraenergy.com.au/api'  
        api_adapter = HTTPAdapter(max_retries=2)
        
        """Create a session and perform all requests in the same session"""
        session = requests.Session()
        session.mount(self.url, api_adapter)
        session.headers.update({'Accept': 'application/json', 'User-Agent': 'AuroraPlus.py', 'Accept-Encoding' : 'gzip, deflate, br', 'Connection' : 'keep-alive' })
        self.session = session

    def gettoken(self): 
        """Get access token"""
        try:
            token = self.session.post(self.url+'/identity/login',data={'username': self.username, 'password': self.password}, timeout=(6))
            if (token.status_code == 200):
                tokenjson = token.json()
                self.token = tokenjson['accessToken']

                """Get CustomerID and ServiceAgreementID"""
                current = self.session.get(self.url+'/customers/current',headers={'Authorization': self.token}).json()[0]
                self.customerId = current['CustomerID']

                """Loop through premises to get active """
                premises = current['Premises']
                for premise in premises:
                    if (premise['ServiceAgreementStatus'] == 'Active'):
                        self.Active = premise['ServiceAgreementStatus'] 
                        self.serviceAgreementID = premise['ServiceAgreementID']
                if (self.Active != 'Active'):
                    self.error = 'No active premise found'
                    return self.error
                else:
                    return True
            elif (token.status_code == 400):
                self.error = 'Invalid username or password'
                return self.error
            elif (token.status_code == 401):
                self.error = 'Invalid username or password'
                return self.error
            elif (token.status_code == 404):
                self.error = 'Not Found' 
                return self.error
            else:
                self.error = 'Token request failed'
                return self.error
        except Timeout:
            self.error = 'Token request timed out'
            return self.error

    def request(self, timespan): 
        try:
            params = {'serviceAgreementID': self.serviceAgreementID, 'customerId': self.customerId, 'index' :-1}
            request = self.session.get(self.url + '/usage/' + timespan, params=params, headers={'Authorization': self.token})
            if (request.status_code == 200):
                return request.json()
            else:
                self.error = 'Data request failed'
        except Timeout:
            self.error = 'Data request timed out'

    def getsummary(self):
        summarydata = self.request("day")
        self.DollarValueUsage = summarydata['SummaryTotals']['DollarValueUsage']
        self.KilowattHourUsage = summarydata['SummaryTotals']['KilowattHourUsage']

    def getday(self):
        self.day = self.request("day")

    def getweek(self):
       self.week = self.request("week")

    def getmonth(self):
       self.month = self.request("month")

    def getquarter(self):
       self.quarter = self.request("quarter")

    def getyear(self):
       self.year = self.request("year")

    def getcurrent(self):
        try:
            """Request current customer data"""
            current = self.session.get(self.url + '/customers/current',headers={'Authorization': self.token})

            if (current.status_code == 200):
                currentjson = current.json()[0]

                """Loop through premises to match serviceAgreementID already found in token request"""
                premises = currentjson['Premises']
                found = ''
                for premise in premises:
                    if (premise['ServiceAgreementID'] == self.serviceAgreementID):
                        found = 'true'
                        self.AmountOwed = "{:.2f}".format(premise['AmountOwed'])
                        self.EstimatedBalance = "{:.2f}".format(premise['EstimatedBalance'])
                        self.AverageDailyUsage = "{:.2f}".format(premise['AverageDailyUsage'])
                        self.UsageDaysRemaining = premise['UsageDaysRemaining']
                        self.ActualBalance = "{:.2f}".format(premise['ActualBalance'])
                        self.UnbilledAmount = "{:.2f}".format(premise['UnbilledAmount'])
                        self.BillTotalAmount = "{:.2f}".format(premise['BillTotalAmount'])
                        self.NumberOfUnpaidBills = premise['NumberOfUnpaidBills']
                        self.BillOverDueAmount = "{:.2f}".format(premise['BillOverDueAmount'])
                if (found != 'true'):
                    self.error = 'ServiceAgreementID not found'
            else:
                self.error = 'Current request failed: ' + current.reason
        except Timeout:
            self.error = 'Current request timed out'