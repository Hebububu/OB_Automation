from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.utils.logger import mainLogger
from app.database.models import Product

logger = mainLogger()

class DatabaseManager:
    """데이터베이스 관리 클래스"""
    
    def __init__(self, db_url: str = 'sqlite:///data/db/test.db'):
        """
        데이터베이스 매니저 초기화
        """
        self.db_url = db_url
        self.engine = None
        self.Session = None
    
    def connect(self) -> Session:
        """
        데이터베이스 연결
        - session을 반환
        """
        try:
            logger.info("데이터베이스 연결을 시도합니다.")
            self.engine = create_engine(self.db_url)
            self.Session = sessionmaker(bind=self.engine)
            logger.info("데이터베이스 연결이 성공했습니다.")
            return self.Session()
        except Exception as e:
            logger.error(f"데이터베이스 연결에 실패했습니다: {str(e)}")
            raise Exception(f"데이터베이스 연결 실패: {str(e)}")
    
    def init_db(self, Base):
        """
        데이터베이스 초기화
        """
        try:
            logger.info("데이터베이스 초기화를 시작합니다.")
            if not self.engine:
                self.connect()
            Base.metadata.create_all(self.engine)
            logger.info("데이터베이스 초기화가 완료되었습니다.")
        except Exception as e:
            logger.error(f"데이터베이스 초기화에 실패했습니다: {str(e)}")
            raise Exception(f"데이터베이스 초기화 실패: {str(e)}")

    """CRUD 구현"""

    def add_product(self, platform: str, product_code: str, product_name: str, tag: str = None) -> Product:
        """
        제품 정보 추가
        """
        try:
            session = self.connect()
            product = Product(
                platform=platform,
                product_code=product_code,
                product_name=product_name,
                tag=tag
            )
            session.add(product)
            session.commit()
            logger.info(f"제품 정보가 추가되었습니다: {platform} - {product_name} - {product_code}")
            return product
        except Exception as e:
            session.rollback()
            logger.error(f"제품 정보 추가 실패: {str(e)}")
            raise
        finally:
            session.close()
    
    def get_product(self, platform: str, product_code: str) -> Product:
        """
        제품 정보 조회
        """
        try:
            session = self.connect()
            product = session.query(Product).filter_by(platform=platform, product_code=product_code).first()
            logger.info(f"조회한 제품 : {product}")
            return product
            
        except Exception as e:
            session.rollback()
            logger.error(f"제품 정보 조회 실패: {str(e)}")
            raise
        finally:
            session.close()

    def update_product_tag(self, platform: str, product_code: str, tag: str) -> Product:
        """
        제품 관리 태그 업데이트
        """
        try:
            session = self.connect()
            product = session.query(Product).filter_by(platform, product_code)
            if product:
                product.tag = tag
                session.commit()
                logger.info(f"제품 태그 업데이트 성공: {platform} - {product_code} - {tag}")
            return product
        
        except Exception as e:
            session.rollback()
            logger.error(f"제품 태그 업데이트 실패: {str(e)}")
            raise

        finally:
            session.close()
    
    def delete_product(self, platform: str, product_code: str) -> Product:
        """
        제품 삭제
        """
        try:
            session = self.connect()
            product = self.get_product(platform=platform, product_code=product_code)

            session.delete(product)
            session.commit()
            logger.info(f"제품 삭제 성공: {product}")

        except Exception as e:
            session.rollback()
            logger.error(f"제품 삭제에 실패했습니다. {str(e)}")
            raise

        finally:
            session.close()

# 전역 인스턴스 생성
db_manager = DatabaseManager()
