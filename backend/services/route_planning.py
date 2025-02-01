from typing import List, Tuple
import networkx as nx
from models import Session, TouristSpot

class RoutePlanningService:
    def __init__(self):
        pass
    
    def plan_optimal_route(self, spot_ids: List[int], start_point: Tuple[float, float]) -> dict:
        """规划最优游览路线"""
        spots = self.session.query(TouristSpot).filter(TouristSpot.id.in_(spot_ids)).all()
        
        # 创建图
        G = nx.Graph()
        
        # 添加节点和边
        for i, spot1 in enumerate(spots):
            G.add_node(spot1.id, 
                      pos=(spot1.latitude, spot1.longitude),
                      name=spot1.name)
            
            # 计算景点间距离作为边权重
            for spot2 in spots[i+1:]:
                distance = self._calculate_distance(
                    (spot1.latitude, spot1.longitude),
                    (spot2.latitude, spot2.longitude)
                )
                G.add_edge(spot1.id, spot2.id, weight=distance)
        
        # 使用TSP算法计算最优路径
        path = nx.approximation.traveling_salesman_problem(G, cycle=True)
        
        return {
            'route': path,
            'spots': [{'id': spot_id, 'name': G.nodes[spot_id]['name']} 
                     for spot_id in path],
            'total_distance': self._calculate_total_distance(G, path)
        }
    
    def _calculate_distance(self, point1: Tuple[float, float], 
                          point2: Tuple[float, float]) -> float:
        """计算两点间距离"""
        from math import radians, sin, cos, sqrt, atan2
        
        lat1, lon1 = map(radians, point1)
        lat2, lon2 = map(radians, point2)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return 6371 * c  # 地球半径（公里）
    
    def _calculate_total_distance(self, G: nx.Graph, path: List[int]) -> float:
        """计算路径总距离"""
        total = 0
        for i in range(len(path)-1):
            total += G[path[i]][path[i+1]]['weight']
        return total 