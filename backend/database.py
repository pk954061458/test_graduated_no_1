from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging

# 加载环境变量
load_dotenv()

# 获取数据库URL
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables")

try:
    # 创建数据库引擎
    engine = create_engine(DATABASE_URL)
    
    # 测试连接
    with engine.connect() as conn:
        pass
        
except Exception as e:
    logging.error(f"Database connection error: {str(e)}")
    raise

# 创建Session类
Session = sessionmaker(bind=engine) 