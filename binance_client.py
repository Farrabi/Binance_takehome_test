from time import sleep
import requests
import pandas as pd
from prometheus_client import start_http_server, Gauge
from json import loads
from collections import deque

class BinanceClient:

    BASE_URL = 'https://api.binance.com/api'


    def __init__(self):
        """Init client variables"""
        
        self.BASE_URL = self.BASE_URL
        self.spread_deque = deque(maxlen=2)
        self.gauge_metric_spread_delta = Gauge('absolute_delta','absolute delta of price spread with previous spread 10 seconds ago', ['symbol'])
        self.gauge_metric_current_spread = Gauge('spread','current price spread', ['symbol'])

    
    def check_api(self):
        """ check Binance API"""

        uri = "/v3/ping"
        request = requests.get(self.BASE_URL + uri)

        if request.status_code != 200:
            raise Exception("Binance API is not available")

    def get_top_symbols(self, asset:str, reponse_json_key:str, print_output=False)->dict:
        """
        Return the top 5 symbols with quote asset BTC
        and the highest volume over the last 24 hours
        in descending order
        """
        uri = "/v3/ticker/24hr"
       
        res =   {}

        request = requests.get(self.BASE_URL + uri)
        df = pd.DataFrame(request.json())
        df = df[['symbol', reponse_json_key]]
        df = df[df.symbol.str.contains(r'(?!$){}$'.format(asset))]
        df[reponse_json_key] = pd.to_numeric(df[reponse_json_key], downcast='float', errors='coerce')
        df_json = df.sort_values(by=[reponse_json_key], ascending=False).head().to_json(orient ='values')
        df_json = loads(df_json)
        for symbol, json_key in df_json:
                res[symbol] = json_key
        if print_output:
            print(f"\n Top Symbols for {asset} by {reponse_json_key} during last 24 hours")
            print(res)
        return res

    def get_notional_value(self, asset:str, reponse_json_key:str, print_output=False)->dict:

        """
        Return the total notional value of the
        200 bids and asks on each symbol's order book.
        """

        uri = "/v3/depth" 

        symbols = self.get_top_symbols(asset, reponse_json_key, print_output=False)
        notional = {}

        for symbol in symbols.keys():
            payload = { 'symbol' : symbol, 'limit' : 500 }
            request = requests.get(self.BASE_URL + uri, params=payload)
            for col in ["bids", "asks"]:
                df = pd.DataFrame(data=request.json()[col], columns=["price", "quantity"], dtype=float)
                df = df.sort_values(by=['price'], ascending=False).head(200)
                df['notional'] = df['price'] * df['quantity']
                df['notional'].sum()
                notional[symbol + '_' + col] = df['notional'].sum()

        if print_output:
            print(f"\n Total Notional value of top 5 {asset} by {reponse_json_key}")
            print(notional)

        return notional

    def get_price_spread(self, asset:str, reponse_json_key:str, print_output=False)->dict:
        """
        Return the price spread for each symbols
        spread = lowest ask - highest bid. 
        """

        uri = '/v3/ticker/bookTicker'

        symbols = self.get_top_symbols(asset, reponse_json_key)
        spread = {}

        for symbol in symbols.keys():
            payload = { 'symbol' : symbol }
            request = requests.get(self.BASE_URL + uri, params=payload)
            price_spread = request.json()
            spread[symbol] = float(price_spread['askPrice']) - float(price_spread['bidPrice'])
 
        if print_output:
            print(f"\n Price Spread for {asset} by {reponse_json_key} during last 24 hours")
            print(spread)

        return spread

    def get_spread_delta(self, asset:str, reponse_json_key:str, print_output=False)->dict:

        res = {}
	# use a deque to store neatly the previous value can be scaled to any size of deque. 
        if len(self.spread_deque) < 1:
            lag_spread= self.get_price_spread(asset, reponse_json_key)
            self.spread_deque.append(lag_spread)
            sleep(10)
            current_spread = self.get_price_spread(asset, reponse_json_key)
            self.spread_deque.append(current_spread)
        else:
            sleep(10)
            current_spread = self.get_price_spread(asset, reponse_json_key)
            self.spread_deque.append(current_spread)
        
        previous_value = self.spread_deque.popleft()
        current_value = current_spread

        for key in current_spread:

            res[key] = [current_value[key],previous_value[key] , abs(current_value[key]-previous_value[key])]
        
        for key in res:
            self.gauge_metric_current_spread.labels(f'{key}_current_spread').set(res[key][0]) # current spread in prometheus format metric
            self.gauge_metric_spread_delta.labels(f'{key}_delta_map_spread').set(res[key][1]) # delta spread in prometheus format metric

        if print_output:
            print(f"\n Absolute Delta for {asset}")
            print(res)
        return res
    
    
if __name__ == "__main__":
    # initiate the server to show  metrics.
    start_http_server(8080)
    client = BinanceClient()
    client.check_api()
    # As market is volatile maybe more customer friendly to expose those metrics every seconds via an api endpoint. 
    client.get_top_symbols('BTC','quoteVolume',True)
    client.get_top_symbols('USDT', 'count', True)
    client.get_notional_value('BTC', 'quoteVolume', True)
    client.get_price_spread('USDT', 'count', True)

    while True:
        client.get_spread_delta('USDT', 'count', True)

