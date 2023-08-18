import datetime
import string
import re
import threading
import time
from mysql import connector
from mysql.connector.errors import ProgrammingError, InterfaceError
from _mysql_connector import MySQLInterfaceError
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler  # Web server
from urllib.parse import urlparse, parse_qs  # Address bar processing
import shutil  # File access
import json  # Processing json
import logging
from logger_setup import logger


# An array of all our exchanges and their settings
class Setting:
    settings_file = open("settings.json", "r")
    setting = json.loads(settings_file.read())
    exchanges = setting['exchanges']
    # {
    #     "Binance": {
    #         "auto_start": True,  # Autoload start
    #         "count_load": 0,  # Number of downloads since the start
    #         "icon": "Binance.png",  # Icon
    #         "last_time": 0,  # Last successful download
    #         "number": 1,  # Exchange number in the database
    #         "log": ""  # Last message after uploading
    #     },
    #     "Gate": {
    #         "auto_start": True,
    #         "count_load": 0,
    #         "icon": "Gate.png",
    #         "last_time": 0,
    #         "number": 2,
    #         "log": ""
    #     },
    #     "Huobi": {
    #         "auto_start": True,
    #         "count_load": 0,
    #         "icon": "Huobi.png",
    #         "last_time": 0,
    #         "number": 3,
    #         "log": ""
    #     },
    #     "KuCoin": {
    #         "auto_start": True,
    #         "count_load": 0,
    #         "icon": "KuCoin.png",
    #         "last_time": 0,
    #         "number": 4,
    #         "log": ""
    #     }
    # }

    # # Array of settings
    # setting = {
    #     "refreshTime": 180,  # Reloading time in seconds
    #     "host": "localhost",  # Host for MySQL
    #     "user": "root",  # MySQL login
    #     "passwd": "",  # MySQL password
    #     "db": "price",  # MySQL database
    #     "checkbox": {  # All CheckBoxes
    #         "history_1m": {  # System name
    #             "name": "Every minute, but no more than 24 hours",  # Title
    #             "act": False  # Status at start-up
    #         },
    #         "history_10m": {  # Системное имя
    #             "name": "Every 10 minutes, but no more than 24 hours.",  # Title
    #             "act": True  # Status at start-up
    #         },
    #         "history_1h": {  # Системное имя
    #             "name": "Every hour, but no more than 24 hours",  # Title
    #             "act": True  # Status at start-up
    #         },
    #         "history_1d": {  # System name
    #             "name": "Once a day, always.",  # Title
    #             "act": True  # Status at start-up
    #         }
    #     },
    #     "time_load": 0
    # }


class Img:
    def load_favicon(self):
        self.send_response(200)
        self.send_header('Content-type', 'image/ico')
        self.end_headers()
        with open(self.path[1:], 'rb') as content:
            shutil.copyfileobj(content, self.wfile)

    def load_img(self):
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()
        with open(self.path[1:], 'rb') as content:
            shutil.copyfileobj(content, self.wfile)


