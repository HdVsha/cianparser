import cianparser.cianparser

import asyncio


async def main():
    await cianparser.parse(accommodation="flat", location="Москва", rooms="all", start_page=1, end_page=5, deal_type="sale")
    # await cianparser.parse(accommodation="flat", location="Москвоская область", rooms="all", start_page=1, end_page=1, deal_type="rent_long")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
