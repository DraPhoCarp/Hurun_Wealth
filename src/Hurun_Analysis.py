import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
doc_dir = os.path.join(parent_dir, 'doc')
chart_dir = os.path.join(doc_dir,"Charts")
os.makedirs(chart_dir, exist_ok=True)

def load_data(filename):
    if not os.path.exists(filename):
        print(f"错误: 文件 '{filename}' 不存在。")
        return None
    df = pd.read_csv(filename)
    return df


def process_analysis_data(df):
    if '出生地' in df.columns:
        df['出生地 (省份)'] = df['出生地'].astype(str).apply(
            lambda x: x.split('-')[1].strip() if len(x.split('-')) > 1 and x.split('-')[1].strip() else
            x.split('-')[0].strip() if x.split('-')[0].strip() else None
        )
        df['出生地 (省份)'] = df['出生地 (省份)'].replace(['', 'nan', 'None', 'NaN', 'null'], None)

    if '行业' in df.columns:
        df['行业'] = df['行业'].astype(str).fillna('')
        df_exploded = df.assign(行业=df['行业'].str.split('、')).explode('行业')
        df_exploded['行业'] = df_exploded['行业'].str.strip()
        df_exploded = df_exploded[df_exploded['行业'] != '']
        return df_exploded

    return df


def analyze_and_visualize(df):
    """对DataFrame进行多维度分析和可视化。"""

    sns.set_style("whitegrid")
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 行业分析
    print("\n--- 行业分析 ---")
    if '行业' in df.columns and '财富 (亿元)' in df.columns:
        industry_counts = df['行业'].value_counts(dropna=True).head(15)
        industry_wealth = df.groupby('行业')['财富 (亿元)'].sum().sort_values(ascending=False).head(15)

        plt.figure(figsize=(12, 7));
        sns.barplot(x=industry_counts.index, y=industry_counts.values, palette='viridis')
        plt.title('2024年胡润富豪榜 - 各行业富豪数量分布 (前15，根据行业实际涉及情况存在同一富豪多次统计)', fontsize=16)
        plt.xlabel('行业');
        plt.ylabel('富豪数量');
        plt.xticks(rotation=45, ha='right');
        plt.tight_layout()
        plt.savefig(os.path.join(chart_dir,'industry_counts_atomic_bar_chart.png'));


        plt.figure(figsize=(12, 7));
        sns.barplot(x=industry_wealth.index, y=industry_wealth.values, palette='plasma')
        plt.title('2024年胡润富豪榜 - 各行业总财富值分布 (前15，根据行业实际涉及情况存在同一富豪多次统计)', fontsize=16)
        plt.xlabel('行业');
        plt.ylabel('总财富值 (亿元)');
        plt.xticks(rotation=45, ha='right');
        plt.tight_layout()
        plt.savefig(os.path.join(chart_dir, 'industry_wealth_atomic_bar_chart.png'));

    else:
        print("跳过行业分析，缺少 '行业' 或 '财富 (亿元)' 列。")

    print("\n--- 可视化 ---")

    if '出生地 (省份)' in df.columns:
        birthplace_series_filtered = df['出生地 (省份)'].dropna()
        birthplace_series_filtered = birthplace_series_filtered[birthplace_series_filtered != '']

        if not birthplace_series_filtered.empty:
            residence_counts = birthplace_series_filtered.value_counts().head(10)
            plt.figure(figsize=(10, 10));
            plt.pie(residence_counts, labels=residence_counts.index, autopct='%1.1f%%', startangle=90,
                    colors=sns.color_palette("pastel"), labeldistance=0.85)
            plt.title('2024年胡润富豪榜 - 富豪出生地（省份）分布 (前10)', fontsize=16);
            plt.axis('equal');
            plt.tight_layout()
            plt.savefig(os.path.join(chart_dir,'birthplace_province_pie_chart.png'));

        else:
            print("没有非缺失的出生地（省份）数据可供饼图分析。")


    # 财富值分布
    if '财富 (亿元)' in df.columns and not df['财富 (亿元)'].isnull().all():
        plt.figure(figsize=(10, 6));
        sns.histplot(df['财富 (亿元)'].dropna(), bins=30, kde=True, color='skyblue')
        plt.title('2024年胡润富豪榜 - 富豪财富值分布', fontsize=16);
        plt.xlabel('财富值 (亿元)');
        plt.ylabel('富豪数量');
        plt.tight_layout()
        plt.savefig(os.path.join(chart_dir,'wealth_distribution_hist.png'));

    else:
        print("跳过财富值分布分析。")

    # 年龄分布
    if '年龄' in df.columns and not df['年龄'].isnull().all():
        plt.figure(figsize=(10, 6));
        sns.histplot(df['年龄'].dropna(), bins=10, kde=True, color='lightcoral')
        plt.title('2024年胡润富豪榜 - 富豪年龄分布', fontsize=16);
        plt.xlabel('年龄');
        plt.ylabel('富豪数量');
        plt.tight_layout()
        plt.savefig(os.path.join(chart_dir,'age_distribution_hist.png'));

    else:
        print("跳过年龄分布分析。")

    # 性别分布
    if '性别' in df.columns and not df['性别'].isnull().all():
        gender_counts = df['性别'].value_counts(dropna=True)
        if not gender_counts.empty:
            plt.figure(figsize=(8, 8));
            plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90,
                    colors=sns.color_palette("pastel"), labeldistance=1.05)
            plt.title('2024年胡润富豪榜 - 富豪性别分布', fontsize=16);
            plt.axis('equal');
            plt.tight_layout()
            plt.savefig(os.path.join(chart_dir,'gender_distribution_pie.png'));

    else:
        print("跳过性别分布分析。")

    # 出生地分布 (柱状图) - Modified to exclude NaN
    if '出生地 (省份)' in df.columns:
        # Filter out NaN/None and empty strings before counting
        birthplace_series_filtered = df['出生地 (省份)'].dropna()
        birthplace_series_filtered = birthplace_series_filtered[birthplace_series_filtered != '']

        if not birthplace_series_filtered.empty:
            birthplace_province_counts = birthplace_series_filtered.value_counts().head(10)
            plt.figure(figsize=(12, 7));
            sns.barplot(x=birthplace_province_counts.index, y=birthplace_province_counts.values, palette='coolwarm')
            plt.title('2024年胡润富豪榜 - 富豪出生地（省份）分布 (前10)', fontsize=16);
            plt.xlabel('出生地（省份）');
            plt.ylabel('富豪数量');
            plt.xticks(rotation=45, ha='right');
            plt.tight_layout()
            plt.savefig(os.path.join(chart_dir,'birthplace_province_bar.png'));

        else:
            print("没有非缺失的出生地（省份）数据可供柱状图分析。")
    else:
        print("跳过出生地分布分析。")

    # 行业与居住地交叉分析 (热力图)
    if '行业' in df.columns and '居住地' in df.columns:
        top_industries = df['行业'].value_counts(dropna=True).head(10).index
        top_residences_for_heatmap = df['居住地'].value_counts(dropna=True).head(10).index
        df_filtered_for_heatmap = df[
            df['行业'].isin(top_industries) & df['居住地'].isin(top_residences_for_heatmap)
            ].dropna(subset=['行业', '居住地'])

        cross_tab = pd.crosstab(df_filtered_for_heatmap['行业'], df_filtered_for_heatmap['居住地'], dropna=True)

        if not cross_tab.empty and not cross_tab.sum().sum() == 0:
            plt.figure(figsize=(12, 8));
            sns.heatmap(cross_tab, annot=True, fmt="d", cmap="YlGnBu", linewidths=.5, linecolor='black')
            plt.title('2024年胡润富豪榜 - 行业与居住地交叉分布 (热力图)', fontsize=16);
            plt.xlabel('居住地');
            plt.ylabel('行业');
            plt.xticks(rotation=45, ha='right');
            plt.yticks(rotation=0);
            plt.tight_layout()
            plt.savefig(os.path.join(chart_dir,'industry_residence_heatmap.png'));

        else:
            print("用于行业与居住地交叉分析的数据不足。")
    else:
        print("跳过热力图分析。")

    print("\n--- 分析与可视化任务完成！ ---")


if __name__ == "__main__":
    csv_filename = "hurun_rich_list_2024.csv"
    df_original = load_data(csv_filename)

    if df_original is not None:
        df_processed_for_analysis = process_analysis_data(df_original.copy())
        analyze_and_visualize(df_processed_for_analysis)
    else:
        print("无法加载数据进行分析。请确保 'hurun_scraper.py' 已成功运行并生成了 CSV 文件。")