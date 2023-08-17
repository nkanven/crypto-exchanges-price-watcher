import string
import threading
import time
from mysql import connector
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler  # Web server
from urllib.parse import urlparse, parse_qs  # Address bar processing
import shutil  # File access
import json  # Processing json


# An array of all our exchanges and their settings
class Setting:
    birzi = {
        "Binance": {
            "auto_start": True,  # Autoload start
            "count_load": 0,  # Number of downloads since the start
            "icon": "Binance.png",  # Icon
            "last_time": 0,  # Last successful download
            "number": 1,  # Exchange number in the database
            "log": ""  # Last message after uploading
        },
        "Gate": {
            "auto_start": True,
            "count_load": 0,
            "icon": "Gate.png",
            "last_time": 0,
            "number": 2,
            "log": ""
        },
        "Huobi": {
            "auto_start": True,
            "count_load": 0,
            "icon": "Huobi.png",
            "last_time": 0,
            "number": 3,
            "log": ""
        },
        "KuCoin": {
            "auto_start": True,
            "count_load": 0,
            "icon": "KuCoin.png",
            "last_time": 0,
            "number": 4,
            "log": ""
        }
    }

    # Array of settings
    setting = {
        "refreshTime": 180,  # Reloading time in seconds
        "host": "localhost",  # Host for MySQL
        "user": "root",  # MySQL login
        "passwd": "",  # MySQL password
        "db": "price",  # MySQL database
        "checkbox": {  # All CheckBoxes
            "history_1m": {  # System name
                "name": "Every minute, but no more than 24 hours",  # Title
                "act": False  # Status at start-up
            },
            "history_10m": {  # Системное имя
                "name": "Every 10 minutes, but no more than 24 hours.",  # Title
                "act": True  # Status at start-up
            },
            "history_1h": {  # Системное имя
                "name": "Every hour, but no more than 24 hours",  # Title
                "act": True  # Status at start-up
            },
            "history_1d": {  # System name
                "name": "Once a day, always.",  # Title
                "act": True  # Status at start-up
            }
        },
        "time_load": 0
    }


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
                return API.birzi(http)
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
        if (Setting.birzi[get_array['name'][0]]['auto_start']):
            Setting.birzi[get_array['name'][0]]['auto_start'] = False
        else:
            Setting.birzi[get_array['name'][0]]['auto_start'] = True
        # We'll send the new settings
        API.send_json(http, Setting.birzi)

    # List of exchanges
    def birzi(self, http):
        API.send_json(http, Setting.birzi)

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


class Birzi:
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
            for symbol in price_list:
                try:
                    if float(symbol['lastPrice']) > 0:  # Let's check the price availability
                        price.append([symbol['symbol'], symbol['lastPrice']])

                except Exception as inst:
                    print(inst)  # If there is an error accessing the result

            save_price(price, Setting.birzi['Binance']['number'])

            # Let's report on progress

            Setting.birzi['Binance']["count_load"] += 1
            Setting.birzi['Binance']["log"] = f"Downloaded Binance for {round(time.time() - time_start, 3)} sec."
            log(Setting.birzi['Binance']["log"], Setting.birzi['Binance']['number'])
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
                price.append([symbol['currency_pair'], symbol['last']])
            except Exception as inst:
                print(inst)  # If there is an error accessing the result

        save_price(price, Setting.birzi['Gate']['number'])

        Setting.birzi['Gate']["count_load"] += 1
        Setting.birzi['Gate']["log"] = f"Loading Gate for {round(time.time() - time_start, 3)} sec."
        log(Setting.birzi['Gate']["log"], Setting.birzi['Gate']['number'])

    # Downloading Huobi
    def Huobi(self):

        time_start = time.time()  # Let's remember the time of the strat

        # Let's get the data with prices from the link.
        price_list = requests.get(
            "https://api.huobi.pro/market/tickers").json()  # We will get the answer in JSON format

        price = []
        # Let's loop through all trading pairs
        for symbol in price_list['data']:
            price.append([symbol['symbol'], symbol['close']])

        save_price(price, Setting.birzi['Huobi']['number'])

        # Let's report on progress
        Setting.birzi['Huobi']["count_load"] += 1
        Setting.birzi['Huobi']["log"] = f"Loading Huobi for{round(time.time() - time_start, 3)} Sec."
        log(Setting.birzi['Huobi']["log"], Setting.birzi['Huobi']['number'])

    # Loading KuCoin
    def KuCoin(self):

        time_start = time.time()  # Let's remember the time of the strat

        # Let's get the data with prices from the link.
        price_list = requests.get(
            "https://api.kucoin.com/api/v1/market/allTickers").json()  # We will get the answer in JSON format

        price = []
        # Let's loop through all trading pairs
        for symbol in price_list['data']['ticker']:
            price.append([symbol['symbol'], symbol['last']])

        save_price(price, Setting.birzi['KuCoin']['number'])
        # Let's report on progress
        Setting.birzi['KuCoin']["count_load"] += 1
        Setting.birzi['KuCoin']["log"] = f"Loading KuCoin for{round(time.time() - time_start, 3)} Sec."
        log(Setting.birzi['KuCoin']["log"], Setting.birzi['KuCoin']['number'])


