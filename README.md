# 胡润百富榜2024数据分析项目

## 项目概述

本项目通过爬取2024年胡润百富榜数据，对富豪信息进行多维度分析，包括行业分布、财富分布、人口统计学特征等，并通过可视化图表展示分析结果。

## 项目结构

```
hurun-rich-list-analysis/
├── doc/                                # 文档和数据存储目录
│   ├── hurun_rich_list_2024.csv        # 原始爬取数据
│   └── Charts/                         # 可视化图表目录
│       ├── age_distribution_hist.png
│       ├── birthplace_province_bar.png
│       ├── birthplace_province_pie_chart.png
│       ├── gender_distribution_pie.png
│       ├── industry_counts_atomic_bar_chart.png
│       ├── industry_residence_heatmap.png
│       ├── industry_wealth_atomic_bar_chart.png
│       └── wealth_distribution_hist.png
├── src/
│   ├── Hurun_Spider.py                # 数据爬取脚本
│   └── Hurun_Analysis.py               # 数据分析与可视化脚本
└── README.md                           # 项目说明文件
```

## 数据来源

数据来源于胡润百富官网：https://www.hurun.net/

## 功能实现

### 1. 数据爬取 (`hurun_scraper.py`)

- 通过API接口获取2024年胡润百富榜数据
- 爬取字段包括：
  - 排名、姓名、财富值、财富变化
  - 企业名称、行业分类、公司总部所在地
  - 性别、年龄、出生地、教育背景等个人信息
- 数据保存为CSV格式

### 2. 数据分析与可视化 (`hurun_analysis.py`)

#### 行业分析
- 各行业富豪数量分布（柱状图）
- 各行业总财富值分布（柱状图）

#### 人口统计学分析
- 富豪年龄分布（直方图）
- 富豪性别分布（饼图）
- 富豪出生地分布（饼图+柱状图）

#### 交叉分析
- 行业与居住地交叉分布（热力图）

## 使用说明

### 环境要求

- Python 3.7+
- 所需库：
  - requests
  - pandas
  - matplotlib
  - seaborn

### 安装依赖

```bash
pip install requests pandas matplotlib seaborn
```

### 运行步骤

1. 首先运行爬虫脚本获取数据：
```bash
python src/Hurun_Spider.py
```

2. 然后运行分析脚本生成可视化图表：
```bash
python src/Hurun_Analysis.py
```

## 分析结果

### 主要发现

1. **行业分布**：
   - [简要描述主要发现，如哪些行业富豪数量最多，哪些行业总财富最高]

2. **人口统计学特征**：
   - [描述年龄、性别、出生地等方面的分布特点]

3. **地域特征**：
   - [描述富豪出生地与居住地的分布特点]
   

## 注意事项

1. 胡润官网可能有反爬机制，请合理设置请求间隔
2. API参数中的榜单ID(`num`)可能需要随年份更新
3. 部分富豪的个人信息可能不完整

## 后续改进方向

1. 增加历史数据对比分析
2. 添加财富变化趋势分析
3. 优化可视化图表交互性

## 作者信息

[鲤遑舒/32小组]  
[oruserohung@gmail.com]  
[2025/7/15]