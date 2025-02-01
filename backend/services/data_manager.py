import pandas as pd
from typing import List, Tuple
from models import Session, TouristSpot, VisitorData
import logging
import json

class DataManager:
    def __init__(self):
        self.session = Session()
    
    def import_csv_data(self, file_path: str, user_id: int) -> bool:
        try:
            df = pd.read_csv(file_path)
            # 数据清洗和验证
            df = self.clean_data(df)
            
            # 添加用户关联
            for _, row in df.iterrows():
                spot = TouristSpot(
                    name=row['name'],
                    location=row['location'],
                    latitude=row['latitude'],
                    longitude=row['longitude'],
                    price=row['price'],
                    user_id=user_id  # 设置数据所有者
                )
                self.session.add(spot)
            
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            logging.error(f"Data import error: {e}")
            return False
            
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        # 移除空值
        df = df.dropna(subset=['name', 'location'])
        # 标准化价格
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        return df 

    def validate_data(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """数据验证"""
        try:
            required_columns = ['name', 'location', 'price', 'rating']
            if not all(col in df.columns for col in required_columns):
                return False, "缺少必要的列"
                
            # 数据类型验证
            if not pd.to_numeric(df['price'], errors='coerce').notna().all():
                return False, "价格数据格式不正确"
                
            return True, "验证通过"
        except Exception as e:
            return False, str(e)
            
    def standardize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """数据标准化"""
        # 标准化地理位置信息
        df['location'] = df['location'].str.strip()
        
        # 标准化价格（去除货币符号等）
        df['price'] = df['price'].replace('[\$,¥]', '', regex=True)
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        
        return df 

    def backup_data(self, backup_path: str) -> bool:
        """数据备份"""
        try:
            df = pd.DataFrame([{
                'id': spot.id,
                'name': spot.name,
                'location': spot.location,
                'price': spot.price,
                'rating': spot.rating,
                'visitor_count': spot.visitor_data[-1].visitor_count if spot.visitor_data else 0
            } for spot in self.session.query(TouristSpot).all()])
            
            df.to_csv(backup_path, index=False)
            return True
        except Exception as e:
            logging.error(f"Backup error: {e}")
            return False

    def batch_process(self, data: List[dict]) -> Tuple[int, int]:
        """批量处理数据"""
        success = 0
        failed = 0
        
        for item in data:
            try:
                spot = TouristSpot(**item)
                self.session.add(spot)
                success += 1
            except Exception as e:
                logging.error(f"Processing error for item {item}: {e}")
                failed += 1
                
        self.session.commit()
        return success, failed 

    def get_user_data(self, user_id: int) -> pd.DataFrame:
        """获取用户的数据"""
        spots = self.session.query(TouristSpot)\
            .filter_by(user_id=user_id).all()
            
        return pd.DataFrame([{
            'id': spot.id,
            'name': spot.name,
            'location': spot.location,
            'price': spot.price,
            'rating': spot.rating
        } for spot in spots]) 

    def save_sensitive_data(self, data: dict) -> bool:
        try:
            encrypted_data = self.encryption.encrypt_sensitive_data(
                json.dumps(data)
            )
            # 保存加密数据
            return True
        except Exception as e:
            logging.error(f"Error saving sensitive data: {e}")
            return False 

    def get_all_spots(self):
        """
        获取所有景点数据
        """
        try:
            return pd.read_csv("attractions.csv")
        except:
            return pd.DataFrame() 