from datetime import timedelta, datetime, timezone
from typing import Any
from schedtrans.json_parser.json_parse import JsonParser
from schedtrans.json_request.request import RequestSchedule
from schedtrans.logger.log import logger
from schedtrans.telegram.common import open_file, save_file


@logger.catch
def convert_time(seconds: str | float) -> str:
    minutes = int(seconds) // 60
    if minutes >= 60:
        return f'{int(minutes // 60)} час {int(minutes % 60)} мин.'
    return f'{int(minutes)} мин.'


@logger.catch
async def detail_route(json_data) -> dict[Any, dict[str, str | Any]] | None:
    parser = JsonParser()
    count_results = 0
    result_json_route = {}
    segments = parser.parse_json(json_data, 'segments')
    utc_offset = timedelta(hours=3)
    current_time = timezone(utc_offset)
    current_datetime = datetime.now(current_time)
    if segments:
        for segment in segments:
            departure = parser.parse_json(segment, 'departure')
            date_departure = datetime.strptime(
                str(departure),
                '%Y-%m-%dT%H:%M:%S%z',
            )
            if date_departure > current_datetime:
                from_station = parser.parse_json(segment, 'from')
                to_station = parser.parse_json(segment, 'to')
                transport_type = parser.parse_json(
                    segment,
                    'thread',
                    'transport_type',
                )
                arrival = parser.parse_json(segment, 'arrival')
                date_arrival = datetime.strptime(
                    str(arrival),
                    '%Y-%m-%dT%H:%M:%S%z',
                )
                departure_format_date = date_departure.strftime('%H:%M')
                arrival_format_date = date_arrival.strftime('%H:%M')
                number = parser.parse_json(
                    segment,
                    'thread',
                    'number',
                )
                short_title = parser.parse_json(
                    segment,
                    'thread',
                    'short_title',
                )
                uid_thread = parser.parse_json(
                    segment,
                    'thread',
                    'uid',
                )
                duration = convert_time(
                    parser.parse_json(segment, 'duration'),
                )
                stops = parser.parse_json(segment, 'stops')

                result_json_route[uid_thread] = {
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
                count_results += 1
                if count_results >= 10:
                    break
        save_file('result_transport_route.json', result_json_route)
        await detail_thread()
    else:
        return None


@logger.catch
async def detail_thread():
    parser = JsonParser()
    result = open_file('result_transport_route.json')
    print(result, 'detail_thread_result_transport_route.json')
    for key, value in result.items():
        uid = key
        code_from_station = parser.parse_json(
            value,
            'from_station',
            'code',
        )
        code_to_station = parser.parse_json(
            value,
            'to_station',
            'code',
        )
        request = RequestSchedule(
            uid=uid,
            from_station=code_from_station,
            to_station=code_to_station,
        )
        await request.request_thread_transport_route()
        threads = open_file('threads.json')
        print(threads)
        days = parser.parse_json(threads, 'days')
        result[uid]['days'] = days
    print(result, 'result')
    save_file('result_transport_route.json', result)


@logger.catch
async def get_schedule_route(json_data):
    await detail_route(json_data)
    return open_file('result_transport_route.json')
