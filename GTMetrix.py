import requests
import requests.auth


class GTMetrixAPI(object):

    """docstring for GTMetrixAPI"""
    API_URL = "https://gtmetrix.com/api/0.1/test"

    def __init__(self, email, apiToken):
        self._email = email
        self._apiToken = apiToken
        self._httpAuthentication = requests.auth.HTTPBasicAuth(
            self._email, self._apiToken)
        self.testResource = None

    @property
    def email(self):
        return self._email

    @property
    def apiToken(self):
        return self._apiToken

    @property
    def httpAuthentication(self):
        return self._httpAuthentication

    def startTest(self, url):
        httpRequest = requests.post(
            GTMetrixAPI.API_URL, auth=self._httpAuthentication, data={"url": url})
        self.testInformation = httpRequest.json()

    def getTestResults(self):
        httpRequest = requests.get(
            self.testInformation["poll_state_url"], auth=self._httpAuthentication)
        self.testResource =  httpRequest.json()

    def getPageSpeed(self):
        httpRequest = requests.get(self.testResource["resources"]["pagespeed"], auth=self._httpAuthentication)
        return httpRequest.json()


username = "jose.colella@dynatrace.com"
apiKey = "43b7a445ee75fefe746e603d2bf783c2"
