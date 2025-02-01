import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from backend.database import Session
from backend.models import User, TouristSpot, VisitorData

class RecommendationService:
    def __init__(self):
        pass
    
    def get_similar_spots(self, spot_id: int, n_recommendations: int = 5) -> list:
        """基于景点特征的相似景点推荐"""
        spots = self.session.query(TouristSpot).all()
        
        # 构建特征矩阵（价格、评分、访客量等）
        features = np.array([[
            s.price,
            s.rating,
            s.visitor_data[-1].visitor_count if s.visitor_data else 0
        ] for s in spots])
        
        # 计算相似度
        similarities = cosine_similarity(features)
        spot_idx = next(i for i, s in enumerate(spots) if s.id == spot_id)
        
        # 获取最相似的景点
        similar_indices = similarities[spot_idx].argsort()[-n_recommendations-1:-1][::-1]
        return [spots[i] for i in similar_indices]
    
    def get_personalized_recommendations(self, user_id: int, n_recommendations: int = 5) -> list:
        """基于用户历史行为的个性化推荐"""
        # 这里可以实现协同过滤算法
        pass 