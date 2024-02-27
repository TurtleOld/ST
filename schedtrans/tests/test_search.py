import json
import pathlib

from schedtrans.prepare_data.process_data_generate import Processing


async def test_search_dict():
    file = pathlib.Path('schedtrans/tests/fixtures/search.json')
    with open(file) as f:
        json_data = json.loads(f.read())
    assert isinstance(json_data, dict)

    process_json_data = Processing(json_data)
    await process_json_data.detail_route()
    thread_json_data = await process_json_data.detail_thread()
    print(thread_json_data)
