# Python interface for Australian BOM Weather API

Includes support for AsyncIO and returns populated objects with objects parsed
ready for use.

> **Disclaimer** This package is not associated with or endorsed by the Australian 
> Bureau of Meteorology (BOM). Usage may be subject to their term and conditions. 
> See the copyright notice published on their website for more information:
> http://reg.bom.gov.au/other/copyright.shtml

## Installation

```shell
# Pip
pip install bomapi

# Pipenv
pipenv install bomapi

# Poetry
poetry add bomapi
```

## Usage

### Find a location

```python
import bomapi

results = bomapi.location_search("Wollongong")
for result in results:
    print(result.name)
```

### Get data from a location

```python
import bomapi

geohash = "r3gk6rr"  # Wollongong (or use the result object from location_search)
location = bomapi.Location(geohash)

observations = location.observations()
print(observations.rain_since_9am)
```

### Async support

```python
import bomapi.aio

geohash = "r3gk6rr"  # Wollongong
location = bomapi.aio.Location(geohash)

observations = await location.observations()
print(observations.rain_since_9am)
```
