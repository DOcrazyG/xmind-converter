"""XMind转换器库的打包配置"""

from setuptools import setup, find_packages
import os

# 读取README.md文件内容
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

# 读取requirements.txt文件内容
with open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), 'r', encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name="xmind-converter",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="XMind文件与CSV(三元组)、Markdown、HTML、JSON等文件格式的相互转换",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/xmind-converter",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.md', '*.txt'],
    },
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'xmind-converter = xmind_converter.cli:cli',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)