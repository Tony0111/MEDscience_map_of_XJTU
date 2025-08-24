import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
# =====================================================================
# 首先，定义我们的“领域停用词”列表
# =====================================================================
'''
停用词主要用于过滤掉那些过于通用、频繁出现但对具体研究领域没有实际意义的关键词。
这些词汇往往是描述性或背景性的，不能帮助我们识别出真正的研究热点或趋势。
通过去除这些停用词，我们可以更清晰地聚焦于那些真正反映特定研究领域的关键词，从而提高分析的准确性和有效性。
'''
domain_stop_words = [
    # ============== 常见通用生物体/人群标签 ==============
    'Humans', 'Animals', 'human', 'animal',
    'Female', 'female', 'Male', 'male',
    'Middle Aged',           # 中年人
    'Adult',                 # 成年人
    'Aged',                  # 老年人
    'Young Adult',           # 青年人
    'Adolescent',            # 青少年
    'Child',                 # 儿童
    'Aged, 80 and over',     # 80岁及以上老年人
    "Infant",                # 婴儿
    "Child, Preschool",      # 学龄前儿童
    "Infant, Newborn",       # 新生儿
    "East Asian People",     # 东亚人 (通常人群定义不作为热点)

    # ============== 常见研究类型/报告形式/方法学标签 ==============
    'Case Reports', 'patient', 'patients',
    'Retrospective Studies', 'Cross-Sectional Studies', 'Prospective Studies', # 研究类型
    'Surveys and Questionnaires', # 调查问卷
    'Case-Control Studies',       # 病例对照研究
    "Cohort Studies",             # 队列研究
    "Longitudinal Studies",       # 纵向研究
    "Follow-Up Studies",          # 随访研究
    "Reproducibility of Results", # 结果重现性 (科学研究的基本要求)
    "Nutrition Surveys",          # 营养调查 (属于方法学，而非具体研究内容)
    "ROC Curve",                  # ROC 曲线 (统计学评估工具)
    "meta-analysis",              # Meta分析 (统计学研究方法)
    "Xenograft Model Antitumor Assays", # 异种移植模型抗肿瘤试验 (具体的实验模型和方法)
    "Proportional Hazards Models",# 新增：比例风险模型 (统计学方法)

    # ============== 常见资金/机构/地理位置标签 ==============
    'Research Support, N.I.H., Extramural', # 基金或机构标签
    'United States', # 地理位置
    'United States/epidemiology', # 地理位置/流行病学
    'China','China/epidemiology', # 地理位置
    "Cities",                     # 城市 (过于通用，通常只作为背景)
    "NHANES",                     # 特定研究数据集

    # ============== 常见研究对象/模型/工具标签 ==============
    'Mice', 'Rats',   # 研究对象：小鼠、大鼠
    'Mice, Inbred C57BL', # C57BL近交系小鼠
    'Rats, Sprague-Dawley', # 斯普拉格-道利大鼠
    'Mice, Nude',             # 裸鼠
    "Mice, Inbred BALB C",    # BALB/c 近交系小鼠
    "Mice, Knockout",         # 基因敲除小鼠 (特定类型动物模型)
    'Cell Line, Tumor', # 肿瘤细胞系
    'Cells, Cultured',        # 培养细胞
    "Cell Line",              # 细胞系 (更通用的概念)

    # ============== 常见、宽泛的研究指标/概念/过程标签 ==============
    'Prognosis',            # 研究结果：预后
    'prognosis',            # 小写预后
    'Risk Factors',         # 研究概念：危险因素
    'Treatment Outcome',    # 研究结果：治疗结果
    'Incidence',            # 流行病学指标：发病率
    "Prevalence",           # 流行病学指标：患病率
    'Pregnancy', # 如果是妇产科，可能需要去掉
    'Apoptosis', # 细胞凋亡（如果其细分如 "/drug effects" 或 "/genetics" 更重要，则可作为停用词）
    'apoptosis', # 小写细胞凋亡
    'Disease Models, Animal', # 动物疾病模型（通用概念）
    'Signal Transduction',    # 信号转导（如果其细分如 "/drug effects" 更重要，则可作为停用词）
    'Cell Proliferation',     # 细胞增殖（如果其细分如 "/genetics" 或 "/drug effects" 更重要，则可作为停用词）
    "Inflammation",           # 炎症（作为非常宽泛的病理过程，如果想聚焦更具体的，可考虑停用）
    "inflammation",           # 小写炎症
    "Disease Progression",    # 疾病进展 (通用性质描述)
    "Time Factors",           # 时间因素 (过于泛化)
    "Risk Assessment",        # 风险评估 (通用管理概念)
    "Quality of Life",        # 生活质量 (通用健康结局指标)
    "Temperature",            # 温度 (除非特定领域才有意义)
    "body mass index",        # 身体质量指数
    "Body Mass Index",        # 身体质量指数
    "oxidative stress",       # 小写氧化应激 (保留大写形式为热点)
    "Genotype",               # 基因型 (基础概念)
    "Catalysis",              # 催化 (基础概念)
    "Phenotype",              # 表型 (基础概念)

    # ============== 在此列表中处理大小写不一致的词汇 ==============
    # 这些词汇我们会保留其有大写或更具体形式在后续分析中，此处只为处理小写重复
    "machine learning",
    "immunotherapy"
]
# 你可以根据你的数据不断完善这个列表！


