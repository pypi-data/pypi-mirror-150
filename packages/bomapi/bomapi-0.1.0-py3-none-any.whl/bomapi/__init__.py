"""
Python interface for the Australia BOM Weather API.

The official website is `https://weather.bom.gov.au/`_
"""
from http import HTTPStatus
from typing import Sequence, Union, Mapping

import httpx

from .data_structures import (
    DailyForecast,
    LocationObservation,
    LocationWarning,
    LocationInfo,
    LocationResult,
    ThreeHourlyForcast,
)
from .exceptions import ResultError, ResultNotFound

API_BASE_URL = "https://api.weather.bom.gov.au/v1"


def _make_request(url_path: str, *, params: Mapping[str, str] = None):
    response = httpx.get(f"{API_BASE_URL}{url_path}", params=params)
    if response.status_code == HTTPStatus.OK:
        return response.json().get("data")

    if response.status_code == HTTPStatus.BAD_REQUEST:
        raise ResultNotFound("Requested item not found", response)

    else:
        raise ResultError("Request returned an error", response)


LocationValue = Union[str, LocationResult]


def location_search(search: str) -> Sequence[LocationResult]:
    """
    Search the location API to for a weather location
    """
    if not search:
        # Catch an empty string that would cause a 403 (bit odd)
        return []

    data = _make_request(f"/locations", params={"search": search})
    return [LocationResult.from_data(item) for item in data]


class Location:
    def __init__(self, location: LocationValue):
        self.geohash = (
            location.geohash if isinstance(location, LocationResult) else location
        )

    def info(self) -> LocationInfo:
        """
        Get information about a location.

        Can accept either a geohash value or a LocationResult instance.
        """

        data = _make_request(f"/locations/{self.geohash}")
        return LocationInfo.from_data(data)

    def warnings(self) -> Sequence[LocationWarning]:
        """
        Identify warnings for the specified location
        """
        data = _make_request(f"/locations/{self.geohash}/warnings")
        return [LocationWarning.from_data(item) for item in data]

    def observations(self) -> LocationObservation:
        """
        Get observations made at the specified location
        """
        data = _make_request(f"/locations/{self.geohash[:6]}/observations")
        return LocationObservation.from_data(data)

    def forcast_daily(self) -> Sequence[DailyForecast]:
        """
        Daily forecast for the next seven days
        """

        data = _make_request(f"/locations/{self.geohash[:6]}/forecasts/daily")
        return [DailyForecast.from_data(item) for item in data]

    def forcast_3_hourly(self) -> Sequence[ThreeHourlyForcast]:
        """
        Three-hourly forecast for the next two days
        """

        data = _make_request(f"/locations/{self.geohash[:6]}/forecasts/3-hourly")
        return [ThreeHourlyForcast.from_data(item) for item in data]
