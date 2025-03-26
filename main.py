import pandas as pd
from app.core.parser import XLSXParser

pd.set_option('display.max_rows', None)


parser = XLSXParser() # 엑셀 파서 정의

df = parser.read_xlsx("data/input/자동화.xls") # 엑셀 파일 읽기

validated_df = parser.validate_data(df) # 엑셀 파일 검증 

sorted_df = parser.sort_by_platform_seller_product(df) # 순서대로 정렬

data_per_platform = parser.count_by_platform(df) # 판매사이트별 판매량 집계
print(data_per_platform)

parser.export_xlsx(sorted_df,"data/output") # 엑셀로 데이터 내보내기


