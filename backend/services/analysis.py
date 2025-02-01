import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from backend.database import Session
from backend.models import TouristSpot, VisitorData
from datetime import datetime
from .cache_manager import CacheManager

class AnalysisService:
    def __init__(self):
        self.session = Session()
        self.cache_manager = CacheManager()
    
    def get_location_distribution(self) -> dict:
        """获取景点地理分布统计"""
        cache_key = f"location_dist_{datetime.now().date()}"
        cached_data = self.cache_manager.get(cache_key)
        if cached_data:
            return cached_data
        
        spots = self.session.query(TouristSpot).all()
        distribution = {}
        for spot in spots:
            if spot.location not in distribution:
                distribution[spot.location] = 0
            distribution[spot.location] += 1
        
        self.cache_manager.set(cache_key, distribution)
        return distribution
    
    def get_price_analysis(self) -> dict:
        """价格分析"""
        prices = [spot.price for spot in self.session.query(TouristSpot).all()]
        return {
            'average': np.mean(prices),
            'median': np.median(prices),
            'max': max(prices),
            'min': min(prices)
        }

    def time_series_analysis(self) -> dict:
        """时间序列分析"""
        visitor_data = self.session.query(VisitorData).all()
        df = pd.DataFrame([{
            'date': v.visit_date,
            'count': v.visitor_count,
            'revenue': v.revenue
        } for v in visitor_data])
        
        # 按月统计
        monthly = df.set_index('date').resample('M').sum()
        
        # 计算环比增长
        monthly['growth_rate'] = monthly['count'].pct_change() * 100
        
        # 季节性分析
        seasonal = df.set_index('date').resample('Q').sum()
        
        return {
            'monthly_stats': monthly.to_dict(),
            'seasonal_stats': seasonal.to_dict(),
            'total_visitors': df['count'].sum(),
            'total_revenue': df['revenue'].sum()
        } 