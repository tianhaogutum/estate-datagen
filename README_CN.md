# 合成数据生成项目

## 项目简介

这是一个用于维护和检查管理文档的**合成数据生成系统**。该项目使用Claude AI和多模态LLM技术，基于种子文档自动生成高保真的HTML和PDF格式的合成文档。

**主要目标：**
- 为维护合同（Wartungsvertrag）和维护协议（Wartungsprotokoll）生成逼真的合成文档
- 支持多种设备类型（如热泵、烟雾报警器、太阳能系统等）
- 通过参数化提示工程实现灵活的文档变异
- 生成的文档具有多样化的布局和内容，适用于机器学习模型训练

## 项目结构

```
SyntheticDataGeneration/
├── README.md                              # 英文说明（需完善）
├── README_CN.md                           # 中文说明
├── TechChallenge_Background_Diafania/
│   ├── main.py                            # 主程序入口
│   ├── KONZEPT.md                         # 德文概念文档
│   ├── KONZEPT_CN.md                      # 中文概念文档
│   ├── utils/
│   │   └── render.py                      # HTML到PDF转换工具
│   ├── Daten_AI_Engineer_CaseStudy/       # 种子文档（样本文件）
│   └── output/                            # 生成的文档输出目录
```

## 快速开始

### 1. 环境准备

**系统依赖：**
```bash
# macOS 用户需要安装 LibreOffice（用于 DOCX 转 PDF）
brew install libreoffice
```

**Python 依赖：**
```bash
pip install -r requirements.txt
```

**依赖包括：**
- `anthropic` - Claude API 客户端
- `python-dotenv` - 环境变量管理
- `weasyprint` - HTML 到 PDF 转换

### 2. 配置 API 密钥

创建 `.env` 文件在项目根目录：

```
ANTHROPIC_API_KEY=your_api_key_here
```

