from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Brands(Base):
    __tablename__ = "brands"

    brand_id = Column(Integer, primary_key=True)
    brand_name = Column(String, unique=True)
    products = relationship("Product", back_populates="brand")


class Product(Base):
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey("brands.brand_id"))
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Integer)
    date_updated = Column(Date)
    brand = relationship(Brands, back_populates="products")

    def __repr__(self):
        return f'{self.product_name} products'





#python -m venv env
#.\env\Scripts\activate
#pip install sqlalchemy
#pip freeze > requirements.txt