from pydantic import BaseModel, Field
import src.mm.logic as logic
from src.mm.models.deployment import Deployment
from src.mm.models.affectedProduct import AffectedProduct
from src.mm.models.vulnerability import Vulnerability
import calendar


def get_second_tuesday_string(y: int, m: int) -> str:
    """Get a string representation for the chosen second Tuesday

    :param y: year
    :param m: month
    :return: string in form -> 'Tuesday, Month dd, yyyy'
    """
    c = calendar.Calendar()
    # d[3] == 1 means the 4th value in the d tuple should match 1, which is Tuesday
    # d[1] == month means the second value in the d tuple should match month
    # ending [1] means the second value in the returned list, which is the second Tuesday date tuple
    second = list(filter(lambda d: d[3] == 1 and d[1] == m, c.itermonthdays4(y, m)))[1]
    months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
              9: "September", 10: "October", 11: "November", 12: "December"}
    return f"Tuesday, {months[m]} {second[2]}, {y}"


def get_second_tuesday_date(y: int, m: int, delta: int) -> str:
    """Get a string representation for the chosen second Tuesday

    :param y: year
    :param m: month
    :param delta: days before(-) or after(+) the second tuesday
    :return: string in form -> 'yyyy-mm-dd'
    """
    c = calendar.Calendar()
    # d[3] == 1 means the 4th value in the d tuple should match 1, which is Tuesday
    # d[1] == month means the second value in the d tuple should match month
    # ending [1] means the second value in the returned list, which is the second Tuesday date tuple
    second = list(filter(lambda d: d[3] == 1 and d[1] == m, c.itermonthdays4(y, m)))[1]
    return f"{second[0]}-{second[1]:02d}-{second[2]+delta:02d}"


class Source(BaseModel):
    pass


class MonthlyReport(BaseModel):
    name: str
    year: int
    month: int
    misc_html: str = ""
    office_html: str = ""
    deployments: list[Deployment] = Field(default_factory=list)
    aps: list[AffectedProduct] = Field(default_factory=list)
    vulnerabilities: list[Vulnerability] = Field(default_factory=list)
    unique_kb_count: int = Field(default=0)
    msrc_updates: int = Field(default=0)
    misc_updates: int = Field(default=0)
    office_updates: int = Field(default=0)
    msrc_cve: int = Field(default=0)

    @property
    def patch_day(self) -> str:
        return get_second_tuesday_string(self.year, self.month)

    @property
    def start(self):
        if self.month == 1:
            month = 12
            year = self.year - 1
        else:
            month = self.month
            year = self.year
        return f"{get_second_tuesday_date(year, month, 1)}"

    @property
    def start_encoded(self):
        return f"{self.start}T00%3A00%3A00-06%3A00"

    @property
    def end(self):
        return f"{get_second_tuesday_date(self.year, self.month, 2)}"

    @property
    def end_encoded(self):
        return f"{self.end}T23%3A59%3A59-06%3A00"

    @property
    def sources(self):
        sources = Source(start=self.start, end=self.end)


    def get_vulnerability_api_url(self, skip: int) -> str:
        return f"https://api.msrc.microsoft.com/sug/v2.0/en-US/vulnerability?%24orderBy=cveNumber+asc&%24filter=%28releaseDate+gt+{self.start}T00%3A00%3A00-05%3A00+or+latestRevisionDate+gt+{self.start}T00%3A00%3A00-05%3A00%29+and+%28releaseDate+lt+{self.end}T23%3A59%3A59-05%3A00+or+latestRevisionDate+lt+{self.end}T23%3A59%3A59-05%3A00%29&$skip={str(skip)}"

    def get_affectedProduct_api_url(self, skip: int) -> str:
        return f"https://api.msrc.microsoft.com/sug/v2.0/en-US/affectedProduct?%24orderBy=releaseDate+desc&%24filter=%28releaseDate+gt+{self.start}T00%3A00%3A00-05%3A00%29+and+%28releaseDate+lt+{self.end}T23%3A59%3A59-05%3A00%29&$skip={str(skip)}"

    def get_deployment_api_url(self, skip: int) -> str:
        return f"https://api.msrc.microsoft.com/sug/v2.0/en-US/deployment/?%24orderBy=product+desc&%24filter=%28releaseDate+gt+{self.start}T00%3A00%3A00-06%3A00%29+and+%28releaseDate+lt+{self.end}T23%3A59%3A59-06%3A00%29&$skip={str(skip)}"

    def get_specific_deployment_by_article(self, articleName: str):
        return f"https://api.msrc.microsoft.com/sug/v2.0/en-US/deployment/?%24orderBy=product+desc&%24filter=articleName+eq+%27{articleName}%27"

    def get_specific_ap_by_cve(self, cveNumber: str):
        return f"https://api.msrc.microsoft.com/sug/v2.0/en-US/affectedProduct?%24filter=cveNumber+eq+%27{cveNumber}%27"

    def get_specific_ap_by_id(self, ap_id: str):
        return f"https://api.msrc.microsoft.com/sug/v2.0/en-US/affectedProduct/{ap_id}"

    def get_specific_vuln_by_cve(self, cveNumber: str):
        return f"https://api.msrc.microsoft.com/sug/v2.0/en-US/vulnerability?%24orderBy=cveNumber+desc&%24filter=cveNumber+eq+%27{cveNumber}%27"

    def get_office_url(self) -> str:
        # "https://docs.microsoft.com/en-us/officeupdates/office-updates-msi"
        y = int(self.end[0:4])
        m = int(self.end[5:7])
        kb_dict = {
            1: "5002084",
            2: "5002085",
            3: "5002086",
            4: "5002087",
            5: "5002088",
            6: "5002089",
            7: "5002090",
            8: "5002091",
            9: "5002092",
            10: "5002093",
            11: "5002094",
            12: "5002095",
        }
        base_url = "https://support.microsoft.com/help/"
        if y == 2023:
            if 13 > m > 0:
                return f'{base_url}{kb_dict[m]}'
        else:
            print('Not the right year.')
            return ""

    def get_misc_url(self) -> str:
        return "https://support.microsoft.com/help/894199"

    def get_catalog_url(self, articleName: str) -> str:
        # include "KB" letters in the search
        return f"https://www.catalog.update.microsoft.com/Search.aspx?q=KB{articleName}"

    def get_catalog_inline_url(self, update_id: str) -> str:
        # "https://www.catalog.update.microsoft.com/ScopedViewInline.aspx?updateid=" + id + "#PackageDetails"
        return f"https://www.catalog.update.microsoft.com/ScopedViewInline.aspx?updateid={update_id}#PackageDetails"

    async def run(self):
        print(f"Starting: {self.name}")
        print(f"Patch Tuesday: {self.patch_day}")
        print("Report Range:")
        print(self.start, "to", self.end)
        data = await logic.gather_data(self)
