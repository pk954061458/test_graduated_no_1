from models import Base, User
from database import engine, Session
import bcrypt
import logging

def init_database():
    try:
        # 创建所有表
        Base.metadata.create_all(engine)
        
        # 创建管理员账户
        session = Session()
        if not session.query(User).filter_by(username='admin').first():
            hashed = bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt())
            admin = User(
                username='admin',
                password=hashed.decode('utf-8'),
                email='admin@example.com',
                is_admin=True,
                data_access_level=3
            )
            session.add(admin)
            session.commit()
            print("Admin user created successfully!")
        session.close()
        
    except Exception as e:
        logging.error(f"Database initialization error: {e}")
        raise

if __name__ == '__main__':
    init_database() 