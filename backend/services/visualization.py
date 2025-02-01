import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class VisualizationService:
    def create_heatmap(self, data: pd.DataFrame) -> go.Figure:
        """创建热力图"""
        fig = go.Figure(data=go.Densitymapbox(
            lat=data['latitude'],
            lon=data['longitude'],
            z=data['visitor_count'],
            radius=10
        ))
        fig.update_layout(mapbox_style="stamen-terrain")
        return fig
        
    def create_dashboard(self, data: dict) -> list:
        """创建数据大屏"""
        figures = []
        
        # 添加时间趋势图
        fig_trend = px.line(
            data['time_series'],
            x='date',
            y='visitor_count',
            title='游客量趋势'
        )
        figures.append(fig_trend)
        
        # 添加地理分布图
        fig_geo = self.create_heatmap(data['spatial'])
        figures.append(fig_geo)
        
        return figures 