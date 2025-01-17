# GFZ Helmholtz Centre for Geosciences Web Service API Client

## Description

Unofficial client for **Helmholtz Centre for Geosciences Web Service API**. For getting Geomagnetic Index (Kp, etc) 
Nowcast and Forecast data (https://spaceweather.gfz-potsdam.de/products-data/forecasts/forecast-kp-index). 
Kp is an important measure for the energy input from the solar wind to Earth and it is used by space weather services in near real-time. 
The geomagnetic Hpo index is a Kp-like index with a time resolution of half an hour, called Hp30, and one hour, called Hp60.

Official API description : https://kp.gfz-potsdam.de/en/data

Library provides Classic and Asynchronous client classes for using in python applications.

## Features:
- Getting geomagnetic index forecast (as a Dict)
- Getting geomagnetic three-hourly index for period (as a Dict)
- Getting geomagnetic three-hourly index for period as a Tuple (like official client by GFZ German Research Centre for Geosciences)

## Classes

### GFZClient

Classic client class for Web Service API

### GFZAsyncClient

Asynchronous client class for Web Service API

## Methods

### get_forecast(index)

Returns Dict with Index prediction dataset. 
Parameter `index` define index for data request. Should be in `('Kp','Hp30', 'Hp30')`

### get_nowcast(start_time, end_time, index, [data_state])

Returns Dict with geomagnetic three-hourly Index for period. 
Parameters `start_time` and `end_time` defines time period. Both should be string with UTC date/time, format: `'YYYY-MM-DD'` or `'YYYY-MM-DDThh:mm:ss'`
Parameter `index` define index for data request. Should be in `('Kp', 'ap', 'Ap', 'Cp', 'C9', 'Hp30', 'Hp60', 'ap30', 'ap60', 'SN', 'Fobs', 'Fadj')`
Optional Parameter `data_state` define index state. Possible values: `'def', 'all'`. Output of definitive values only (only for **Kp, ap, Ap, Cp, C9, SN**) 

### get_kp_index(starttime, endtime, index, [status])

Returns tuple with geomagnetic three-hourly Index for period or `(0, 0, 0)` in an Error case. 
Parameters `starttime` and `endtime` defines time period. Both should be string with UTC date/time, format: `'YYYY-MM-DD'` or `'YYYY-MM-DDThh:mm:ss'`
Parameter `index` define index for data request. Should be in `('Kp', 'ap', 'Ap', 'Cp', 'C9', 'Hp30', 'Hp60', 'ap30', 'ap60', 'SN', 'Fobs', 'Fadj')`
Optional Parameter `status` define index state. Possible values: `'def', 'all'`. Output of definitive values only (only for **Kp, ap, Ap, Cp, C9, SN**)

Method **get_kp_index** implements getKpindex method from official python client with same behaviour and added for compatibility purposes

## How to use

### Installation

```shell
pip install gfz-api-client
```

### Classic client

```python
from gfz_client import GFZClient

client = GFZClient()

# Get geomagnetic index forecast
data = client.get_forecast(index="Kp")

# Get geomagnetic three-hourly Kp index for period
data = client.get_nowcast(start_time="2011-11-04T00:05:23", end_time="2011-11-04T00:05:23", index="Kp")

# Get geomagnetic three-hourly Kp index for period as a tuple
data = client.get_kp_index(starttime="2011-11-04T00:05:23Z", endtime="2011-11-04T00:05:23Z", index="Kp")

```

### Asynchronous client

```python
from gfz_client import GFZAsyncClient

client = GFZAsyncClient()

# Get geomagnetic index forecast
data = await client.get_forecast(index="Kp")

# Get geomagnetic three-hourly Kp index for period
data = await client.get_nowcast(start_time="2011-11-04T00:05:23Z", end_time="2011-11-04T00:05:23Z", index="Kp")

# Get geomagnetic three-hourly Kp index for period as a tuple
data = await client.get_kp_index(starttime="2011-11-04T00:05:23", endtime="2011-11-04T00:05:23", index="Kp")

```
