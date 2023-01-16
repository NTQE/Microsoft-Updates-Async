# import src.mm.report as report
import asyncio
from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


async def main():
    rep = report.MonthlyReport(name='Monthly Report', year=2023, month=1)

    await rep.run()

    print(rep.get_deployment_api_url(skip=0))
    print(rep.get_vulnerability_api_url(skip=0))
    print(rep.get_affectedProduct_api_url(skip=0))
    print(report.get_misc_url())
    print(rep.get_office_url())

    for kb in rep.kbs:
        print(kb)
    print(len(rep.kbs))
