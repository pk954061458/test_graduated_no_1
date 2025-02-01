# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="tourism",
    version="0.1",
    packages=find_packages(),
    package_data={
        '': ['*.txt', '*.rst', '*.md'],
    },
    description="旅游相关的 Python 包",
    author="您的名字",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/tourism",
    install_requires=[
        'streamlit>=1.0.0',
        'pandas>=1.0.0',
        'numpy>=1.19.0',
        'plotly>=4.14.0',
        'folium>=0.12.0',
        'pyjwt>=2.0.0',
        'requests>=2.25.0',
        'marshmallow>=3.14.0',
        'sqlalchemy>=1.4.0',
        'bcrypt>=3.2.0',
        'python-dotenv>=0.19.0'
    ],
    python_requires='>=3.6',
) 