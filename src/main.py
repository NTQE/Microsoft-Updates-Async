from src.mm.models.report import MonthlyReport
import asyncio


async def main():
    report = MonthlyReport(name='Monthly Report', year=2023, month=1)

    task = await report.run()

    print(report.get_deployment_api_url(skip=0))
    print(report.get_vulnerability_api_url(skip=0))
    print(report.get_affectedProduct_api_url(skip=0))
    print(report.get_misc_url())
    print(report.get_office_url())

    print(len(report.deployments))


if __name__ == '__main__':
    asyncio.run(main())
