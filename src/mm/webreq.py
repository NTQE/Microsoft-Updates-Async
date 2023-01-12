from src.mm.models.deployment import DeploymentResponse, Deployment
from src.mm.models.vulnerability import VulnerabilityResponse, Vulnerability
from src.mm.models.affectedProduct import AffectedProductResponse, AffectedProduct
import aiohttp
import asyncio
from bs4 import BeautifulSoup as bs
import re


async def gather_deployment(session: aiohttp.ClientSession, rep):
    url = rep.get_deployment_api_url(skip=0)
    async with session.get(url) as response:
        json = await response.json()
        resp = DeploymentResponse(**json)
        resp_list = resp.value
        if int(resp.count) > len(resp_list):
            pages = [x*len(resp.value) for x in [*range(1, (int(resp.count)//len(resp.value) + 1))]]
            for page in pages:
                async with session.get(rep.get_deployment_api_url(skip=page)) as p:
                    json = await p.json()
                    resp_list.extend(DeploymentResponse(**json).value)
        rep.deployments = resp_list


async def gather_ap(session: aiohttp.ClientSession, rep):
    url = rep.get_affectedProduct_api_url(skip=0)
    async with session.get(url) as response:
        json = await response.json()
        resp = AffectedProductResponse(**json)
        resp_list = resp.value
        if int(resp.count) > len(resp_list):
            pages = [x*len(resp.value) for x in [*range(1, (int(resp.count)//len(resp.value) + 1))]]
            for page in pages:
                async with session.get(rep.get_affectedProduct_api_url(skip=page)) as p:
                    json = await p.json()
                    resp_list.extend(AffectedProductResponse(**json).value)
        rep.aps = resp_list


async def gather_vulnerability(session: aiohttp.ClientSession, rep):
    url = rep.get_vulnerability_api_url(skip=0)
    async with session.get(url) as response:
        json = await response.json()
        resp = VulnerabilityResponse(**json)
        resp_list = resp.value
        if int(resp.count) > len(resp_list):
            pages = [x*len(resp.value) for x in [*range(1, (int(resp.count)//len(resp.value) + 1))]]
            for page in pages:
                async with session.get(rep.get_vulnerability_api_url(skip=page)) as p:
                    json = await p.json()
                    resp_list.extend(VulnerabilityResponse(**json).value)
        rep.vulnerabilities = resp_list


async def gather_misc(session: aiohttp.ClientSession, rep) -> list[Vulnerability]:
    url = rep.get_misc_url()


async def gather_office(session: aiohttp.ClientSession, rep) -> list[Vulnerability]:
    url = rep.get_office_url()
