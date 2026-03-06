# Feishu Doc Creator - 飞书文档创建助手

## 概述

自动化创建飞书云文档的 Skill，支持批量创建文本、代码块、列表、引用、分割线等多种块类型，并自动在文档第一行插入原文链接。

## 核心功能

- ✅ 自动获取飞书 API 访问令牌
- ✅ 在指定知识库创建文档
- ✅ 批量创建多种类型的块（文本、代码、列表、引用、分割线等）
- ✅ **强制在文档第一行插入原文链接**
- ✅ 图片链接自动插入到对应位置
- ✅ 支持粗体、斜体等文本样式
- ✅ 自动处理 API 频率限制
- ✅ 块类型支持检测（自动避开不支持的块类型）

## 支持的块类型

### ✅ 支持的块类型
- `block_type: 2` - Text（普通文本）
- `block_type: 12` - Bullet（无序列表）
- `block_type: 13` - Ordered（有序列表）
- `block_type: 14` - Code（代码块，支持多种语言）
- `block_type: 15` - Quote（引用/提示框）
- `block_type: 22` - Divider（分割线）

### ❌ 不支持的块类型
- `block_type: 1` - Heading1（返回 "block not support to create"）
- `block_type: 3` - Heading3（返回 "invalid param"）
- `block_type: 4` - Heading4（返回 "invalid param"）

**解决方案**: 使用 Text 块 + 粗体模拟标题效果

## 使用方法

### 方式一：直接调用 Python 脚本

```bash
python create_feishu_doc.py
```

### 方式二：通过 CoPaw 对话

告诉阿星："创建一个飞书文档，标题是 XXX，内容是 XXX"

### 方式三：作为模块导入

```python
from feishu_doc_creator import FeishuDocCreator

creator = FeishuDocCreator(
    app_id='cli_xxxxx',
    app_secret='xxxxx',
    space_id='7613425678519634889'
)

doc_id = creator.create_document(
    title='文档标题',
    source_url='https://github.com/...',
    blocks=[
        {'block_type': 2, 'text': {'elements': [{'text_run': {'content': '内容'}}]}},
    ]
)
```

## 配置说明

### 环境变量

在 `~/.feishu/credentials.json` 中配置：

```json
{
  "app_id": "cli_a92c40fae038dbde",
  "app_secret": "USpxv0LPvEcNB6ofv3iW6fA07NIGQ76J",
  "space_id": "7613425678519634889"
}
```

### 或在代码中直接指定

```python
APP_ID = 'cli_xxxxx'
APP_SECRET = 'xxxxx'
SPACE_ID = '7613425678519634889'
```

## 最佳实践

### 1. 文档结构

```python
blocks = [
    # 第 1 行：原文链接（强制）
    {'block_type': 2, 'text': {'elements': [{'text_run': {'content': '📎 原文链接：https://...'}}]}},
    {'block_type': 22, 'divider': {}},
    
    # 第 2 行开始：正式内容
    {'block_type': 2, 'text': {'elements': [{'text_run': {'content': '标题', 'bold': True}}]}},
    {'block_type': 2, 'text': {'elements': [{'text_run': {'content': '正文内容'}}]}},
]
```

### 2. 图片插入

```python
# 图片链接放在对应内容后面
{'block_type': 2, 'text': {'elements': [{'text_run': {'content': '步骤 1：配置环境（📸 图片：https://example.com/img.png）'}}]}}
```

### 3. 代码块

```python
{'block_type': 14, 'code': {
    'elements': [{'text_run': {'content': 'npm install -g package'}}],
    'language': 'bash'
}}
```

### 4. 批量创建

- 每批 10-15 个块比较稳定
- 批次之间 delay 0.5 秒
- 避免单次创建过多块

## API 限制

- **频率限制**: 单文档 3 次编辑/秒
- **块数量**: 一次最多创建 50 个块
- **图片**: 不支持通过 API 直接插入图片，只能用纯文本 URL

## 错误处理

### 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| `1770001` | invalid param | 检查块 schema 格式 |
| `1770029` | block not support to create | 更换支持的块类型 |
| `99992402` | field validation failed | 检查必填字段 |
| `0` | success | 创建成功 |

### 重试机制

```python
def create_blocks_with_retry(doc_id, token, blocks, max_retries=3):
    for i in range(max_retries):
        result = create_blocks(doc_id, token, blocks)
        if result.get('code') == 0:
            return result
        time.sleep(1 * (i + 1))  # 指数退避
    return result
```

