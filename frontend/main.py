import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import folium
import time
from backend.services.data_permission import DataPermissionService
from backend.services.recommendation import RecommendationService
from backend.services.monitoring import MonitoringService
from backend.services.user_service import UserService
from backend.services.route_planning import RoutePlanningService
from backend.services.data_manager import DataManager
from backend.services.auth import AuthService

# 创建服务实例
permission_service = DataPermissionService()
recommendation_service = RecommendationService()
monitoring_service = MonitoringService()
user_service = UserService()
route_planning_service = RoutePlanningService()
data_manager = DataManager()
auth_service = AuthService()

def login_required(func):
    """登录验证装饰器"""
    def wrapper(*args, **kwargs):
        if not st.session_state.get('user'):
            st.warning("请先登录！")
            return
        return func(*args, **kwargs)
    return wrapper

def create_sidebar():
    st.sidebar.title("旅游数据分析系统")
    
    # 侧边栏风格设置
    st.markdown("""
        <style>
        .css-1d391kg {
            background-color: #1E2738;
        }
        .st-emotion-cache-16txtl3 {
            font-weight: normal;
            color: #333333;
        }
        .stButton>button {
            background-color: transparent;
            color: #333333;
            border: none;
            text-align: left;
            width: 100%;
            padding: 0.5rem 1rem;
        }
        .stButton>button:hover {
            background-color: rgba(255,255,255,0.1);
        }
        .sidebar .sidebar-content {
            background-color: #1E2738;
        }
        </style>
    """, unsafe_allow_html=True)
    
    selected = None
    
    # 数据管理菜单
    st.sidebar.markdown("### 数据管理", unsafe_allow_html=True)
    if st.sidebar.button("📥 数据导入导出", key="data_import", use_container_width=True):
        selected = "数据导入导出"
    if st.sidebar.button("🧹 数据清洗", key="data_clean", use_container_width=True):
        selected = "数据清洗"
    if st.sidebar.button("🛠️ 数据维护", key="data_maintain", use_container_width=True):
        selected = "数据维护"

    st.sidebar.markdown("### 统计分析", unsafe_allow_html=True)
    if st.sidebar.button("🗺️ 地理分布分析", key="geo_analysis", use_container_width=True):
        selected = "地理分布分析"
    if st.sidebar.button("💰 价格区间分析", key="price_analysis", use_container_width=True):
        selected = "价格区间分析" 
    if st.sidebar.button("⭐ 评分销量分析", key="score_analysis", use_container_width=True):
        selected = "评分销量分析"

    st.sidebar.markdown("### 智能推荐", unsafe_allow_html=True)
    if st.sidebar.button("🎯 景点推荐", key="spot_recommend", use_container_width=True):
        selected = "景点推荐"
    if st.sidebar.button("🗺️ 路线规划", key="route_plan", use_container_width=True):
        selected = "路线规划"
    if st.sidebar.button("🔍 相似度分析", key="similarity", use_container_width=True):
        selected = "相似度分析"
        
    return selected


def load_data():
    try:
        return pd.read_csv("attractions.csv")
    except:
        return pd.DataFrame()

def save_data(df):
    df.to_csv("attractions.csv", index=False)

def check_password():
    """返回`True` 如果用户输入了正确的用户名和密码"""
    
    # 初始化 session state
    if "login_attempts" not in st.session_state:
        st.session_state["login_attempts"] = 0
        
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        
    if "show_register" not in st.session_state:
        st.session_state["show_register"] = False
        
    if st.session_state["authenticated"]:
        return True
        
    # 创建登录表单
    placeholder = st.empty()
    
    # 显示注册表单
    if st.session_state["show_register"]:
        with placeholder.form("register_form"):
            st.subheader("用户注册")
            new_username = st.text_input("用户名")
            new_password = st.text_input("密码", type="password")
            confirm_password = st.text_input("确认密码", type="password")
            col1, col2 = st.columns(2)
            with col1:
                register_submit = st.form_submit_button("注册")
            with col2:
                back_to_login = st.form_submit_button("返回登录")
            
            if register_submit:
                if not new_username or not new_password:
                    st.error("用户名和密码不能为空！")
                elif new_password != confirm_password:
                    st.error("两次输入的密码不一致！")
                else:
                    # 这里应该添加将用户信息保存到数据库的逻辑
                    st.success("注册成功！请返回登录页面进行登录。")
                    
            if back_to_login:
                st.session_state["show_register"] = False
                st.rerun()
    
    # 显示登录表单
    else:
        with placeholder.form("login_form"):
            st.subheader("系统登录")
            username = st.text_input("用户名")
            password = st.text_input("密码", type="password")
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("登录")
            with col2:
                register = st.form_submit_button("注册账号")
            
            if submit:
                # 使用auth_service替代硬编码验证
                success, message = auth_service.login(username, password)
                if success:
                    user = auth_service.get_user_by_username(username)
                    token = auth_service.generate_token(user)
                    st.session_state.user = user
                    st.session_state.token = token
                    st.session_state.is_admin = user.is_admin
                    return True
                else:
                    st.error(message)

            if register:
                st.session_state["show_register"] = True
                st.rerun()
    
    return st.session_state["authenticated"]

