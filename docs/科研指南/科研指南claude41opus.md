花费0.10

## 🤖 Assistant

作为医学生主动开展这样的系统性调研，说明你很有科研意识！这种方法确实比盲目联系教授要高效得多。我来给你一个详细的操作方案：

## 一、数据收集阶段

### 1. PubMed检索策略
```
检索式构建：
("Xi'an Jiaotong University"[Affiliation] OR 
 "Xian Jiaotong University"[Affiliation] OR
 "Xi An Jiao Tong University"[Affiliation]) 
AND ("2019/01/01"[Date - Publication] : "2024/12/31"[Date - Publication])
```

**建议分学院/附属医院细化**：
- 第一附属医院、第二附属医院分别检索
- 可加入Department限定，如"Department of Cardiology"

### 2. Zotero数据管理
- 创建分层文件夹：按学院→科室→研究方向
- 批量导入时使用PubMed导出的.nbib格式
- 安装ZotFile插件自动重命名PDF
- 使用标签系统标记：高产作者、热点方向、潜在导师

## 二、数据处理与分析

### 3. Python预处理脚本框架
```python
import pandas as pd
from Bio import Entrez
import re

# 提取并清洗作者信息
def extract_xjtu_authors(pmid_list):
    """
    重点提取：
    - 通讯作者（Last Author）
    - 第一作者
    - 共同第一/通讯作者
    """
    
# 识别研究方向
def classify_research_topics(abstracts):
    """
    使用MeSH terms或关键词聚类
    建议用scikit-learn做主题建模
    """

# 生成作者合作网络
def build_collaboration_network():
    """
    输出VOSviewer可识别的格式
    """
```

### 4. VOSviewer可视化重点

**三个关键分析**：
1. **作者合作网络**：找出核心团队和"学术大佬"
2. **关键词共现图谱**：识别研究热点和趋势
3. **引文分析**：判断影响力（如果有数据）

**参数设置建议**：
- Minimum cluster size: 5-10（避免过于分散）
- 使用full counting而非fractional counting
- 时间切片分析：观察研究方向演变

## 三、深度挖掘策略

### 5. 重点关注指标
- **发文量**：年均3篇以上的活跃PI
- **期刊分布**：发表在专业Top期刊的教授
- **合作广度**：国际合作多的导师（机会更多）
- **第一/通讯作者比例**：真正的独立PI
- **近期活跃度**：近2年仍在发文的

### 6. 特别提醒
- 关注**青年教授**：竞争小、机会多、更愿意带本科生
- 查看**基金信息**：有国自然/省部级项目的老师
- 留意**新发方向**：如医学AI、类器官、单细胞等交叉领域

## 四、实战建议

### 7. 输出成果
制作一份**"西交医学院科研地图"**：
- Excel表格：教授姓名|科室|研究方向|代表作|联系方式
- PPT可视化：VOSviewer图谱+解读
- 个人匹配度评分：根据你的兴趣排序

### 8. 后续行动
1. **初筛3-5位目标导师**
2. **精读其近3年代表作**（不只看摘要）
3. **撰写个性化自荐信**：展示你的数据分析能力
4. **先联系其研究生**：了解实验室氛围

## 五、人际交往技巧

- **首次邮件**：附上你的分析报告，展示认真程度
- **面谈准备**：准备1-2个基于其论文的学术问题
- **态度定位**：强调"学习"而非"发文章"
- **时间承诺**：明确每周可投入时间

**加分操作**：如果某教授最近发了重要文章，可以说"我注意到您在Nature子刊上关于XXX的工作..."，这种细节会让教授印象深刻。

需要我帮你写具体的Python脚本或者调试VOSviewer参数吗？
