Ready code for downloading prices from 4 exchanges
- Binance
- Gate
- Huobi
- KuCoin
<br>
Where to start:<br>
1. Create a database from the price.sql file<br>
2. Make changes to the settings<br>
3. Install components to run Python<br>

```CMD
pip install mysqlclient
pip install requests
```

Customisation :
```Python
    # Array of settings
    setting = {
        "refreshTime":180, # Reloading time in seconds
        "host":"localhost", # Host for MySQL
        "user":"root", # MySQL login
        "passwd":"", # MySQL password
        "db":"price", # MySQL database
        "checkbox": { # All CheckBoxes
            "history_1m": { # System name
                "name": "Every minute but not more than twenty-four hours", # Title
                "act" : False # Status at start-up
            },
            "history_10m": { # System name
                "name": "Every 10 minutes but not more than 24 hours", # Title
                "act" : True # Status at start-up
            },
            "history_1h": { # System name
                "name": "Every hour but not more than twenty-four hours", # Title
                "act" : True # Status at start-up
            },
            "history_1d": { # System name
                "name": "Once a day, always," # Title
                "act" : True # Status at start-up
            }
        },
        "time_load": 0
    }
```

Configuring boot autorun
```Python
   birzi = {
        "Binance": {
            "auto_start":True, # Auto load start
            "count_load":0, # Number of downloads since the start
            "icon":"Binance.png", # Icon
            "last_time":0, # Last successful download
            "number":1, # Exchange number in the database
            "log":"" # Last message after uploading
            },
        "Gate": {
            "auto_start":True,
            "count_load":0,
            "icon":"Gate.png",
            "last_time":0,
            "number":2,
            "log":""
            },
        "Huobi": {
            "auto_start":True,
            "count_load":0,
            "icon":"Huobi.png",
            "last_time":0,
            "number":3,
            "log":""
            },
        "KuCoin": {
            "auto_start":True,
            "count_load":0,
            "icon":"KuCoin.png",
            "last_time":0,
            "number":4,
            "log":""
            }
    }
```
