import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import folium
import tensorflow as tf
from models import Session, TouristSpot, VisitorData

class AdvancedAnalysis:
    def __init__(self):
        self.session = Session()
        
    def cluster_analysis(self, n_clusters: int = 3) -> dict:
        """景区聚类分析"""
        spots = self.session.query(TouristSpot).all()
        features = np.array([[s.price, s.rating] for s in spots])
        
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        
        kmeans = KMeans(n_clusters=n_clusters)
        clusters = kmeans.fit_predict(features_scaled)
        
        return {
            'clusters': clusters.tolist(),
            'centers': kmeans.cluster_centers_.tolist()
        }
        
    def spatial_analysis(self) -> folium.Map:
        """地理空间分析"""
        spots = self.session.query(TouristSpot).all()
        
        # 创建地图
        center_lat = np.mean([spot.latitude for spot in spots])
        center_lng = np.mean([spot.longitude for spot in spots])
        
        m = folium.Map(location=[center_lat, center_lng], zoom_start=5)
        
        # 添加景点标记
        for spot in spots:
            folium.Marker(
                [spot.latitude, spot.longitude],
                popup=f"{spot.name}\n价格: {spot.price}\n评分: {spot.rating}"
            ).add_to(m)
            
        return m 

    def predict_visitors(self, spot_id: int, days: int = 30) -> dict:
        """预测未来访客量"""
        from sklearn.linear_model import LinearRegression
        
        historical_data = self.session.query(VisitorData)\
            .filter_by(spot_id=spot_id)\
            .order_by(VisitorData.visit_date).all()
            
        # 准备训练数据
        X = np.array(range(len(historical_data))).reshape(-1, 1)
        y = np.array([d.visitor_count for d in historical_data])
        
        # 训练模型
        model = LinearRegression()
        model.fit(X, y)
        
        # 预测
        future_days = np.array(range(len(historical_data), len(historical_data) + days))
        predictions = model.predict(future_days.reshape(-1, 1))
        
        return {
            'predictions': predictions.tolist(),
            'confidence': model.score(X, y)
        } 

    def predict_with_lstm(self, spot_id: int, days: int = 30) -> dict:
        """使用LSTM进行深度学习预测"""
        # 获取历史数据
        data = self.session.query(VisitorData)\
            .filter_by(spot_id=spot_id)\
            .order_by(VisitorData.visit_date).all()
        
        # 准备训练数据
        sequence_length = 7
        X, y = self._prepare_sequences(data, sequence_length)
        
        # 构建LSTM模型
        model = tf.keras.Sequential([
            tf.keras.layers.LSTM(50, activation='relu', input_shape=(sequence_length, 1)),
            tf.keras.layers.Dense(1)
        ])
        
        # 训练模型
        model.compile(optimizer='adam', loss='mse')
        model.fit(X, y, epochs=100, verbose=0)
        
        # 预测
        last_sequence = X[-1:]
        predictions = []
        for _ in range(days):
            pred = model.predict(last_sequence)
            predictions.append(pred[0, 0])
            last_sequence = np.roll(last_sequence, -1)
            last_sequence[0, -1, 0] = pred[0, 0]
        
        return {
            'predictions': predictions,
            'confidence': model.evaluate(X, y, verbose=0)
        } 