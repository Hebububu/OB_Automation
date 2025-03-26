from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    """제품 정보 테이블"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    platform = Column(String, nullable=False)
    product_code = Column(String, nullable=False)
    product_name = Column(String)
    tag = Column(String)

    __table_args__ = (
        UniqueConstraint('platform', 'product_code', name='uix_platform_product'),
    )