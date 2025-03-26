# app/core/parser.py
import pandas as pd

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

    def read_xlsx(self, file_path):
        """
        XLSX 파일 읽기
        - 파일 존재 여부 확인
        - pandas로 XLSX 파일 읽기
        - DataFrame 반환
        """
        try:
            df = pd.read_excel(file_path)
            print(df)
        except Exception as e:
            raise Exception(f"파일 읽기 실패: {str(e)}")

    def validate_data(self, df):
        """
        데이터 검증
        - 필수 컬럼 존재 여부 확인
        - 데이터 타입 검증
        - 검증 결과 반환
        """
        try:
            for col in self.required_columns:
                if col not in df.columns:
                    raise ValueError(f"필수 컬럼이 존재하지 않습니다: {col}")
            return True
        except Exception as e:
            raise Exception(f"데이터 검증에 실패했습니다: {str(e)}")


    def sort_by_flatform(self, df):
        """
        플랫폼별 데이터 정렬
        - 판매사이트명 기준으로 데이터 정렬
        - 정렬된 DataFrame 반환
        """

    def sort_by_id(self, df):
        """
        판매자 ID별 데이터 정렬
        - 판매자 ID를 기준으로 데이터 정렬
        - 정렬된 DataFrame 반환
        """

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

    def export_xlsx(self, df, output_path):
        """
        결과를 XLSX 파일로 내보내기
        - DataFrame을 XSLX 형식으로 저장
        - 저장 결과 반환
        """