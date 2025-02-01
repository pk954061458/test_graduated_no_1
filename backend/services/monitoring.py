from datetime import datetime, timedelta
import pandas as pd
from models import Session, TouristSpot, VisitorData
import random

class MonitoringService:
    def __init__(self):
        self.session = Session()
    
    def get_real_time_stats(self):
        """
        获取实时监控数据
        模拟返回一些示例数据
        """
        return {
            'current_visitors': random.randint(100, 1000),
            'visitor_growth': random.uniform(-5, 15),
            'today_revenue': random.uniform(10000, 50000),
            'peak_hours': [random.randint(9, 11), random.randint(14, 16)],
            'alerts': [
                {
                    'message': '景区A游客量接近容量上限',
                    'level': 'warning',
                    'timestamp': datetime.now()
                } if random.random() > 0.7 else None
            ]
        }
    
    def _calculate_growth(self, today_data: list, yesterday_data: list) -> float:
        """计算同比增长率"""
        today_count = sum(d.visitor_count for d in today_data)
        yesterday_count = sum(d.visitor_count for d in yesterday_data)
        
        if yesterday_count == 0:
            return 0
        return ((today_count - yesterday_count) / yesterday_count) * 100
    
    def _get_peak_hours(self, today_data: list) -> list:
        """分析高峰时段"""
        df = pd.DataFrame([{
            'hour': d.visit_date.hour,
            'count': d.visitor_count
        } for d in today_data])
        
        return df.groupby('hour')['count'].sum().nlargest(3).index.tolist()
    
    def _generate_alerts(self, today_data: list) -> list:
        """生成预警信息"""
        alerts = []
        threshold = 1000  # 拥挤阈值
        
        for data in today_data:
            if data.visitor_count > threshold:
                alerts.append({
                    'spot_id': data.spot_id,
                    'message': f'景点人数超过{threshold}，请注意疏导',
                    'level': 'warning'
                })
        
        return alerts 