# 定义数据文件路径
data_path = 'D:/MEDscience_map_of_XJTU/data/raw'
# 读取数据文件
df = pd.read_csv(os.path.join(data_path, 'zotero_data_combined.csv'))


# 定义我们要保留的列和它们的新名字
# 这是一个字典，key是原始列名，value是我们的新列名
columns_to_keep = {
    'Author': 'authors',
    'Title': 'title',
    'Publication Title': 'journal',
    'Publication Year': 'year',
    'DOI': 'doi',
    'Abstract Note': 'abstract',
    'Manual Tags': 'manual_tags',
    'Automatic Tags': 'auto_tags',
    'Pages': 'pages',
    'Volume': 'volume',
    'Issue': 'issue'
}
# 从原始DataFrame中只选择我们需要的列
# 注意：df[list(columns_to_keep.keys())] 会选择出所有我们定义好的原始列
df_clean = df[list(columns_to_keep.keys())].copy()
# 对选出的新DataFrame进行重命名
df_clean = df_clean.rename(columns=columns_to_keep)
# --- 验证我们的成果 ---
print("清洗后的数据信息：")
df_clean.info()
print("\n清洗后的数据前5行预览：")
print(df_clean.head())

# 根据info()输出的信息发现：auto_tags列完全为空，因此我们决定丢弃这一列
# 丢弃 'auto_tags' 列
# inplace=True 表示直接在原始的 df_clean 上修改，而不是返回一个新DataFrame
df_clean.drop(columns=['auto_tags'], inplace=True)
print("已丢弃 'auto_tags' 列。")

# 从 info() 看出，journal, doi, abstract, manual_tags 等列都有缺失值。对于这些本应是字符串的列，最好的处理方法是 用一个空字符串 '' 来填充 NaN。
# 找出所有数据类型为 'object' (通常是字符串) 的列
string_columns = df_clean.select_dtypes(include=['object']).columns
# 使用空字符串 '' 填充这些列中的所有 NaN 值
df_clean[string_columns] = df_clean[string_columns].fillna('')
# --- 验证我们的成果 ---
print("\n填充NaN后的数据信息：")
df_clean.info()

# 1. 处理有DOI的记录
#   - isin(['']) 是为了确保我们选中了空字符串
#   - ~ 符号是 "取反" 的意思，所以这里是选择 doi 不是空字符串的行
df_has_doi = df_clean[~df_clean['doi'].isin([''])].copy()
df_no_doi = df_clean[df_clean['doi'].isin([''])].copy()
# 对有DOI的部分进行去重
print(f"去重前，有DOI的记录数: {len(df_has_doi)}")
df_has_doi.drop_duplicates(subset=['doi'], keep='first', inplace=True)
print(f"去重后，有DOI的记录数: {len(df_has_doi)}")

