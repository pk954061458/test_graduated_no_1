from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# 创建数据库引擎
engine = create_engine('sqlite:///tourism.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100))
    is_admin = Column(Boolean, default=False)
    data_access_level = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime)
    
    tourist_spots = relationship("TouristSpot", back_populates="user")

class TouristSpot(Base):
    __tablename__ = 'tourist_spots'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    location = Column(String(200))
    latitude = Column(Float)
    longitude = Column(Float)
    price = Column(Float)
    rating = Column(Float)
    description = Column(String(500))
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)
    
    user = relationship("User", back_populates="tourist_spots")
    visitor_data = relationship("VisitorData", back_populates="spot")

class VisitorData(Base):
    __tablename__ = 'visitor_data'
    
    id = Column(Integer, primary_key=True)
    spot_id = Column(Integer, ForeignKey('tourist_spots.id'))
    visit_date = Column(DateTime, default=datetime.now)
    visitor_count = Column(Integer)
    revenue = Column(Float)
    
    spot = relationship("TouristSpot", back_populates="visitor_data")

# 创建所有表
def init_db():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db() 