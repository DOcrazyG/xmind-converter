# XMind转换器

XMind转换器是一个Python库，用于实现XMind文件与CSV(三元组)、Markdown、HTML、JSON等文件格式的相互转换。

## 功能特性

- 支持XMind文件解析
- 支持转换为CSV、Markdown、HTML、JSON格式
- 支持从CSV、Markdown、JSON格式转换回XMind（部分支持）
- 提供命令行工具
- 支持Python 3.7+

## 安装

### 使用pip安装

```bash
pip install xmind-converter
```

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/xmind-converter.git
cd xmind-converter

# 安装依赖
pip install -r requirements.txt

# 安装包
pip install -e .
```

## 基本使用

### Python API

```python
from xmind_converter import XMindConverter

# 创建转换器实例
converter = XMindConverter()

# 加载XMind文件
node = converter.load_xmind('example.xmind')

# 转换为CSV
csv_content = converter.convert_to(node, 'csv')
print(csv_content)

# 转换为Markdown
md_content = converter.convert_to(node, 'md')
print(md_content)

# 转换为HTML
html_content = converter.convert_to(node, 'html')
print(html_content)

# 转换为JSON
json_content = converter.convert_to(node, 'json')
print(json_content)

# 保存到文件
converter.convert_to(node, 'csv', 'output.csv')
converter.convert_to(node, 'md', 'output.md')
converter.convert_to(node, 'html', 'output.html')
converter.convert_to(node, 'json', 'output.json')
```

### 命令行工具

```bash
# 转换XMind文件到CSV
xmind-converter convert example.xmind output.csv

# 转换XMind文件到Markdown
xmind-converter convert example.xmind output.md

# 转换XMind文件到HTML
xmind-converter convert example.xmind output.html

# 转换XMind文件到JSON
xmind-converter convert example.xmind output.json

# 从CSV转换到XMind
xmind-converter reverse input.csv output.xmind

# 查看版本信息
xmind-converter info
```

## 项目结构

```
xmind_converter/
├── __init__.py          # 包初始化文件
├── core.py              # 核心数据模型
├── parsers/             # XMind文件解析模块
│   ├── __init__.py
│   └── xmind_parser.py  # XMind文件解析器
├── converters/          # 转换模块
│   ├── __init__.py
│   ├── csv_converter.py  # CSV转换逻辑
│   ├── md_converter.py   # Markdown转换逻辑
│   ├── html_converter.py # HTML转换逻辑
│   └── json_converter.py # JSON转换逻辑
├── utils/               # 工具函数
│   ├── __init__.py
│   └── common.py        # 通用工具函数
├── exceptions.py        # 异常定义
└── cli.py               # 命令行工具
tests/                   # 测试代码
docs/                    # 文档
```

## 依赖项

- Python 3.7+
- click >= 8.0.0

## 测试

```bash
# 运行测试
python -m pytest tests/
```

## 贡献

欢迎贡献代码！请按照以下步骤：

1. Fork 仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用MIT许可证 - 详情见 [LICENSE](LICENSE) 文件

## 联系方式

- 作者: Your Name
- 邮箱: your.email@example.com
- 项目链接: https://github.com/yourusername/xmind-converter