# 2. 处理没有DOI的记录
#    对于没有DOI的，我们使用一个更严格的标准：标题、年份和作者列表都得一样才算重复
print(f"\n去重前，无DOI的记录数: {len(df_no_doi)}")
df_no_doi.drop_duplicates(subset=['title', 'year', 'authors'], keep='first', inplace=True)
print(f"去重后，无DOI的记录数: {len(df_no_doi)}")

# 3. 将处理好的两部分数据重新合并起来
df_final = pd.concat([df_has_doi, df_no_doi], ignore_index=True)
# --- 最终验证 ---
print(f"\n所有数据去重完成！最终剩余 {len(df_final)} 条有效记录。")
print("\n最终数据集信息：")
df_final.info()
# 现在，df_clean 可以被 df_final 覆盖，或者你后面一直使用 df_final
df_clean = df_final

def standardize_author_name(name):
    """
    将单个作者姓名标准化为 'Lastname F.' 的格式。
    例如：'Jin, Xuting' -> 'Jin X'
           'Xuting Jin' -> 'Jin X'
    """
    name = name.strip()  # 去除首尾的空格
    if not name:
        return None  # 如果是空字符串，返回None

    # 情况1: 'Lastname, Firstname' 格式
    if ',' in name:
        parts = name.split(',', 1) # 只分割一次
        last_name = parts[0].strip()
        first_name = parts[1].strip()
        if first_name:
            return f"{last_name} {first_name[0]}"
        else:
            return last_name # 只有姓的情况
    
    # 情况2: 'Firstname Lastname' 格式
    else:
        parts = name.split()
        if len(parts) > 1:
            last_name = parts[-1].strip()
            first_name = parts[0].strip()
            return f"{last_name} {first_name[0]}"
        else:
            # 只有一个词的名字 (比如一个机构名误入)
            return name
        
        # df_clean 是你上一步得到的最终DataFrame
def process_authors_string(authors_str):
    """
    处理整个作者字符串，返回一个标准化的作者列表。
    """
    if not authors_str or pd.isna(authors_str):
        return [] # 如果是空字符串或NaN，返回空列表

    authors_list_raw = authors_str.split(';')
    
    # 对列表中的每个名字应用标准化函数
    standardized_list = [standardize_author_name(name) for name in authors_list_raw]
    
    # 过滤掉处理失败的 None 值
    return [name for name in standardized_list if name is not None]

# 使用 .apply() 方法将这个函数应用到 'authors' 列的每一行
df_clean['authors_list'] = df_clean['authors'].apply(process_authors_string)

# --- 验证我们的成果 ---
# 查看新创建的列和原始列的对比
print("\n作者信息处理前后对比：")
print(df_clean[['authors', 'authors_list']].head())

# 检查一下某一行的数据
print("\n查看单行处理结果示例：")
print("原始数据:", df_clean.loc[0, 'authors'])
print("处理后:", df_clean.loc[0, 'authors_list'])



# ===========================================================================


import pandas as pd
import networkx as nx
from collections import Counter
from itertools import combinations

# =========================================================================
#  前提：假设 df_clean 已经存在于您的环境中
# =========================================================================

# --- 配置参数 (请在此处修改) ---
KEYWORD_COLUMN = 'manual_tags'
SEPARATOR = ';' 


# 转换为小写、去除前后空格，并存入set中以加快查找速度
domain_stop_words_set = {word.strip().lower() for word in domain_stop_words if word.strip()}
# -------------------------------------------------------------

# 2. 调整过滤阈值
MIN_FREQUENCY = 10
MIN_WEIGHT = 5
# =========================================================================


