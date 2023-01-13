# async-mm-v2

## Microsoft Monthly Patch Updates Report Creation
This package creates a spreadsheet, starting a report for the updates for a specified month with information from the Catalog, MSRC Security Center, WSUS Updates, and Office Updates.

Sources:

MSRC: https://msrc.microsoft.com/update-guide/deployments

Catalog: https://www.catalog.update.microsoft.com/Search.aspx?q=

KB894199: https://support.microsoft.com/help/894199

Office: https://learn.microsoft.com/en-us/officeupdates/office-updates-msi


### Guide:

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
