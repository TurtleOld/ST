from blacksheep import Application, get

app = Application()


@get('/')
async def start():
    return {'ok': 'Home page...'}
