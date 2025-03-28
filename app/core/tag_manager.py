from app.utils.logger import mainLogger
from app.database.databasemanager import DatabaseManager

import pandas as pd

logger = mainLogger()
db = DatabaseManager()

class TagManager:
    """태그를 활용하기 위한 클래스입니다."""
    def __init__(self):
        # 사용할 태그 지정
        self.valid_tags = {"기기", "탱크"}
    
    def filter_valid_tags(self, df):
        """
        기기 혹은 탱크 태그가 있는 행만 필터링
        """

        try:
            logger.info("DB 기반 태그 필터링 시작")
            filtered_rows = []

            for _, row in df.iterrows():
                platform = row["판매사이트명"]
                product_code = row["판매사이트 상품코드"]

                product = db.get_product(platform, product_code)
                if product and product.tag in self.valid_tags:
                    filtered_rows.append(row)
            
            filtered_df = pd.DataFrame(filtered_rows)
            logger.info(f"DB 기반 태그 필터링 완료: {len(filtered_df)} 행")
            return filtered_df
        
        except Exception as e:
            logger.error(f"DB 기반 태그 필터링 실패: {str(e)}")
            raise

