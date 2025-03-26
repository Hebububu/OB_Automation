from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.utils.logger import mainLogger

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

# 전역 인스턴스 생성
db_manager = DatabaseManager()