## 完整示例

```python
# -*- coding: utf-8 -*-
import requests
import time

APP_ID = 'cli_a92c40fae038dbde'
APP_SECRET = 'USpxv0LPvEcNB6ofv3iW6fA07NIGQ76J'
SPACE_ID = '7613425678519634889'

def get_tenant_token():
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    r = requests.post(url, json={'app_id': APP_ID, 'app_secret': APP_SECRET})
    return r.json().get('tenant_access_token') if r.json().get('code') == 0 else None

def create_doc(token, space_id, title):
    url = f'https://open.feishu.cn/open-apis/wiki/v2/spaces/{space_id}/nodes'
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    data = {'title': title, 'obj_type': 'docx', 'node_type': 'origin'}
    r = requests.post(url, headers=headers, json=data)
    result = r.json()
    if result.get('code') == 0:
        return result.get('data', {}).get('node', {}).get('obj_token')
    return None

def create_blocks(doc_id, token, blocks):
    url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children'
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    data = {'index': -1, 'children': blocks}
    r = requests.post(url, headers=headers, json=data)
    return r.json()

def main():
    token = get_tenant_token()
    if not token:
        print("Failed to get token")
        return
    
    doc_id = create_doc(token, SPACE_ID, "示例文档")
    print(f"Document created: {doc_id}")
    print(f"URL: https://bytedance.feishu.cn/docx/{doc_id}")
    
    # 创建块（包含原文链接）
    batches = [
        [
            {'block_type': 2, 'text': {'elements': [{'text_run': {'content': '📎 原文链接：https://github.com/example/repo'}}]}},
            {'block_type': 22, 'divider': {}},
            {'block_type': 2, 'text': {'elements': [{'text_run': {'content': '示例文档标题', 'bold': True}}]}},
        ],
        [
            {'block_type': 2, 'text': {'elements': [{'text_run': {'content': '这是正文内容。'}}]}},
            {'block_type': 12, 'bullet': {'elements': [{'text_run': {'content': '列表项 1'}}]}},
            {'block_type': 12, 'bullet': {'elements': [{'text_run': {'content': '列表项 2'}}]}},
        ],
        [
            {'block_type': 14, 'code': {'elements': [{'text_run': {'content': 'npm install example'}}], 'language': 'bash'}},
            {'block_type': 15, 'quote': {'elements': [{'text_run': {'content': '这是一个提示框'}}]}},
        ]
    ]
    
    for i, batch in enumerate(batches, 1):
        result = create_blocks(doc_id, token, batch)
        print(f"Batch {i}: {result.get('code')}")
        time.sleep(0.5)
    
    print(f"\n✅ Document complete: https://bytedance.feishu.cn/docx/{doc_id}")

if __name__ == '__main__':
    main()
```

## 文件结构

```
feishu_doc_creator/
├── SKILL.md                 # 本文件
├── feishu_doc_creator.py    # 核心创建脚本
├── credentials.example.json # 凭证示例
└── examples/
    ├── create_basic_doc.py  # 基础示例
    ├── create_with_images.py # 带图片示例
    └── create_from_url.py   # 从 URL 创建示例
```

## 清理临时文件

任务完成后自动清理：
- 测试脚本（test_*.py）
- 临时文档创建脚本
- 调试用的中间文档
- 测试截图文件夹

## 相关资源

- 飞书开放平台：https://open.feishu.cn/document
- API 调试台：https://open.feishu.cn/api-explorer
- 文档 API 参考：https://open.feishu.cn/document/ukTMukTMukTM/ukDNz4SO0MjL5QzM
- GitHub 示例：https://github.com/jiulingyun/openclaw-cn

## 更新日志

### v1.0.0 (2026-03-06)
- ✅ 初始版本
- ✅ 支持 6 种块类型
- ✅ 强制原文链接在第一行
- ✅ 图片链接位置优化
- ✅ 临时文档自动清理
- ✅ 错误处理和重试机制

## 注意事项

1. **必须配置凭证**：App ID、App Secret、Space ID
2. **网络要求**：需要能访问飞书开放平台 API
3. **权限要求**：应用需要文档编辑权限
4. **图片限制**：只能用纯文本 URL，无法直接插入
5. **标题处理**：用 Text+ 粗体模拟，Heading 块不支持

## 作者

- AI 助手：阿星
- 用户：老郑
- 创建时间：2026-03-06
