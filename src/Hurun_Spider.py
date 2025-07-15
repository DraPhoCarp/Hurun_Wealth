import requests
import pandas as pd
import json
import time
import os

# JSON API 的 URL
api_base_url = "https://www.hurun.net/zh-CN/Rank/HsRankDetailsList"

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://www.hurun.net/',
}

# 初始查询参数
base_params = {
    'num': 'ODBYW2BI',  # 2024榜单的特定ID，复现时可以自行更改查询年份对应的ID，如2023年对应：16BKYYA3
    'search': '',
    'offset': 0,
    'limit': 20,  # 每次请求20条数据
}


def fetch_hurun_data(url, headers, base_params):
    """从胡润百富JSON API抓取数据并进行初步处理。"""
    all_rich_data_raw = []
    total_rich_count = 0
    current_offset = 0

    print("开始抓取胡润百富榜 JSON 数据...")

    try:
        while True:
            params = base_params.copy()
            params['offset'] = current_offset

            print(f"正在请求数据：offset={params['offset']}, limit={params['limit']}...")

            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            response_dict = response.json()
            rich_list_items = response_dict.get('rows')  # 富豪列表在 'rows' 键下

            if total_rich_count == 0:
                total_rich_count = response_dict.get('total', 0)
                print(f"检测到榜单总人数：{total_rich_count} 人。")

            if not rich_list_items:
                print(f"offset={current_offset} 处没有数据，可能已抓取完毕或到达榜单末尾。")
                break

            all_rich_data_raw.extend(rich_list_items)
            print(f"成功获取 {len(rich_list_items)} 条数据。当前已累计获取 {len(all_rich_data_raw)} 条。")

            if len(all_rich_data_raw) >= total_rich_count:
                print("已获取所有富豪数据，停止抓取。")
                break

            current_offset += params['limit']
            time.sleep(0.5)

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")

    return all_rich_data_raw


def process_raw_data(raw_data):
    """扁平化原始JSON数据并清洗。"""
    processed_data = []
    for item in raw_data:
        row = {}

        # 提取顶层信息
        row['排名'] = item.get('hs_Rank_Rich_Ranking')
        row['姓名'] = item.get('hs_Rank_Rich_ChaName_Cn')
        row['财富 (亿元)'] = item.get('hs_Rank_Rich_Wealth')
        row['财富变化'] = item.get('hs_Rank_Rich_Wealth_Change')
        row['企业'] = item.get('hs_Rank_Rich_ComName_Cn')
        row['行业'] = item.get('hs_Rank_Rich_Industry_Cn')
        row['居住地'] = item.get('hs_Rank_Rich_ComHeadquarters_Cn')

        # 从 'hs_Character' 嵌套列表中提取个人信息
        if item.get('hs_Character') and len(item['hs_Character']) > 0:
            character_info = item['hs_Character'][0]  # 取第一个人物信息
            row['性别'] = character_info.get('hs_Character_Gender')
            row['年龄'] = character_info.get('hs_Character_Age')
            row['出生地'] = character_info.get('hs_Character_BirthPlace_Cn')
            row['教育程度'] = character_info.get('hs_Character_Education_Cn')
            row['毕业院校'] = character_info.get('hs_Character_School_Cn')
            row['出生日期'] = character_info.get('hs_Character_Birthday')
        else:
            row['性别'] = ''
            row['年龄'] = ''
            row['出生地'] = ''
            row['教育程度'] = ''
            row['毕业院校'] = ''
            row['出生日期'] = ''

        processed_data.append(row)

    df = pd.DataFrame(processed_data)

    # 清洗数据类型
    df['财富 (亿元)'] = pd.to_numeric(df['财富 (亿元)'], errors='coerce')
    df['年龄'] = pd.to_numeric(df['年龄'], errors='coerce')

    return df


if __name__ == "__main__":
    raw_data = fetch_hurun_data(api_base_url, headers, base_params)

    if raw_data:
        df_rich_list = process_raw_data(raw_data)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        doc_dir = os.path.join(parent_dir, 'doc')
        os.makedirs(doc_dir, exist_ok=True)
        output_filename = os.path.join(doc_dir, "hurun_rich_list_2024.csv")
        df_rich_list.to_csv(output_filename, index=False, encoding='utf-8-sig')
        print(f"\n数据已成功抓取并保存到 {output_filename}")
        print("\nDataFrame 结构信息:")
        df_rich_list.info()
        print("\nDataFrame 列名和前5行数据:")
        print(df_rich_list.head())
    else:
        print("未抓取到任何数据。")