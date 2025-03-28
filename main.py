import pandas as pd
from app.core.parser import XLSXParser
from app.core.tag_manager import TagManager
from app.database.databasemanager import DatabaseManager
from app.database.models import Base

pd.set_option('display.max_rows', None) # df 모든 행 보기 옵션

db = DatabaseManager() # 데이터베이스 초기화
parser = XLSXParser() # 파서 초기화
tag = TagManager() # 태그 초기화

db.init_db(Base) # 데이터베이스 초기화

df = parser.read_xlsx("data/input/자동화.xls")

validated_df = parser.validate_data(df)

parser.register_products_interactively(df)

sorted_df = parser.sort_by_platform_seller_product(df)

filtered_df = tag.filter_valid_tags(sorted_df)

additional_df = parser.filter_additional_product(sorted_df)

if "주문선택사항" not in additional_df.columns:
    additional_df["주문선택사항"] = ""

ob_df = pd.concat([filtered_df, additional_df])

parser.export_xlsx(ob_df, "data/output")