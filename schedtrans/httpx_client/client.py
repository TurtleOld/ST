import httpx


async def make_request(url, params):
    async with httpx.AsyncClient(
        base_url='https://api.rasp.yandex.net/v3.0/',
        http2=True,
        params=params,
        timeout=3,
    ) as client:
        return await client.get(f'/{url}')