class API:
    # Guiding you on the right path
    def route(self, http, get_array):
        if 'act' in get_array:
            if get_array['act'][0] == 'setting':
                return API.setting(http)
            elif get_array['act'][0] == 'birzi':
                return API.exchanges(http)
            elif get_array['act'][0] == 'onoff':
                return API.onoff(http, get_array)
            elif get_array['act'][0] == 'time_load':
                return API.time_load(http)
            elif get_array['act'][0] == 'checkbox':
                return API.checkbox(http)
            elif get_array['act'][0] == 'checkboxOnOff':
                return API.checkboxOnOff(http, get_array)
            return API.Error(http, get_array)
        else:
            return API.Error(http, get_array)

            # Switching the state of the checkbox in the settings

    def checkboxOnOff(self, http, get_array):
        # Let's change the switch
        if Setting.setting['checkbox'][get_array['name'][0]]['act']:
            Setting.setting['checkbox'][get_array['name'][0]]['act'] = False
        else:
            Setting.setting['checkbox'][get_array['name'][0]]['act'] = True
        # We'll send the new settings
        API.send_json(http, Setting.setting['checkbox'])

    # Let's send all the checkboxes in the settings
    def checkbox(self, http):
        API.send_json(http, Setting.setting['checkbox'])

    # Script loading start time counter        
    def time_load(self, http):
        time_load = {
            "time_load": Setting.setting["refreshTime"] - Setting.setting["time_load"]
        }
        API.send_json(http, time_load)

    # Switching the exchange loading      
    def onoff(self, http, get_array):
        # Let's change the switch
        if Setting.exchanges[get_array['name'][0]]['auto_start']:
            Setting.exchanges[get_array['name'][0]]['auto_start'] = False
        else:
            Setting.exchanges[get_array['name'][0]]['auto_start'] = True
        # We'll send the new settings
        API.send_json(http, Setting.exchanges)

    # List of exchanges
    def exchanges(self, http):
        API.send_json(http, Setting.exchanges)

    # Settings list
    def setting(self, http):
        API.send_json(http, Setting.setting)

    # Send an error message
    def Error(self, http, message):
        error = {
            'code': 'error',
            'message': message
        }
        API.send_json(http, error)

    # Send a message in JSON format   
    def send_json(self, http, message):
        http.send_response(200)
        http.send_header('Content-type', 'application/json; charset=UTF-8')
        http.end_headers()
        jsonRequest = json.dumps(message)
        http.wfile.write(f"{jsonRequest}".encode())


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Let's put all GET request variables into an array
        get_array = parse_qs(urlparse(self.path).query)

        # Working with pictures
        if self.path.startswith("/img/"):
            Img.load_img(self)
        # Let's upload an icon
        elif self.path == "/favicon.ico":
            Img.load_favicon(self)
        # The rest of the paths are processed here.
        elif self.path.startswith("/api/"):
            API.route(self, get_array)
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            if 'act' in get_array:
                self.wfile.write(f"{get_array['act'][0]}".encode())
            else:
                html = open('index.html', 'r', encoding="utf-8").read()
                self.wfile.write(html.encode())