# Database connection
def connectDB():
    return connector.connect(host=Setting.setting["host"], user=Setting.setting["user"], passwd=Setting.setting["passwd"],
                           db=Setting.setting["db"])


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
def save_price(price: list, birza: int):
    # Let's connect to the database
    conn = connectDB()
    cursor = conn.cursor()

    # Let's create an array with old prices to calculate the price change for 24 hours
    old_time = round(time.time()) - 86400 + 600  # Let's calculate the time - 24 hours in seconds
    cursor.execute(
        f"SELECT `symbol`, `price`, MIN(`last_update`) FROM `price_history_10m` WHERE `birza` = {birza} AND `last_update` BETWEEN {old_time} AND ({old_time} + 700) GROUP BY `symbol` ; ")
    result = cursor.fetchall()
    crypto_price_old = {}
    for row in result:
        crypto_price_old[row[0]] = float(row[1])

    for symbol in price:
        # Calculate the percentage change in price
        if symbol[0] in crypto_price_old:
            changes = price_difference(symbol[1], crypto_price_old[symbol[0]])
        else:
            changes = 0

        cursor.execute(
            f"INSERT INTO `price` (`birza`, `symbol`, `price`) VALUES ({birza}, '{symbol[0]}', '{symbol[1]}') ON DUPLICATE KEY UPDATE price = '{symbol[1]}' , `prevDay` = {changes} ,last_update = UNIX_TIMESTAMP();")  # Record the change in price

        if (Setting.setting["checkbox"]["history_1h"]["act"]):
            cursor.execute(
                f"INSERT INTO `price_history_1h` (`birza`, `symbol`, `price`) VALUES ({birza}, '{symbol[0]}', {symbol[1]}) ON DUPLICATE KEY UPDATE price = {symbol[1]} , last_update = UNIX_TIMESTAMP();")
        if (Setting.setting["checkbox"]["history_1d"]["act"]):
            cursor.execute(
                f"INSERT INTO `price_history_1d` (`birza`, `symbol`, `date_day`, `price`) VALUES ({birza}, '{symbol[0]}', now(), {symbol[1]}) ON DUPLICATE KEY UPDATE price = {symbol[1]} ;")
        if (Setting.setting["checkbox"]["history_10m"]["act"]):
            cursor.execute(
                f"INSERT INTO `price_history_10m` (`birza`, `symbol`, `minut`, `price`) VALUES ({birza}, '{symbol[0]}', concat(SUBSTRING(date_format(now(),'%H:%i'),1,4), '0'), {symbol[1]}) ON DUPLICATE KEY UPDATE price = {symbol[1]} , last_update = UNIX_TIMESTAMP();")
        if (Setting.setting["checkbox"]["history_1m"]["act"]):
            cursor.execute(
                f"INSERT INTO `price_history_1m` (`birza`, `symbol`, `minut`, `price`) VALUES ({birza}, '{symbol[0]}', date_format(current_timestamp(),'%H:%i'), {symbol[1]}) ON DUPLICATE KEY UPDATE price = {symbol[1]} , last_update = UNIX_TIMESTAMP();")

    conn.commit()
    conn.close()


# Infinite loop for exchanges
def while_Birzi():
    # Let's move the start back in time so that the first boot happens immediately
    start_time = round(time.time()) - Setting.setting["refreshTime"]

    while True:
        timer = start_time + Setting.setting["refreshTime"] - round(time.time())
        if timer <= 0:  # It's time to launch
            loadAllBirzi()
            Setting.setting['time_load'] = 0
            start_time = round(time.time())  # Let's reset the clock
        else:  # We'll wait another second.
            Setting.setting['time_load'] += 1
            time.sleep(1)


# Uploading exchanges
def loadAllBirzi():
    exchanges = Birzi()
    if Setting.birzi['Binance']['auto_start']:
        threading.Thread(target=exchanges.Binance).start()
    # if Setting.birzi['Gate']['auto_start']:
    #     threading.Thread(target=Birzi.Gate).start()
    # if Setting.birzi['Huobi']['auto_start']:
    #     threading.Thread(target=Birzi.Huobi).start()
    # if Setting.birzi['KuCoin']['auto_start']:
    #     threading.Thread(target=Birzi.KuCoin).start()


def log(message: string, birza: int):
    # conn = connectDB()
    # cursor = conn.cursor()
    # cursor.execute(f"INSERT INTO `log` (`message`, `birza`, `time_create`) VALUES ('{message}', {birza}, UNIX_TIMESTAMP());")
    # conn.commit()
    # conn.close()
    print(message)


if __name__ == '__main__':
    # Let's start an infinite loop to run exchanges
    threading.Thread(target=while_Birzi).start()

    # Start the web server to control the operation
    httpd = HTTPServer(('', 8000), HTTPRequestHandler)
    httpd.serve_forever()
