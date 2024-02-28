import datetime
import os

from dotenv import load_dotenv

from schedtrans.httpx_client.client import make_request
from httpx import Response

from schedtrans.telegram.common import save_file

load_dotenv()


class RequestSchedule:
    api_key: str | None = os.environ.get('YANDEX_API_KEY')
    search_url: str = 'search/'
    thread_url: str = 'thread/'
    nearest_stations_url: str = 'nearest_stations/'
    schedule_url: str = 'schedule/'
    date: str = datetime.datetime.now().isoformat()

    def __init__(
        self,
        transport_types: str = '',
        from_station: int = 0,
        to_station: int = 0,
        current_station: str = '',
        latitude: float = 0,
        longitude: float = 0,
        distance: int = 1,
        offset: int = 0,
        limit: int = 700,
        uid: str = '',
    ):
        self.transport_types: str = transport_types
        self.from_station: int = from_station
        self.to_station: int = to_station
        self.current_station: str = current_station
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.distance: int = distance
        self.offset: int = offset
        self.limit: int = limit
        self.uid: str = uid

    async def request_transport_between_stations(self) -> None:
        params: dict[str, str | int | None] = {
            'apikey': self.api_key,
            'transport_types': self.transport_types,
            'from': f's{self.from_station}',
            'to': f's{self.to_station}',
            'date': self.date,
            'limit': self.limit,
        }
        result = await make_request(self.search_url, params=params)
        save_file('route_between_stations.json', result.json())

    async def request_thread_transport_route(self) -> None:
        params: dict[str, str | int | None] = {
            'apikey': self.api_key,
            'uid': self.uid,
            'from': self.from_station,
            'to': self.to_station,
            'limit': self.limit,
        }
        result = await make_request(self.thread_url, params=params)
        save_file('threads.json', result.json())

    async def request_station_location(self) -> Response:
        params: dict[str, str | int | None] = {
            'apikey': self.api_key,
            'lat': self.latitude,
            'lng': self.longitude,
            'distance': self.distance,
            'limit': self.limit,
        }
        return await make_request(self.nearest_stations_url, params=params)

    async def request_flight_schedule_station(self) -> Response:
        params: dict[str, str | int | None] = {
            'apikey': self.api_key,
            'date': self.date,
            'station': self.current_station,
            'limit': self.limit,
        }
        return await make_request(self.schedule_url, params=params)
