import asyncio
import src.mm.webreq as webreq
import aiohttp


async def gather_data(report):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(webreq.gather_deployment(session, report)),
                 asyncio.create_task(webreq.gather_ap(session, report)),
                 asyncio.create_task(webreq.gather_vulnerability(session, report)),
                 asyncio.create_task(webreq.gather_misc(session, report)),
                 asyncio.create_task(webreq.gather_office(session, report))]

        d, v, ap, m, o = await asyncio.gather(*tasks)