class Exchanges:
    def __init__(self):
        pass

    # Downloading Binance
    def Binance(self):

        try:

            time_start = time.time()  # Let's remember the time of the strat

            # Follow the link to get the data with prices.
            price_list = requests.get(
                "https://api.binance.com/api/v3/ticker/24hr").json()  # We will get the answer in JSON format

            # If there is an error code in the message, it is worth aborting the job.
            if 'code' in price_list:
                print(f"Error code {price_list['code']} msg = {price_list['msg']}")
                return False

            price = []
            # Let's loop through all trading pairs
            # print(price_list)
            # exit()
            for symbol in price_list:
                try:
                    if float(symbol['lastPrice']) > 0:  # Let's check the price availability
                        price.append(
                            [
                                symbol['symbol'],
                                symbol['lastPrice'],
                                symbol['bidPrice'],
                                symbol['askPrice'],
                                float(symbol['bidQty']),
                                float(symbol['askQty']),
                                symbol['volume']
                            ]
                        )

                except Exception as inst:
                    print(inst)  # If there is an error accessing the result

            save_price(price, Setting.exchanges['Binance']['number'])

            # Let's report on progress

            Setting.exchanges['Binance']["count_load"] += 1
            Setting.exchanges['Binance']["log"] = f"Downloaded Binance for {round(time.time() - time_start, 3)} sec."
            log(Setting.exchanges['Binance']["log"], Setting.exchanges['Binance']['number'])
        except Exception as inst:
            print("Exception ", inst)

    # Loading Gate
    def Gate(self):
        time_start = time.time()

        # Get the data as JSON
        data = requests.get("https://api.gateio.ws/api/v4/spot/tickers/").json()

        price = []
        # In the loop, let's go through each currency.
        for symbol in data:
            try:
                price.append(
                    [
                        symbol['currency_pair'],
                        symbol['last'],
                        symbol['highest_bid'],
                        symbol['lowest_ask'],
                        symbol['base_volume'],
                        symbol['quote_volume'],
                        float(symbol['base_volume']) + float(symbol['quote_volume'])
                    ]
                )
            except Exception as inst:
                print(inst)  # If there is an error accessing the result

        save_price(price, Setting.exchanges['Gate']['number'])

        Setting.exchanges['Gate']["count_load"] += 1
        Setting.exchanges['Gate']["log"] = f"Loading Gate for {round(time.time() - time_start, 3)} sec."
        log(Setting.exchanges['Gate']["log"], Setting.exchanges['Gate']['number'])

    # Downloading Huobi
    def Huobi(self):

        time_start = time.time()  # Let's remember the time of the strat

        # Let's get the data with prices from the link.
        price_list = requests.get(
            "https://api.huobi.pro/market/tickers").json()  # We will get the answer in JSON format

        price = []
        # Let's loop through all trading pairs
        for symbol in price_list['data']:
            price.append(
                [
                    symbol['symbol'],
                    symbol['close'],
                    symbol['bid'],
                    symbol['ask'],
                    symbol['bidSize'],
                    symbol['askSize'],
                    symbol['vol']
                ]
            )

        save_price(price, Setting.exchanges['Huobi']['number'])

        # Let's report on progress
        Setting.exchanges['Huobi']["count_load"] += 1
        Setting.exchanges['Huobi']["log"] = f"Loading Huobi for{round(time.time() - time_start, 3)} Sec."
        log(Setting.exchanges['Huobi']["log"], Setting.exchanges['Huobi']['number'])

    # Loading KuCoin
    def KuCoin(self):

        time_start = time.time()  # Let's remember the time of the strat

        # Let's get the data with prices from the link.
        price_list = requests.get(
            "https://api.kucoin.com/api/v1/market/allTickers").json()  # We will get the answer in JSON format

        price = []
        # Let's loop through all trading pairs
        for symbol in price_list['data']['ticker']:
            price.append(
                [
                    symbol['symbol'],
                    symbol['last'],
                    symbol['buy'],
                    symbol['sell'],
                    0.0,
                    0.0,
                    symbol['vol']
                ]
            )

        save_price(price, Setting.exchanges['KuCoin']['number'])
        # Let's report on progress
        Setting.exchanges['KuCoin']["count_load"] += 1
        Setting.exchanges['KuCoin']["log"] = f"Loading KuCoin for{round(time.time() - time_start, 3)} Sec."
        log(Setting.exchanges['KuCoin']["log"], Setting.exchanges['KuCoin']['number'])


# Database connection
def connectDB():
    try:
        with connector.connect(host=Setting.setting["host"], user=Setting.setting["user"],
                               passwd=Setting.setting["passwd"]) as db:
            db.cursor().execute('CREATE DATABASE IF NOT EXISTS exchange_prices')
            db.cursor().execute('USE exchange_prices')
            db.commit()
            with open('price.sql', 'r') as sql_file:
                # print(sql_file.read())
                result_iterator = db.cursor().execute(sql_file.read(), multi=True)
                for res in result_iterator:
                    # print("Running query: ", res)  # Will print out a short representation of the query
                    print(f"Affected {res.rowcount} rows")
    except ProgrammingError as inst:
        logger.critical("Database connection error occurred", exc_info=True)
    except MySQLInterfaceError as e:
        logger.log(level=logging.INFO, msg="Unknown error occurred 4", exc_info=True)
    except InterfaceError as e:
        logger.info("Unknown error occurred 0", exc_info=True)
    except Exception as inst:
        logger.critical("Unknown error occurred 1", exc_info=True)


# Let's calculate the price difference
def price_difference(new: string, old: string):
    if new == '' or new == '0':  # The price must not be blank or 0
        return 0
    else:
        # Let's convert strings to numbers
        old = float(old)
        new = float(new)
        if old == 0:
            return 0
        return round(((new - old) / old) * 100, 2)


