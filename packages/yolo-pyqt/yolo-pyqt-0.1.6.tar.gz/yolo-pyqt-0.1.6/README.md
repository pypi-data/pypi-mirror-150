# Introduction
yolo-pyqt provides an easy way to build automated quantitative trading systems for individual traders.

The main features are:
* Simple API interface for querying and trading stocks and implementations for Futu and IB based on
  [Futu Open API](https://openapi.futunn.com/futu-api-doc/en/) and [ib_insync](https://ib-insync.readthedocs.io/index.html)

# Installation
```shell
pip install yolo-pyqt
```

Requirements:
* Python 3.6 or higher;
* A running FutuOpenD application (version 5.9 or higher).
* A running TWS or IB Gateway application (version 1012 or higher).
  As for the configuration, please locate to Configuration/API/Settings, Make sure:
  * 'Read-only API' is not checked.
  * 'Download open orders on connection' is checked.
  * Set 'Socket port'
  * Set 'Master API client ID'

# Examples:
This is a complete script to get realtime prices for specified stock codes via IB API:
```python
from pyqt.api.impl.ib_api import IbAPI
import time

ib_api = IbAPI('127.0.0.1', 7496, 526)
ib_api.start()
for _ in range(5):
  data = ib_api.get_market_snapshot(['AAPL'])
  print('data=', data)
  time.sleep(1)
ib_api.stop()
```
Entire interface refers to [interface](https://github.com/TaoYang526/yolo-pyqt/blob/master/api/interface.py).
