# app/core/parser.py
import pandas as pd
import os
from app.utils.logger import mainLogger

logger = mainLogger()

class XLSXParser:
    """ 엑셀 데이터를 활용하기 위한 클래스입니다. """
    def __init__(self):
        """
        초기화
        - 필요한 컬럼 정의
        - 기본 설정값 초기화
        """
        self.required_columns = [
            "판매사이트명",
            "판매사이트 상품코드",
            "판매자ID",
            "상품명",
            "주문선택사항",
            "주문수량"
        ]
        logger.info("XLSXParser 초기화 완료")

    def read_xlsx(self, file_path):
        """
        XLSX 파일 읽기
        - 파일 존재 여부 확인
        - pandas로 XLSX 파일 읽기
        - DataFrame 반환
        """
        try:
            logger.info(f"파일 읽기 시작: {file_path}")
            df = pd.read_excel(file_path)
            logger.info(f"파일 읽기 완료: {len(df)} 행")
            return df
        except Exception as e:
            logger.error(f"파일 읽기 실패: {str(e)}")
            raise Exception(f"파일 읽기 실패: {str(e)}")

    def validate_data(self, df):
        """
        데이터 검증
        - 필수 컬럼 존재 여부 확인
        - 데이터 타입 검증
        - 검증 결과 반환
        """
        try:
            logger.info("데이터 검증 시작")
            for col in self.required_columns:
                if col not in df.columns:
                    logger.error(f"필수 컬럼 누락: {col}")
                    raise ValueError(f"필수 컬럼이 존재하지 않습니다: {col}")
            logger.info("데이터 검증 완료")
            return True
        except Exception as e:
            logger.error(f"데이터 검증 실패: {str(e)}")
            raise Exception(f"데이터 검증 실패: {str(e)}")

    def sort_by_flatform(self, df):
        """
        플랫폼별 데이터 정렬
        - 판매사이트명 기준으로 데이터 정렬
        - 정렬된 DataFrame 반환
        """
        try:
            logger.info("플랫폼별 정렬 시작")
            sorted_df = df.sort_values("판매사이트명")
            logger.info("플랫폼별 정렬 완료")
            return sorted_df
        except Exception as e:
            logger.error(f"플랫폼별 정렬 실패: {str(e)}")
            raise Exception(f"플랫폼별 정렬 실패: {str(e)}")
        
    def sort_by_id(self, df):
        """
        판매자 ID별 데이터 정렬
        - 판매자 ID를 기준으로 데이터 정렬
        - 정렬된 DataFrame 반환
        """
        try:
            logger.info("판매자ID별 정렬 시작")
            sorted_df = df.sort_values("판매자ID")
            logger.info("판매자ID별 정렬 완료")
            return sorted_df
        except Exception as e:
            logger.error(f"판매자ID별 정렬 실패: {str(e)}")
            raise Exception(f"판매자ID별 정렬 실패: {str(e)}")
        
    def sort_by_platform_seller_product(self, df):
        """
        플랫폼, 판매자, 상품 순으로 데이터 정렬
        - 판매사이트명, 판매자ID, 상품명 순으로 정렬
        - 정렬된 DataFrame 반환
        """
        try:
            logger.info("플랫폼, 판매자, 상품 순으로 정렬 시작")
            sorted_df = df.sort_values(by=["판매사이트명","판매자ID","상품명"])
            logger.info("플랫폼, 판매자, 상품 순으로 정렬 완료")
            return sorted_df
        except Exception as e:
            logger.error(f"플랫폼, 판매자, 상품 순 정렬 실패 {str(e)}")
            raise Exception(f"플랫폼, 판매자, 상품 순 정렬 실패 {str(e)}")

    def filter_by_tag(self, df, tag_manager):
        """
        관리용 태그 기반 필터링
        - 태그가 있는 제품만 필터링
        - 필터링된 DataFrame 반환
        """
    
    def count_ob(self, df):
        """
        출고 수량 집계
        - 태그별 출고 수량 계산
        - 집계 결과 반환
        """

    def count_by_platform(self, df):
        """
        판매사이트별 판매량 집계
        - 판매사이트명별로 주문수량을 합계하여 계산
        - 집계 결과를 DataFrame으로로 반환
        """
        try:
            logger.info("판매사이트별 판매량 집계 시작")
            platform_counts = df.groupby('판매사이트명')['주문수량'].sum().reset_index()
            logger.info("판매사이트별 판매량 집계 완료")
            return platform_counts
        except Exception as e:
            logger.error(f"판매사이트별 집계 실패: {str(e)}")
            raise Exception(f"판매사이트별 집계 실패:{str(e)}")

    def export_xlsx(self, df, output_path):
        """
        결과를 XLSX 파일로 내보내기
        - DataFrame을 XSLX 형식으로 저장
        - 저장 결과 반환
        """
        try:
            file_name = "출고데이터.xlsx"
            full_path = os.path.join(output_path, file_name)

            logger.info(f"파일 저장 시작: {full_path}")
            df.to_excel(full_path, index=False)
            logger.info("파일 저장 완료")
            return True
        except Exception as e:
            logger.error(f"파일 저장 실패: {str(e)}")
            raise Exception(f"파일 저장 실패: {str(e)}")