# Let's save the list of prices under the exchange number
def save_price(price: list, exchange_id: int):
    try:
        crypto_price_old = {}
        # Let's connect to the database
        with connector.connect(host=Setting.setting["host"], user=Setting.setting["user"],
                               passwd=Setting.setting["passwd"], db=Setting.setting["db"]) as db:
            cursor = db.cursor()
            # Let's create an array with old prices to calculate the price change for 24 hours
            old_time = round(time.time()) - 86400 + 600  # Let's calculate the time - 24 hours in seconds
            query = f"SELECT `symbol`, MIN(`price`), MIN(`last_update`) FROM `price_history_10m` WHERE `exchange_id` = {exchange_id} AND `last_update` BETWEEN {old_time} AND ({old_time} + 700) GROUP BY `symbol` ; "
            # print(query)
            cursor.execute(query)
            # print("Row count ", cursor.rowcount)
            result = [] if cursor.rowcount == 0 else cursor.fetchall()
            for row in result:
                crypto_price_old[row[0]] = float(row[1])

        with connector.connect(host=Setting.setting["host"], user=Setting.setting["user"],
                               passwd=Setting.setting["passwd"], db=Setting.setting["db"]) as db:
            cursor = db.cursor()
            for symbol in price:
                # Calculate the percentage change in price
                n_now = datetime.datetime.now()
                minute = f"{str(n_now.hour)}:{str(n_now.minute)}"
                if symbol[0] in crypto_price_old:
                    changes = price_difference(symbol[1], crypto_price_old[symbol[0]])
                else:
                    changes = 0
                harmonized_symbol = re.sub(r"_|-|//", "", symbol[0].replace(" ", ""))
                # This will clear the unread result from the cursor.
                query = (f"INSERT INTO `price` (`exchange_id`, `symbol`, `price`, `bid`,  `ask`,  `bidqty`, `askqty`, "
                         f"`volume`, `harmonized_symbol`) VALUES ({exchange_id}, '{symbol[0]}', {symbol[1]}, "
                         f"{symbol[2]}, {symbol[3]}, {symbol[4]}, {symbol[5]}, {symbol[6]}, "
                         f"'{harmonized_symbol}') ON DUPLICATE KEY UPDATE price = {symbol[1]}, `bid` = {symbol[2]}, "
                         f"`ask` = {symbol[3]},  `bidqty` = {symbol[4]}, `askqty` = {symbol[5]}, `volume` = "
                         f"{symbol[6]}, `prevDay` = {changes} ,last_update = CURRENT_TIMESTAMP;")

                # print(query)
                cursor.execute(query)  # Record the change in price
                db.commit()
    except Exception as e:
        logger.critical("Unknown error occurred 2", exc_info=True)


# Infinite loop for exchanges
def exchanges_loop():
    # Let's move the start back in time so that the first boot happens immediately
    start_time = round(time.time()) - Setting.setting["refreshTime"]

    while True:
        timer = start_time + Setting.setting["refreshTime"] - round(time.time())
        if timer <= 0:  # It's time to launch
            load_exchanges()
            Setting.setting['time_load'] = 0
            start_time = round(time.time())  # Let's reset the clock
        else:  # We'll wait another second.
            Setting.setting['time_load'] += 1
            time.sleep(1)


# Uploading exchanges
def load_exchanges():
    exchanges = Exchanges()
    if Setting.exchanges['Binance']['auto_start']:
        threading.Thread(target=exchanges.Binance).start()
    # if Setting.exchanges['Gate']['auto_start']:
    #     threading.Thread(target=exchanges.Gate).start()
    # if Setting.exchanges['Huobi']['auto_start']:
    #     threading.Thread(target=exchanges.Huobi).start()
    # if Setting.exchanges['KuCoin']['auto_start']:
    #     threading.Thread(target=exchanges.KuCoin).start()


def log(message: string, exchange_id: int):
    with connector.connect(host=Setting.setting["host"], user=Setting.setting["user"],
                           passwd=Setting.setting["passwd"], db=Setting.setting["db"]) as db:
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO `log` (`message`, `exchange_id`, `time_create`) VALUES ('{message}', {exchange_id}, CURRENT_TIMESTAMP);")
        db.commit()
    # print(message)


if __name__ == '__main__':
    # Let's start an infinite loop to run exchanges
    connectDB()
    # Start the web server to control the operation
    httpd = HTTPServer(('0.0.00', 8000), HTTPRequestHandler)
    # httpd.serve_forever()
    threading.Thread(target=exchanges_loop).start()
    threading.Thread(target=httpd.serve_forever)