def main():
    st.set_page_config(page_title="旅游数据分析系统", layout="wide")
    
    if not check_password():
        return
        
    selected = create_sidebar()
    
    # 添加用户和权限管理入口
    if st.session_state.get('is_admin'):
        st.sidebar.markdown("### 系统管理", unsafe_allow_html=True)
        if st.sidebar.button("👥 用户管理", key="user_management"):
            selected = "用户管理"
        if st.sidebar.button("🔐 权限管理", key="permission_management"):
            selected = "权限管理"
    
    # 根据选择显示相应的内容
    if selected == "用户管理":
        show_user_management()
    elif selected == "权限管理":
        show_data_permission_management()
    elif selected == "数据导入导出":
        show_data_import()
    elif selected == "数据清洗":
        show_data_clean()
    elif selected == "数据维护":
        show_data_maintain()
    elif selected == "地理分布分析":
        show_geo_analysis()
    elif selected == "价格区间分析":
        show_price_analysis()
    elif selected == "评分销量分析":
        show_score_analysis()
    elif selected == "景点推荐":
        show_spot_recommend()
    elif selected == "路线规划":
        show_route_plan()
    elif selected == "相似度分析":
        show_similarity()


@login_required
def show_data_import():
    if not permission_service.check_permission(
        st.session_state.user.id, 
        action='write'
    ):
        st.error("没有权限执行此操作")
        return
    st.title("数据导入导出")
    
    # 文件上传
    uploaded_file = st.file_uploader("上传数据文件", type=['csv', 'xlsx'])
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        save_data(df)
        st.success("数据上传成功!")
    
    # 数据预览和编辑
    df = load_data()
    if not df.empty:
        st.subheader("数据预览")
        
        # 数据清洗工具
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("去除重复数据"):
                df = df.drop_duplicates()
                save_data(df)
                st.success("已去除重复数据")
        
        with col2:
            if st.button("填充缺失值"):
                df = df.fillna("未知")
                save_data(df)
                st.success("已填充缺失值")
        
        with col3:
            if st.button("导出数据"):
                csv = df.to_csv(index=False)
                st.download_button(
                    "下载CSV文件",
                    csv,
                    "attractions.csv",
                    "text/csv"
                )
        
        # 数据表格
        st.dataframe(df, height=400)
        
        # 编辑功能
        st.subheader("数据编辑")
        col1, col2 = st.columns(2)
        with col1:
            row_index = st.number_input("选择要编辑的行索引", 0, len(df)-1)
        with col2:
            column = st.selectbox("选择要编辑的列", df.columns)
        
        new_value = st.text_input("输入新值", df.iloc[row_index][column])
        if st.button("更新"):
            df.loc[row_index, column] = new_value
            save_data(df)
            st.success("数据已更新!")

def show_data_clean():
    st.title("数据清洗")
    # 实现数据清洗的逻辑

def show_data_maintain():
    st.title("数据维护")
    # 实现数据维护的逻辑

def show_geo_analysis():
    st.title("地理分布分析")
    df = load_data()
    
    if not df.empty:
        # 城市分布
        st.subheader("城市分布")
        city_counts = df['城市'].value_counts()
        fig = px.bar(city_counts, title="各城市景点数量")
        st.plotly_chart(fig)

def show_price_analysis():
    st.title("价格区间分析")
    df = load_data()
    
    if not df.empty:
        # 价格分布
        st.subheader("价格分布")
        fig = px.histogram(df, x="价格", nbins=30, title="价格分布直方图")
        st.plotly_chart(fig)

def show_score_analysis():
    st.title("评分销量分析")
    df = load_data()
    
    if not df.empty:
        # 基础统计信息
        st.subheader("基础统计信息")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("总景点数", len(df))
            st.metric("平均价格", f"¥{df['价格'].mean():.2f}")
        
        with col2:
            st.metric("总销量", df['销量'].sum())
            st.metric("平均评分", f"{df['评分'].mean():.1f}")
        
        # 相关性分析
        st.subheader("相关性分析")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        corr = df[numeric_cols].corr()
        fig = px.imshow(corr, title="相关性热力图")
        st.plotly_chart(fig)

def show_spot_recommend():
    st.title("景点推荐")
    # 实现景点推荐的逻辑

