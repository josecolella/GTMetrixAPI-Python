# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import with_statement
import re
import requests
import requests.auth


class GTMetrixAPI(object):

    """GTMetrixAPI class provides a python client to the features of the GTMetrixAPI
    encapsulating all appropriate methods within the class

    Attributes:
        _email (str): The email associated to the GTMetrix API
        _apiToken (str): The api token associated to the GTMetrix API
        _httpAuthentication (requests.auth.HTTPBasicAuth): The HTTP Basic authentication object
    """
    API_URL = "https://gtmetrix.com/api/0.1/test"

    def __init__(self, email, apiToken):
        """
        """
        self._email = email
        self._apiToken = apiToken
        self._httpAuthentication = requests.auth.HTTPBasicAuth(
            self._email, self._apiToken)
        self.testResource = None
        self._htmlCleanRegex = re.compile("<.*?>")

    @property
    def email(self):
        return self._email

    @property
    def apiToken(self):
        return self._apiToken

    @property
    def httpAuthentication(self):
        return self._httpAuthentication

    def requestTest(self, url):
        """Creates a request for a specific url

        Args:
            url (str): The url to test
        """
        httpRequest = requests.post(
            GTMetrixAPI.API_URL, auth=self._httpAuthentication, data={"url": url})
        self.testInformation = httpRequest.json()

    def getTestResults(self):
        """
        TODO
        Example:
        {'error': '',
         'resources': {'har': 'https://gtmetrix.com/api/0.1/test/KwQrzFbM/har',
          'pagespeed': 'https://gtmetrix.com/api/0.1/test/KwQrzFbM/pagespeed',
          'pagespeed_files': 'https://gtmetrix.com/api/0.1/test/KwQrzFbM/pagespeed-files',
          'report_pdf': 'https://gtmetrix.com/api/0.1/test/KwQrzFbM/report-pdf',
          'report_pdf_full': 'https://gtmetrix.com/api/0.1/test/KwQrzFbM/report-pdf?full=1',
          'screenshot': 'https://gtmetrix.com/api/0.1/test/KwQrzFbM/screenshot',
          'yslow': 'https://gtmetrix.com/api/0.1/test/KwQrzFbM/yslow'},
         'results': {'html_bytes': '20793',
          'html_load_time': '523',
          'page_bytes': '1422612',
          'page_elements': '101',
          'page_load_time': '3012',
          'pagespeed_score': '85',
          'report_url': 'https://gtmetrix.com/reports/santander.co.uk/DmraeRIa',
          'yslow_score': '68'},
         'state': 'completed'}
        """
        httpRequest = requests.get(
            self.testInformation["poll_state_url"], auth=self._httpAuthentication)
        self.testResource = httpRequest.json()

    def _getPageSpeedInformation(self):
        """
        TODO
        """
        httpRequest = requests.get(
            self.testResource["resources"]["pagespeed"], auth=self._httpAuthentication)
        self.pageSpeedInformation = httpRequest.json()

    def _getYSlowInformation(self):
        """
        TODO
        """
        httpRequest = requests.get(
            self.testResource["resources"]["yslow"], auth=self._httpAuthentication)
        self.ySlowInformation = httpRequest.json()

    def savePageSpeedRecommendations(self, fileName, limit=6):
        """
        TODO
        """
        self._getPageSpeedInformation()
        possibleRecommendations = filter(
            lambda rule: rule["score"] < 100, self.pageSpeedInformation["rules"])
        with open(fileName, "w") as file:
            for possibleRecommendation in possibleRecommendations:
                cleanRecommendationDetail = re.sub(
                    self._htmlCleanRegex, "", possibleRecommendation["warnings"])
                file.write("{recommendationName},Score:{recommendationScore};Recommendations:{recommendationDetail}\n".format(recommendationName=possibleRecommendation[
                           "name"], recommendationScore=possibleRecommendation["score"], recommendationDetail=cleanRecommendationDetail))
            file.close()

    def saveYSlowRecommendations(self, fileName, limit=6):
        """
        TODO
        """
        pass
