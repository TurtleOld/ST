from datetime import timedelta, datetime, timezone
from schedtrans.json_parser.json_parse import JsonParser
from schedtrans.json_request.request import RequestSchedule


def convert_time(seconds: str | float) -> str:
    minutes = int(seconds) // 60
    if minutes >= 60:
        return f'{int(minutes // 60)} час {int(minutes % 60)} мин.'
    return f'{int(minutes)} мин.'


class Processing:

    count_results = 0
    parser = JsonParser()
    result_json_route = {}

    def __init__(self, json_data=None):
        if json_data is None:
            json_data = {}
        self.json_data = json_data

    async def detail_route(self) -> None:
        segments = self.parser.parse_json(self.json_data, 'segments')
        utc_offset = timedelta(hours=3)
        current_time = timezone(utc_offset)
        current_datetime = datetime.now(current_time)
        if segments:
            for segment in segments:
                departure = self.parser.parse_json(segment, 'departure')
                date_departure = datetime.strptime(
                    str(departure),
                    '%Y-%m-%dT%H:%M:%S%z',
                )
                if date_departure > current_datetime:
                    from_station = self.parser.parse_json(segment, 'from')
                    to_station = self.parser.parse_json(segment, 'to')
                    transport_type = self.parser.parse_json(
                        segment,
                        'thread',
                        'transport_type',
                    )
                    arrival = self.parser.parse_json(segment, 'arrival')
                    date_arrival = datetime.strptime(
                        str(arrival),
                        '%Y-%m-%dT%H:%M:%S%z',
                    )
                    departure_format_date = date_departure.strftime('%H:%M')
                    arrival_format_date = date_arrival.strftime('%H:%M')
                    number = self.parser.parse_json(
                        segment,
                        'thread',
                        'number',
                    )
                    short_title = self.parser.parse_json(
                        segment,
                        'thread',
                        'short_title',
                    )
                    uid_thread = self.parser.parse_json(
                        segment,
                        'thread',
                        'uid',
                    )
                    duration = convert_time(
                        self.parser.parse_json(segment, 'duration'),
                    )
                    stops = self.parser.parse_json(segment, 'stops')

                    self.result_json_route[uid_thread] = {
                        'transport_type': transport_type,
                        'from_station': from_station,
                        'to_station': to_station,
                        'departure_format_date': departure_format_date,
                        'arrival_format_date': arrival_format_date,
                        'number': number,
                        'short_title': short_title,
                        'duration': duration,
                        'stops': stops,
                    }
                    self.count_results += 1
                    if self.count_results >= 10:
                        break
            await self.detail_thread()

    async def detail_thread(self):
        result = self.result_json_route
        for key, value in result.items():
            uid = key
            code_from_station = self.parser.parse_json(
                value,
                'from_station',
                'code',
            )
            code_to_station = self.parser.parse_json(
                value,
                'to_station',
                'code',
            )
            request = RequestSchedule(
                uid=uid,
                from_station=code_from_station,
                to_station=code_to_station,
            )
            threads = await request.request_thread_transport_route()
            days = self.parser.parse_json(threads.json(), 'days')
            self.result_json_route[uid]['days'] = days
        return self.result_json_route