def show_route_plan():
    st.title("路线规划")
    # 实现路线规划的逻辑

def show_similarity():
    st.title("相似度分析")
    # 实现相似度分析的逻辑

def show_recommendations():
    st.title("智能推荐")
    
    # 选择推荐类型
    rec_type = st.radio(
        "推荐类型",
        ["相似景点推荐", "个性化推荐", "热门景点"]
    )
    
    if rec_type == "相似景点推荐":
        spot_id = st.selectbox("选择景点", get_all_spots())
        similar_spots = recommendation_service.get_similar_spots(spot_id)
        
        for spot in similar_spots:
            st.write(f"### {spot.name}")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("价格", f"¥{spot.price}")
            with col2:
                st.metric("评分", f"{spot.rating}分")

def show_route_planning():
    st.title("路线规划")
    
    selected_spots = st.multiselect(
        "选择要游览的景点",
        get_all_spots()
    )
    
    if st.button("规划路线") and selected_spots:
        route = route_planning_service.plan_optimal_route(
            [s.id for s in selected_spots],
            start_point=(30.5, 114.3)  # 默认起点
        )
        
        # 显示地图
        m = folium.Map(location=[30.5, 114.3], zoom_start=12)
        
        # 添加路线
        coordinates = [(s.latitude, s.longitude) for s in route['spots']]
        folium.PolyLine(coordinates, weight=2, color='red').add_to(m)
        
        # 显示总距离和预计用时
        st.metric("总距离", f"{route['total_distance']:.1f}公里")
        st.metric("预计用时", f"{len(selected_spots) * 2}小时")

def show_real_time_dashboard():
    st.title("实时监控大屏")
    
    # 获取实时数据
    stats = monitoring_service.get_real_time_stats()
    
    # 显示关键指标
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "当前游客数", 
            stats['current_visitors'],
            f"{stats['visitor_growth']:.1f}%"
        )
    with col2:
        st.metric("今日收入", f"¥{stats['today_revenue']:,.2f}")
    with col3:
        st.metric("高峰时段", f"{stats['peak_hours'][0]}:00")
    
    # 显示预警信息
    if stats['alerts']:
        st.warning("⚠️ 预警信息")
        for alert in stats['alerts']:
            st.write(f"- {alert['message']}")
            
    # 自动刷新
    time.sleep(300)  # 5分钟刷新一次
    st.rerun()

def show_data_permission_management():
    st.title("数据权限管理")
    
    if not st.session_state.get('is_admin'):
        st.warning("只有管理员可以访问此页面")
        return
    
    # 显示所有用户
    users = user_service.get_all_users()
    selected_user = st.selectbox(
        "选择用户",
        options=users,
        format_func=lambda x: x.username
    )
    
    if selected_user:
        # 显示当前权限
        st.info(f"当前权限级别: {selected_user.data_access_level}")
        
        # 修改权限
        new_level = st.selectbox(
            "设置权限级别",
            options=[1, 2, 3],
            format_func=lambda x: {
                1: "只读权限",
                2: "读写权限",
                3: "管理员权限"
            }[x]
        )
        
        if st.button("更新权限"):
            if permission_service.grant_permission(
                st.session_state['user_id'],
                selected_user.id,
                new_level
            ):
                st.success("权限更新成功")
            else:
                st.error("权限更新失败")

def show_user_management():
    st.title("用户管理")
    
    if not st.session_state.get('is_admin'):
        st.warning("只有管理员可以访问此页面")
        return
    
    tab1, tab2 = st.tabs(["用户列表", "添加用户"])
    
    with tab1:
        users = user_service.get_all_users()
        for user in users:
            with st.expander(f"用户: {user.username}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"注册时间: {user.created_at}")
                    st.write(f"最后登录: {user.last_login}")
                with col2:
                    st.write(f"权限级别: {user.data_access_level}")
                    st.write(f"管理员: {'是' if user.is_admin else '否'}")
    
    with tab2:
        with st.form("add_user_form"):
            username = st.text_input("用户名")
            password = st.text_input("密码", type="password")
            email = st.text_input("邮箱")
            is_admin = st.checkbox("设为管理员")
            
            if st.form_submit_button("添加用户"):
                if user_service.create_user(username, password, email, is_admin):
                    st.success("用户添加成功")
                else:
                    st.error("用户添加失败")

def init_session_state():
    """初始化session状态"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'token' not in st.session_state:
        st.session_state.token = None

def get_all_spots():
    """获取所有景点"""
    try:
        spots = data_manager.get_all_spots()
        return spots
    except Exception as e:
        st.error(f"获取景点失败: {str(e)}")
        return []

if __name__ == "__main__":
    main()