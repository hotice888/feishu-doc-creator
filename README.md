# Feishu Doc Creator 📝

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**飞书文档自动化创建工具** - 通过 API 快速创建专业的飞书云文档

> 🎯 强制规范：文档第一行自动插入原文链接，图片链接智能放置，临时文档自动清理

---

## ✨ 核心特性

- 🚀 **快速创建** - 一键生成飞书文档，支持多种块类型
- 📎 **强制原文链接** - 培养良好习惯，文档第一行自动插入来源链接
- 🖼️ **智能图片处理** - 图片链接自动放置在对应内容位置
- 🗑️ **自动清理** - 任务完成后自动删除临时文档和脚本
- 📦 **开箱即用** - 简洁的 Python API，3 行代码创建文档

---

## 🎯 支持的块类型

| 块类型 | 说明 | 示例 |
|--------|------|------|
| Text | 普通文本（支持粗体） | `text_block('标题', bold=True)` |
| Bullet | 无序列表 | `bullet_block('项目 1')` |
| Ordered | 有序列表 | `ordered_block('步骤 1')` |
| Code | 代码块（多语言） | `code_block('print("Hi")', language='python')` |
| Quote | 引用/提示框 | `quote_block('重要提示')` |
| Divider | 分割线 | `divider_block()` |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置凭证

创建 `~/.feishu/credentials.json` 文件：

```json
{
  "app_id": "cli_xxxxx",
  "app_secret": "xxxxx",
  "space_id": "7613425678519634889"
}
```

> 💡 也可以设置环境变量：`FEISHU_APP_ID`, `FEISHU_APP_SECRET`, `FEISHU_SPACE_ID`

### 3. 使用示例

#### 简单示例

```python
from feishu_doc_creator import FeishuDocCreator

# 初始化
creator = FeishuDocCreator(
    app_id='cli_xxxxx',
    app_secret='xxxxx',
    space_id='7613425678519634889'
)

# 创建内容
content_blocks = [
    creator.text_block('📎 原文链接：https://github.com/hotice888/feishu-doc-creator'),
    creator.divider_block(),
    creator.text_block('欢迎使用 Feishu Doc Creator', bold=True),
    creator.text_block('这是一个自动化工具'),
    creator.code_block('print("Hello World")', language='python'),
]

# 创建文档
doc_id = creator.create_document_with_content(
    title='我的文档',
    source_url='https://github.com/hotice888/feishu-doc-creator',
    content_blocks=content_blocks
)

print(f'文档创建成功：https://bytedance.feishu.cn/docx/{doc_id}')
```

#### 技术文档示例

```python
from feishu_doc_creator import FeishuDocCreator

creator = FeishuDocCreator.from_credentials()

blocks = [
    creator.text_block('📎 原文链接：https://example.com/article'),
    creator.divider_block(),
    creator.text_block('安装步骤', bold=True),
    creator.ordered_block('克隆仓库'),
    creator.ordered_block('安装依赖'),
    creator.ordered_block('配置凭证'),
    creator.text_block('代码示例', bold=True),
    creator.code_block('pip install -r requirements.txt', language='bash'),
    creator.quote_block('💡 提示：确保 Python 版本 >= 3.8'),
]

doc_id = creator.create_document_with_content(
    title='技术文档',
    source_url='https://example.com/article',
    content_blocks=blocks
)
```

---

## 📖 API 参考

### FeishuDocCreator 类

#### 初始化

```python
creator = FeishuDocCreator(app_id, app_secret, space_id)
# 或从凭证文件加载
creator = FeishuDocCreator.from_credentials()
```

#### 创建文档

```python
doc_id = creator.create_document(title)
# 或带内容创建
doc_id = creator.create_document_with_content(title, source_url, content_blocks)
```

#### 块创建方法

```python
creator.text_block(text, bold=False)
creator.bullet_block(text)
creator.ordered_block(text)
creator.code_block(code, language='python')
creator.quote_block(text)
creator.divider_block()
```

#### 批量创建块

```python
creator.create_blocks_in_batches(doc_id, blocks, batch_size=15, delay=0.5)
```

---

## 📁 项目结构

```
feishu-doc-creator/
├── feishu_doc_creator.py    # 核心库
├── SKILL.md                 # 详细技能文档
├── README.md                # 本文件
├── LICENSE                  # MIT 许可证
├── requirements.txt         # Python 依赖
├── skill.json              # Skill 元数据
├── credentials.example.json # 凭证示例
├── .gitignore              # Git 忽略文件
└── examples/
    └── create_example_docs.py  # 使用示例
```

---

## 🔧 配置说明

### 凭证文件位置

- **Windows**: `C:\Users\<用户名>\.feishu\credentials.json`
- **macOS/Linux**: `~/.feishu/credentials.json`

### 环境变量（可选）

```bash
export FEISHU_APP_ID=cli_xxxxx
export FEISHU_APP_SECRET=xxxxx
export FEISHU_SPACE_ID=7613425678519634889
```

---

## ⚠️ API 限制

- **频率限制**: 单文档 3 次编辑/秒
- **块数量**: 一次最多创建 50 个块
- **图片**: 不支持通过 API 直接插入，使用纯文本 URL
- **标题**: Heading 块不支持，用 `text_block('标题', bold=True)` 替代

---

## 💡 最佳实践

### 1. 文档结构模板

```python
blocks = [
    creator.text_block('📎 原文链接：https://...'),  # 强制第一行
    creator.divider_block(),
    creator.text_block('标题', bold=True),
    creator.text_block('正文内容'),
]
```

### 2. 图片处理

```python
# 图片链接放在对应内容后面
creator.text_block('步骤 1（📸 图片：https://example.com/image.png）')
```

### 3. 批量创建

- 每批 10-15 个块
- 批次间 delay 0.5 秒
- 避免单次创建过多

---

## 🧪 运行示例

```bash
cd examples
python create_example_docs.py
```

---

## 📚 相关资源

- [飞书开放平台](https://open.feishu.cn/document)
- [API 调试台](https://open.feishu.cn/api-explorer)
- [文档 API 参考](https://open.feishu.cn/document/ukTMukTMukTM/ukDNz4SO0MjL5QzM)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 👤 作者

- GitHub: [@hotice888](https://github.com/hotice888)
- 创建时间：2026-03-06
- 版本：v1.0.0

---

**Made with ❤️ for the Feishu/Lark Community**
