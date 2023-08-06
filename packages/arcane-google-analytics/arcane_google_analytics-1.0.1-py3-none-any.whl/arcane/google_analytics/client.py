
from typing import Dict, List, Optional
import backoff
import json
import logging

from arcane.core.exceptions import BadRequestError

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .exceptions import GoogleAnalyticsAccountLostAccessException, GoogleAnalyticsServiceDownException, GA_EXCEPTIONS_TO_RETRY


class GaClient:
    def __init__(
        self,
        adscale_key: str,
        ga_view_id: str
    ):
        self.adscale_key = adscale_key
        self.ga_view_id = ga_view_id.replace('ga:', '')

        
    def init_service(self, scope):
        version = 'v3' if scope == 'analytics' else 'v4'
        scopes = ['https://www.googleapis.com/auth/analytics.readonly']  
        
        credentials = service_account.Credentials.from_service_account_file(self.adscale_key, scopes=scopes)
        service = build(scope, version, credentials=credentials, cache_discovery=False)

        return service


    def __get_exception_message__(self) -> str:
        return f'We cannot access your view with the id: {self.ga_view_id} from the Arcane account. Are you sure you granted access and gave the correct ID?'

    @backoff.on_exception(backoff.expo, (GA_EXCEPTIONS_TO_RETRY), max_tries=3)
    def get_metrics_from_view(self,
                            date_ranges: Optional[List[Dict]]=None,
                            metrics: Optional[List]=None,
                            **optional_params):
        """
        helper to call the Google Analytics Core Reporting API. More information on the following link :
        https://developers.google.com/analytics/devguides/reporting/core/v4/basics
        """

        if metrics is None:
            metrics = [{'expression': 'ga:transactions'}]
        if date_ranges is None:
            date_ranges = [{'startDate': '30daysAgo', 'endDate': 'yesterday'}]

        required_params = {
            'viewId': self.ga_view_id,
            'dateRanges': date_ranges,
            'metrics': metrics
            }
        body = {'reportRequests': [{ **required_params, **optional_params}]}

        service = self.init_service('analyticsreporting')
        try:
            res = service.reports().batchGet(body=body).execute()
        except HttpError as err:
            message = json.loads(err.content).get('error').get('message')
            raise BadRequestError(f'Error while getting data from GA. "{message}"') from err
        logging.info(res)
        return res


    @backoff.on_exception(backoff.expo, (GA_EXCEPTIONS_TO_RETRY), max_tries=3)
    def get_view_name(self) -> Optional[str]:
        """
            From an view id check if user has access to it and return the name of view

            adscale_key or access_token must be specified
        """
        # Create service to access the Google Analytics API


        service = self.init_service('analytics')

        try:
            views = service.management().profiles().list(accountId='~all', webPropertyId='~all').execute()
        except HttpError as err:
            if err.resp.status >= 400 and err.resp.status < 500:
                raise GoogleAnalyticsAccountLostAccessException(self.__get_exception_message__())
            else:
                raise GoogleAnalyticsServiceDownException(f"The Google Analytics API does not respond. Thus, we cannot check if we can access your Google Analytics account with the id: {self.ga_view_id}. Please try later" )

        if self.ga_view_id not in [view.get('id') for view in views.get('items', [])]:
            raise GoogleAnalyticsAccountLostAccessException(self.__get_exception_message__())

        for view in views.get('items', []):
            if view.get('id') == self.ga_view_id:
                return view.get('name', '')
