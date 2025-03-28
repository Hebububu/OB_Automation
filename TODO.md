# app 작동 구조 생각하기

데이터베이스 초기화
XLSXParser 클래스 초기화
XLSXParser.read_xlsx로 엑셀 파일 읽기 -> return df
XLSXParser.validate_data(df)로 엑셀 파일 검증 -> return validated_df
XLSXParser.register_products_interactively(validated_df) -> DB에 등록되지 않은 상품 insert
TagManager.filter_valid_tags(validated_df)로 DB와 df 비교 후 tag filter -> return filtered_df

# TODO
filter_additional_product(args= validated_df) -> 상품명에 '추가상품'이 있는 데이터만 df에서 필터링
count_ob(args= filtered_df) -> return product_name 별 총 개수를 포함한 df 

특정 product_name은 옵션명을 표기해야 한다.