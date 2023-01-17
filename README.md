# async-mm-v2

## Microsoft Monthly Patch Updates Report Creation
This package creates a spreadsheet, starting a report for the updates for a specified month with information from the Catalog, MSRC Security Center, WSUS Updates, and Office Updates.

Sources:

MSRC: https://msrc.microsoft.com/update-guide/deployments

Catalog: https://www.catalog.update.microsoft.com/Search.aspx?q=

KB894199: https://support.microsoft.com/help/894199

Office: https://learn.microsoft.com/en-us/officeupdates/office-updates-msi


### Docker Guide:

Download and install Docker.

Download the async-mm-v2 directory and `cd` into the folder.

Run these commands:

`docker build -t async-mm-fastapi-v2 .`

`docker run -d --name mm-fast -p 80:80 async-mm-fastapi-v2`

Check your Docker containers and ensure it is running properly.

Head to http://localhost:80 and check for the json response.

Head to http://localhost:80/report/year={year}+month={month}+name={name}, replacing `{year}` with `2023`, `{month}` with `1` and `{name}` with `report` if you want to download the Report for January 2023.





### Manual Guide:

Create a `main.py` file.

Import the required modules: `import src.mm.report as report` and `import asyncio`

Install the the packages from `requirements.txt`

As seen in the example `main.py` file, create an asynchronous main function and run it with `asyncio.run(main())`

Create the Report, and then run it:

`rep = report.MonthlyReport(name='Monthly Report', year=2023, month=1)`

`await rep.run()`

Everything else happens automatically and creates an .xlsx spreadsheet in the `mm` directory with the name "NAME_YYYY-DD"

### Notes:

Created with Python 3.11
