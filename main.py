import pandas as pd
from app.core.parser import XLSXParser
from app.database.databasemanager import DatabaseManager

pd.set_option('display.max_rows', None)


parser = XLSXParser()

df = parser.read_xlsx("data/input/자동화.xls")

validated_df = parser.validate_data(df)

sorted_df = parser.sort_by_platform_seller_product(df)

parser.register_products_interactively(sorted_df)