print("--- 步骤1：提取和处理关键词 (已集成停用词) ---")
print(f"加载并清洗了 {len(domain_stop_words_set)} 个领域停用词。")
df_clean[KEYWORD_COLUMN] = df_clean[KEYWORD_COLUMN].fillna('').astype(str)

clean_tags_list = df_clean[KEYWORD_COLUMN].apply(
    lambda x: [
        tag.strip() for tag in x.lower().split(SEPARATOR)
        if tag.strip() and tag.strip().lower() not in domain_stop_words_set
    ]
).tolist()

all_tags_flat = [tag for sublist in clean_tags_list for tag in sublist]
tag_frequencies = Counter(all_tags_flat)
print(f"去除停用词后，数据集中共有 {len(tag_frequencies)} 个独立关键词。")


print("\n--- 步骤2：构建完整的共现网络 ---")
G_full = nx.Graph()
for tags_in_doc in clean_tags_list:
    for pair in combinations(sorted(set(tags_in_doc)), 2):
        if G_full.has_edge(pair[0], pair[1]):
            G_full[pair[0]][pair[1]]['weight'] += 1
        else:
            G_full.add_edge(pair[0], pair[1], weight=1)
print(f"原始网络包含 {G_full.number_of_nodes()} 个节点和 {G_full.number_of_edges()} 条边。")


print("\n--- 步骤3：进行核心过滤，为网络“瘦身” ---")
frequent_keywords = {kw for kw, freq in tag_frequencies.items() if freq >= MIN_FREQUENCY}
G_filtered = nx.Graph()
for u, v, data in G_full.edges(data=True):
    if u in frequent_keywords and v in frequent_keywords and data['weight'] >= MIN_WEIGHT:
        G_filtered.add_edge(u, v, weight=data['weight'])

isolated_nodes = list(nx.isolates(G_filtered))
G_filtered.remove_nodes_from(isolated_nodes)
print("网络过滤完成！")
final_nodes = G_filtered.number_of_nodes()
final_edges = G_filtered.number_of_edges()
print(f"过滤后的网络包含 {final_nodes} 个节点和 {final_edges} 条边。")


print("\n--- 步骤4：导出过滤后的网络为 VOSviewer 文件 ---")
G_keywords_weighted = G_filtered
all_keywords = list(G_keywords_weighted.nodes())
if not all_keywords:
    print("\n!! 警告：过滤后网络为空 !! 请降低过滤阈值。")
else:
    keyword_to_id = {keyword: i + 1 for i, keyword in enumerate(all_keywords)}

    # 创建 Map File (需要表头)
    map_filename = 'vosviewer_map_filtered.txt'
    with open(map_filename, 'w', encoding='utf-8') as f:
        f.write("id\tlabel\tweight\n")
        for keyword in all_keywords:
            node_id = keyword_to_id[keyword]
            label = keyword.replace('"', '').replace("'", "")
            weight = tag_frequencies.get(keyword, 1)
            f.write(f"{node_id}\t{label}\t{weight}\n")
    print(f"成功创建 Map File: '{map_filename}'")

    # 创建 Network File (不能有表头)
    network_filename = 'vosviewer_network_filtered.txt'
    with open(network_filename, 'w', encoding='utf-8') as f:
        for u, v, data in G_keywords_weighted.edges(data=True):
            start_id = keyword_to_id[u]
            end_id = keyword_to_id[v]
            link_strength = data['weight']
            f.write(f"{start_id}\t{end_id}\t{link_strength}\n")
    print(f"成功创建 Network File: '{network_filename}'")
    
    print("\n🎉 全部完成！停用词问题已修复，文件格式正确。")



# =====================================================================
'''python
import pandas as pd
import networkx as nx
from collections import Counter
from itertools import combinations


from collections import Counter
from itertools import combinations
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


import networkx as nx
from itertools import combinations 

import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib.pyplot as plt
import seaborn as sns


import pandas as pd
import glob
import os
'''