获取 API 密钥：访问 [Anthropic Console](https://console.anthropic.com/)

### 3. 准备种子文档

将样本文档放在 `Daten_AI_Engineer_CaseStudy/` 目录中：
- 维护协议样本（PDF）
- 维护合同样本（PDF或DOCX）

程序会自动将 DOCX 转换为 PDF。

## 如何使用

### 基本使用流程

#### 步骤 1：编辑 main.py 配置参数

```python
# 选择生成的文档数量
num_solutions = 1

# 选择文档类型
doc_type = "Wartungsvertrag"  # 或 "Wartungsprotokoll"

# 选择设备类型
system_type = "Rauchwarnmelder"  # 可选：Wärmepumpe、Solaranlage、Klimaanlage、Lüftungsanlage
```

**参数说明：**
- `num_solutions`: 一次生成的文档数量
- `doc_type`: 
  - `"Wartungsvertrag"` - 维护合同
  - `"Wartungsprotokoll"` - 维护协议
- `system_type`: 设备类型
  - `"Wärmepumpe"` - 热泵
  - `"Rauchwarnmelder"` - 烟雾报警器
  - `"Solaranlage"` - 太阳能系统
  - `"Klimaanlage"` - 空调
  - `"Lüftungsanlage"` - 通风系统

#### 步骤 2：运行程序

```bash
cd TechChallenge_Background_Diafania/
python main.py
```

#### 步骤 3：查看生成的文档

输出文件保存在 `output/` 目录中：
- `generated_document_00_[类型]_[设备].html` - HTML 格式
- `generated_document_00_[类型]_[设备]_[序号].pdf` - PDF 格式

### 工作原理

```
种子文档（PDF） 
    ↓
编码为 Base64
    ↓
发送至 Claude API 
    ↓
Claude 根据样式和结构生成新的 HTML
    ↓
提取 HTML 内容
    ↓
使用 WeasyPrint 转换为 PDF
    ↓
保存到 output/ 目录
```

## 核心功能

### 1. 种子引导生成（Seed-Guided Generation）

- 上传样本文档给 Claude
- Claude 学习文档的风格、布局和结构
- 生成符合样式但内容完全不同的新文档

### 2. 基线要求（Baseline Requirements）

**维护协议必须包含：**
- 设备类型（Anlagentyp）
- 维护日期（Datum der Wartung）
- 执行的工作（Durchgeführte Arbeiten）
- 备注（Bemerkungen）
- 签名（Unterschriften）

**维护合同必须包含：**
- 设备类型（Anlagentyp）
- 委托人（Auftraggeber）
- 承包人（Auftragnehmer）
- 维护对象（Objekt der Wartung）
- 协议条款（Vereinbarungen）
- 有效期（Laufzeit）
- 成本（Kosten）
- 签名（Unterschriften）

### 3. 文档多样性

生成的文档之间至少 70% 的代码和文本不同，确保：
- 不同的HTML结构
- 不同的CSS样式
- 不同的内容表述
- 不同的布局设计

## 高级用法

### 批量生成文档

编辑 `main.py` 创建循环：

```python
doc_types = ["Wartungsvertrag", "Wartungsprotokoll"]
system_types = ["Wärmepumpe", "Rauchwarnmelder", "Solaranlage"]

for doc_type in doc_types:
    for system_type in system_types:
        num_solutions = 5
        # 运行生成逻辑
```

### 调整生成参数

在 `main.py` 中修改提示词（prompt）部分以：
- 改变文档风格
- 添加特定字段
- 修改内容指南
- 调整布局约束

## 输出示例

### HTML 输出结构
```html
1. <HTML>
   <head>
       <style>@page { size: A4; }</style>
   </head>
   <body>
       <!-- 维护合同内容 -->
   </body>
</HTML>

2. <HTML>
   <!-- 另一个独特的文档 -->
</HTML>
```

### 文件命名规则
```
generated_document_00_Wartungsvertrag_Rauchwarnmelder.html
generated_document_00_Wartungsvertrag_Rauchwarnmelder_1.pdf
generated_document_00_Wartungsvertrag_Rauchwarnmelder_2.pdf
```

## 技术实现细节

- **AI 模型**: Claude Sonnet 4（claude-sonnet-4-20250514）
- **文档处理**: WeasyPrint 库用于 HTML 到 PDF 转换
- **文档格式**: A4 纸张大小，专业排版
- **语言**: 德语（Deutsch）
- **文档编码**: UTF-8

## 已知限制

- ❌ 缺陷级别生成（无、中等、重大缺陷）尚未实现
- ❌ 文档相似度评估（FID-Layout）未集成
- ❌ 视觉元素（徽标、签名）生成未实现

## 未来改进方向

1. **实现缺陷级别变异** - 在生成的文档中标记不同严重程度的问题
2. **集成相似度评估** - 计算生成文档与种子文档的相似度
3. **视觉增强** - 添加徽标和使用扩散模型生成逼真签名
4. **JSON 数据模式** - 支持生成结构化 JSON 数据
5. **模型训练** - 用生成的数据集训练自定义文档生成模型

## 许可证和参考

参考论文：
- DocGenie: [https://openreview.net/forum?id=cT5v6GjdsH](https://openreview.net/forum?id=cT5v6GjdsH)
- VLM与笔迹扩散: [https://arxiv.org/pdf/2602.21824](https://arxiv.org/pdf/2602.21824)

## 问题排查

### 问题：DOCX 转换失败
**解决方案**: 确保已安装 LibreOffice
```bash
brew install libreoffice
```

### 问题：API 错误
**解决方案**: 
- 检查 `.env` 文件中的 API 密钥
- 确保 API 配额充足
- 检查网络连接

### 问题：PDF 转换失败
**解决方案**:
- 确保 HTML 格式有效
- 检查生成的 HTML 文件内容
- 验证 CSS 样式正确性

## 联系与支持

如有问题或建议，请提出 Issue 或 PR。
