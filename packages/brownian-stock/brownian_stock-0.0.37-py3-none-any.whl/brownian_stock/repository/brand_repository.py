from typing import List

import polars as pl

from ..models.brand import Brand
from . import repository_path as rp


class BrandRepository:
    def __init__(self, repository_path: rp.AbstractRepositoryPath):
        self.repository_path = repository_path

    def load(self) -> List[Brand]:
        brand_ls = []
        conn = self.repository_path.connection_str
        brand_df = pl.read_sql("SELECT * FROM brand;", conn).to_pandas()
        for _, row in brand_df.iterrows():
            code = row["Code"]
            company_name = row["CompanyName"]
            sector17 = row["Sector17Code"]
            sector33 = row["Sector33Code"]
            scale_category = row["ScaleCategory"]
            market_code = row["MarketCode"]
            brand = Brand(code, company_name, sector17, sector33, scale_category, market_code)
            brand_ls.append(brand)
        return brand_ls
