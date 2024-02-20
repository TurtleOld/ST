import asyncio

from schedtrans.telegram.commands import start_bot


def main():
    asyncio.run(start_bot())


if __name__ == '__main__':
    main()
