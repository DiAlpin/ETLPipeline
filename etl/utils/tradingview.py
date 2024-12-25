import json
import requests
import random
import string
import re
import datetime
import pandas as pd
from websocket import create_connection



class TVHistoricalPrices:
    _sign_in_url = 'https://www.tradingview.com/accounts/signin/'
    _signin_headers = {'Referer': 'https://www.tradingview.com'}
    _ws_tradingview_url = 'wss://data.tradingview.com/socket.io/websocket'
    _ws_headers = json.dumps({"Origin": "https://data.tradingview.com"})
    _ws_timeout = 5
    _prices_df_cols = [
        'datetime',
        'open',
        'high',
        'low',
        'close',
        'volume',
        ]
    _intervals_map = {
        '1m': "1",
        '3m': "3",
        '5m': "5",
        '15m': "15",
        '30m': "30",
        '45m': "45",
        '1H': "1H",
        '2H': "2H",
        '3H': "3H",
        '4H': "4H",
        '1D': "1D",
        '1W': "1W",
        '1M': "1M",
        }
    _quote_fields = [
        "ch",
        "chp",
        "current_session",
        "description",
        "local_description",
        "language",
        "exchange",
        "fractional",
        "is_tradable",
        "lp",
        "lp_time",
        "minmov",
        "minmove2",
        "original_name",
        "pricescale",
        "pro_name",
        "short_name",
        "type",
        "update_mode",
        "volume",
        "currency_code",
        "rchp",
        "rtc",
        ]

    def __init__(self, exchange='BVB'):
        self.exchange = exchange
        self.credentials = self._get_tradingview_credentials()
        self.token = self._auth() if self.credentials else "unauthorized_user_token"
        self.ws = None
        self.session_id = self._generate_random_id('qs')
        self.chart_id = self._generate_random_id('cs')

    def _get_tradingview_credentials(self):
        """Base features can work without credentials, but for advance
        features credentisls should be provided.
        ex of credentials
            {            
                'username': 'user_abc',
                'password': 'pass_123',
                'remember': 'on'
            }
        """
        return None

    def _auth(self):
        try:
            response = requests.post(
                url=self._sign_in_url, data=self.credentials, headers=self._signin_headers)
            token = response.json()['user']['auth_token']
        except Exception as e:
            print(e)
            token = None

        return token
    
    def _create_connection(self):
        self.ws = create_connection(
            self._ws_tradingview_url, headers=self._ws_headers, timeout=self._ws_timeout
        )

    @staticmethod
    def _generate_random_id(code, length=12):
        random_sring = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
        return f'{code}_{random_sring}'

    @staticmethod
    def _append_header(message):
        return f"~m~{len(message)}~m~{message}"

    @staticmethod
    def _construct_message(func, param_list):
        return json.dumps({"m": func, "p": param_list}, separators=(",", ":"))

    def _create_message(self, func, paramList):
        return self._append_header(self._construct_message(func, paramList))
    
    def _send_message(self, func, args):
        m = self._create_message(func, args)
        self.ws.send(m)

    def _convert2df(self, data, symbol):
        df = pd.DataFrame(data, columns=self._prices_df_cols)#.set_index("datetime")
        df.insert(0, "symbol", value=symbol)

        return df

    @staticmethod
    def _get_row(row):
        splited_row = re.split("\[|:|,|\]", row)
        dt = datetime.datetime.fromtimestamp(float(splited_row[4]))
        row_values = [dt]

        for i in range(5, 10):
            try:
                row_values.append(float(splited_row[i]))
            except ValueError:
                row_values.append(0.0)

        return row_values

    def _create_df(self, raw_data, symbol):
        try:
            out = re.search('"s":\[(.+?)\}\]', raw_data)[1]
            body = out.split(',{"')
            data = []

            for chunk in body:
                row = self._get_row(chunk)
                data.append(row)

            return self._convert2df(data, symbol)

        except AttributeError as e:
            raise ValueError(f"No data for {symbol}, please check the exchange and symbol") from e
        
        except Exception as e:
            raise ValueError(e) from e
        
    def _check_interval(self, interval):
        assert interval in self._intervals_map.keys(), f"'{interval}' is not a valid interval"

        return self._intervals_map[interval]
    
    @staticmethod
    def _compose_symbol_arg(symbol, extended_session):
        session_type = '"extended"' if extended_session else '"regular"'
        return '={"symbol":"' + symbol + '","adjustment":"splits","session":' + session_type + '}'

    def _send_messages(self, symbol, interval, n_bars, extended_session):
        self._create_connection()
        self._send_message("set_auth_token", [self.token])
        self._send_message("chart_create_session", [self.chart_id, ""])
        self._send_message("quote_create_session", [self.session_id])
        self._send_message("quote_set_fields", [self.session_id, *self._quote_fields])

        flags = {"flags": ["force_permission"]}
        self._send_message("quote_add_symbols", [self.session_id, symbol, flags])
        self._send_message("quote_fast_symbols", [self.session_id, symbol])
        self._send_message("resolve_symbol", [self.chart_id, 
                                              "symbol_1", 
                                              self._compose_symbol_arg(symbol, extended_session)])
        self._send_message("create_series", [self.chart_id, 
                                             "s1", 
                                             "s1", 
                                             "symbol_1", 
                                             interval, 
                                             n_bars])
        self._send_message("switch_timezone", [self.chart_id, "exchange"])


    def get_hist(self, 
                 symbol: str, 
                 interval: str, 
                 n_bars: int, 
                 extended_session: bool = False
        ) -> pd.DataFrame:
        """
        Get historical prices for a given symbol.

        Args:
            symbol (str): The symbol for which to retrieve historical prices.
            interval (str, optional): The interval of the historical prices.
            n_bars (int, optional): The number of historical bars to retrieve. Max 5_000.
            extended_session (bool, optional): Whether to include extended session data. Defaults to False.

        Returns:
            pd.DataFrame: A DataFrame containing the historical prices.

        """

        std_symbol = f'{self.exchange}:{symbol.upper()}'
        std_interval = self._check_interval(interval)
        self._send_messages(std_symbol, std_interval, n_bars, extended_session)

        raw_data = ""
        while True:
            try:
                result = self.ws.recv()
                raw_data = raw_data + result + "\n"
            
            except Exception as e:
                break
            if "series_completed" in result:
                break

        return self._create_df(raw_data, symbol)
