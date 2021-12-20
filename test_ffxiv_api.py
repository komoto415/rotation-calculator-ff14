from bs4 import BeautifulSoup
import asyncio
import logging

import aiohttp
import pyxivapi
from pyxivapi.models import Filter, Sort


async def fetch_example_results():
    client = pyxivapi.XIVAPIClient(api_key="633ad07d4bda4ce8804eb679ec3159a87c1765f6e141422980abf268c30f0691")

    # Search Lodestone for a character
    character = await client.character_search(
        world="faerie",
        forename="jinn",
        surname="wayland"
    )
    # # Get an item by its ID (Omega Rod) and return the data in German
    # item = await client.index_by_id(
    #     index="Item",
    #     content_id=23575,
    #     columns=["ID", "Name", "Icon", "ItemUICategory.Name"],
    #     language="de"
    # )
    #
    # filters = [
    #     Filter("ClassJobLevel", "gte", 0)
    # ]
    #

    # print(character)

    action = await client.index_search(
        name="Clemency",
        indexes=["Action"],
        columns=["ID", "Description"],
        string_algo="match"
    )

    print(action["Results"][0])



    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    html = action["Results"][0]["Description"]
    soup = BeautifulSoup(html,features="lxml")
    print(soup.get_text())
    await client.session.close()
if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='%H:%M')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_example_results())

