from __future__ import annotations
from typing import Mapping, Tuple

import tradebot.config.tradebot_config as tradebot_config
from tradebot.utils.exceptions import BadResponseException

import requests
from urllib.parse import urlencode


class TradeBot:
    __base_url = "https://api.tdameritrade.com/v1/"

    def __init__(self, configs:tradebot_config.TradeBotConfigs):
        self.__configs = configs


    def __auth_request_get(self, url:str, headers:Mapping[str, str]=None):
        '''
        Automatically handles authentication, using access_token from configs.
        Can pass optional headers arg to override default.
        '''
        headers = headers or {
            "Authorization": f"Bearer {self.__configs.get('access_token')}"
        }
        res = requests.get(url, headers=headers)
        return res

    
    def get_price_history(self, ticker:str, periodType:str, period:int, frequencyType:str, frequency:str):
        '''
        'ticker' is the stock ticker to be queried.
        'periodType' is the period to show. Valid values
        include 'day', 'month', 'year', or 'ytd'.
        'period' is the number of periods to show.
        'frequencyType' is the frequency units to use. Valid
        values will depend on the 'periodType'. Valid values for each 
        periodType are shown; the default value is marked with an asterisk.

            day: minute*
            month: daily, weekly*
            year: daily, weekly, monthly*
            ytd: daily, weekly*

        'frequency' is the number of frequencyType to include in each candle.
        Valid frequencies by frequencyType (defaults marked with an asterisk):

            minute: 1*, 5, 10, 15, 30
            daily: 1*
            weekly: 1*
            monthly: 1*
        '''
        apikey = self.__configs.get("consumer_key")
        query_string = urlencode({"apikey": apikey, "periodType": periodType, "period": period, "frequencyType": frequencyType, "frequency": frequency})
        url = f"{self.__base_url}marketdata/{ticker}/pricehistory?{query_string}"
        res = self.__auth_request_get(url)

        if not res.ok:
            raise BadResponseException(f"Ensure that the provided query parameters are correct and the device is connected to the internet")
        
        return res.json()


    def get_fundamentals(self, ticker:str) -> Tuple:
        '''
        Returns a 2-tuple where the first item is the symbol that was queried.
        The second item is a dictionary containing the fundamental data for that ticker.
        '''
        apikey = self.__configs.get("consumer_key")
        query_string = urlencode({"apikey": apikey, "symbol": ticker, "projection": "fundamental"})
        url = f"{self.__base_url}instruments?{query_string}"
        res = self.__auth_request_get(url)

        if not res.ok:
            raise BadResponseException(f"Ensure that the provided query parameters are correct and the device is connected to the internet")
            
        data = res.json()
        fundamental_data = data.get(ticker).get("fundamental")
        
        return (ticker, fundamental_data)


    def post_access_token(self):
        '''
        Returns a dictionary with the following data:
        {
            'access_token': '',
            'expires_in': '',
            'scope': '',
            'token_type': '',
        }
        '''
        grant_type = "refresh_token"
        refresh_token = self.__configs.get("refresh_token")
        client_id = self.__configs.get("consumer_key")
        url = f"{self.__base_url}oauth2/token"
        payload = {
            "grant_type": grant_type,
            "refresh_token": refresh_token,
            "client_id": client_id
        }

        res = requests.post(url, data=payload)
        
        if not res.ok:
            raise BadResponseException("Ensure that the provided query parameters are correct and the device is connected to the internet", res)
        
        return res.json()