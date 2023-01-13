import src.mm.report as report
import asyncio


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
        print(kb.unique_products())
        print(kb.highest_severity())
    print(len(rep.kbs))


if __name__ == '__main__':
    asyncio.run(main())
