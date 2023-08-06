from datetime import datetime
from typing import NamedTuple, Mapping, Any, Optional

Data = Mapping[str, Any]

KPH_TO_KNOTS = 1.852


def _parse_date(date_string: str) -> datetime:
    if date_string:
        # Python doesn't parse Z correctly
        date_string = date_string.replace("Z", "+00:00")
        return datetime.fromisoformat(date_string)


class LocationResult(NamedTuple):
    """
    Result of a location search
    """

    id: str
    geohash: str
    state: str
    name: str
    postcode: str

    @classmethod
    def from_data(cls, data: Data) -> "LocationResult":
        return cls(
            data.get("id"),
            data.get("geohash"),
            data.get("state"),
            data.get("name"),
            data.get("postcode"),
        )


class LocationInfo(NamedTuple):
    """
    Information about a location
    """

    id: str
    geohash: str
    state: str
    name: str
    has_wave: bool
    latitude: float
    longitude: float
    marine_area_id: str
    tidal_point: str
    timezone: str

    @classmethod
    def from_data(cls, data: Data) -> "LocationInfo":
        return cls(
            data.get("id"),
            data.get("geohash"),
            data.get("state"),
            data.get("name"),
            data.get("has_wave"),
            data.get("latitude"),
            data.get("longitude"),
            data.get("marine_area_id"),
            data.get("tidal_point"),
            data.get("timezone"),
        )


class LocationWarning(NamedTuple):
    """
    Warning for a location
    """

    id: str
    geohash: str
    state: str
    type: str
    title: str
    short_title: str
    phase: str
    warning_group_type: str
    issue_time: datetime
    expiry_time: datetime

    @classmethod
    def from_data(cls, data: Data) -> "LocationWarning":
        return cls(
            data.get("id"),
            data.get("geohash"),
            data.get("state"),
            data.get("type"),
            data.get("title"),
            data.get("short_title"),
            data.get("phase"),
            data.get("warning_group_type"),
            _parse_date(data.get("issue_time")),
            _parse_date(data.get("expiry_time")),
        )


class Vector(NamedTuple):
    """
    Direction and speed in km/h
    """

    direction: str
    speed: int

    @classmethod
    def from_data(cls, data: Data) -> "Vector":
        return cls(
            data.get("direction"),
            data.get("speed_kilometre"),
        )


class WeatherStation(NamedTuple):
    """
    Description of a weather station
    """

    bom_id: str
    name: str
    distance: int

    @classmethod
    def from_data(cls, data: Data) -> "WeatherStation":
        return cls(
            data.get("bom_id"),
            data.get("name"),
            data.get("distance"),
        )


class Astronomical(NamedTuple):
    """
    Sun rise and set times
    """

    sunrise: datetime
    sunset: datetime

    @classmethod
    def from_data(cls, data: Data) -> "Astronomical":
        return cls(
            _parse_date(data.get("sunrise_time")),
            _parse_date(data.get("sunset_time")),
        )


class LocationObservation(NamedTuple):
    """
    Weather Observation
    """

    gust: int
    humidity: Optional[int]
    rain_since_9am: Optional[float]
    station: WeatherStation
    temp: float
    temp_feels_like: Optional[float]
    wind: Vector

    @classmethod
    def from_data(cls, data: Data) -> "LocationObservation":
        return cls(
            data.get("gust"),
            data.get("humidity"),
            data.get("rain_since_9am"),
            WeatherStation.from_data(data.get("station")),
            data.get("temp"),
            data.get("temp_feels_like"),
            Vector.from_data(data.get("wind")),
        )


class DailyForecastRain(NamedTuple):
    """
    Daily Rain forecast
    """

    min_amount: int
    max_amount: Optional[int]
    units: str
    chance: int
    percent_chance_25: int
    percent_chance_50: int
    percent_chance_75: int

    @classmethod
    def from_data(cls, data: Mapping[str, Any]) -> "DailyForecastRain":
        amount_data = data.get("amount", {})

        return cls(
            amount_data.get("min"),
            amount_data.get("max"),
            amount_data.get("units"),
            data.get("chance"),
            data.get("precipitation_amount_25_percent_chance"),
            data.get("precipitation_amount_50_percent_chance"),
            data.get("precipitation_amount_75_percent_chance"),
        )


class DailyForecastUV(NamedTuple):
    """
    Daily UV forecast
    """

    category: str
    max_index: int
    start_time: datetime
    end_time: datetime

    @classmethod
    def from_data(cls, data: Mapping[str, Any]) -> "DailyForecastUV":

        return cls(
            data.get("category"),
            data.get("max_index"),
            _parse_date(data.get("start_time")),
            _parse_date(data.get("end_time")),
        )


class DailyForecast(NamedTuple):
    """
    Daily forecast
    """

    date: datetime
    temp_min: Optional[int]
    temp_max: int
    short_text: str
    extended_text: str
    icon: str
    fire_danger: str
    rain: Any
    astronomical: Astronomical
    uv: Any

    @classmethod
    def from_data(cls, data: Mapping[str, Any]) -> "DailyForecast":
        return cls(
            _parse_date(data.get("date")),
            data.get("temp_min"),
            data.get("temp_max"),
            data.get("short_text"),
            data.get("extended_text"),
            data.get("icon_descriptor"),
            data.get("fire_danger"),
            DailyForecastRain.from_data(data.get("rain")),
            Astronomical.from_data(data.get("astronomical")),
            DailyForecastUV.from_data(data.get("uv")),
        )


class ThreeHourlyForcastRain(NamedTuple):
    """
    Three-hourly Rain forecast
    """

    min_amount: int
    max_amount: Optional[int]
    units: str
    chance: int

    @classmethod
    def from_data(cls, data: Mapping[str, Any]) -> "ThreeHourlyForcastRain":
        amount_data = data.get("amount", {})

        return cls(
            amount_data.get("min"),
            amount_data.get("max"),
            amount_data.get("units"),
            data.get("chance"),
        )


class ThreeHourlyForcast(NamedTuple):
    """
    Three-hourly forecast
    """

    time: datetime
    is_night: bool
    next_forecast: datetime
    temp: int
    icon: str
    rain: ThreeHourlyForcastRain
    wind: Vector

    @classmethod
    def from_data(cls, data: Mapping[str, Any]) -> "ThreeHourlyForcast":
        return cls(
            _parse_date(data.get("time")),
            data.get("is_night"),
            _parse_date(data.get("next_forecast_period")),
            data.get("temp"),
            data.get("icon_descriptor"),
            ThreeHourlyForcastRain.from_data(data.get("rain")),
            Vector.from_data(data.get("wind")),
        )
