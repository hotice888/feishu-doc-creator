# -*- coding: utf-8 -*-
"""
示例：使用 Feishu Doc Creator 创建飞书文档
"""

import sys
import os

# 添加 Skill 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from feishu_doc_creator import FeishuDocCreator

def main():
    # 初始化创建器
    # ⚠️ 重要：不要在此处硬编码凭证！
    # 请从环境变量或凭证文件读取
    creator = FeishuDocCreator.from_credentials()
    # 或者显式指定（不推荐在代码中硬编码）：
    # creator = FeishuDocCreator(
    #     app_id=os.getenv('FEISHU_APP_ID'),
    #     app_secret=os.getenv('FEISHU_APP_SECRET'),
    #     space_id=os.getenv('FEISHU_SPACE_ID')
    # )
    
    # 示例 1：创建简单文档
    print("="*60)
    print("示例 1：创建简单文档")
    print("="*60)
    
    content_blocks = [
        creator.text_block('快速开始指南', bold=True),
        creator.text_block('这是一个简单的飞书文档创建示例。'),
        creator.divider_block(),
        creator.text_block('步骤 1：安装依赖', bold=True),
        creator.code_block('npm install -g openclaw-cn', language='bash'),
        creator.text_block('步骤 2：运行安装向导', bold=True),
        creator.code_block('openclaw-cn onboard --install-daemon', language='bash'),
        creator.quote_block('💡 提示：确保 Node.js 版本 >= 22'),
    ]
    
    doc_id = creator.create_document_with_content(
        title='快速开始指南',
        source_url='https://github.com/jiulingyun/openclaw-cn',
        content_blocks=content_blocks
    )
    
    if doc_id:
        print(f"文档链接：https://bytedance.feishu.cn/docx/{doc_id}\n")
    
    # 示例 2：创建带图片链接的文档
    print("="*60)
    print("示例 2：创建带图片链接的文档")
    print("="*60)
    
    content_blocks = [
        creator.text_block('配置教程', bold=True),
        creator.text_block('步骤 1：打开飞书开放平台'),
        creator.text_block('📸 截图：https://example.com/step1.png'),
        creator.text_block('步骤 2：创建应用'),
        creator.text_block('📸 截图：https://example.com/step2.png'),
        creator.text_block('步骤 3：获取凭证'),
        creator.text_block('📸 截图：https://example.com/step3.png'),
        creator.code_block('''{
  "app_id": "cli_xxxxx",
  "app_secret": "xxxxx"
}''', language='json'),
    ]
    
    doc_id = creator.create_document_with_content(
        title='配置教程',
        source_url='https://open.feishu.cn/document',
        content_blocks=content_blocks
    )
    
    if doc_id:
        print(f"文档链接：https://bytedance.feishu.cn/docx/{doc_id}\n")
    
    # 示例 3：创建技术文档
    print("="*60)
    print("示例 3：创建技术文档")
    print("="*60)
    
    content_blocks = [
        creator.text_block('API 参考', bold=True),
        creator.text_block('本文档介绍飞书开放平台的主要 API。'),
        creator.divider_block(),
        creator.text_block('1. 认证 API', bold=True),
        creator.ordered_block('获取租户访问令牌'),
        creator.ordered_block('获取用户访问令牌'),
        creator.code_block('''POST /open-apis/auth/v3/tenant_access_token/internal
{
  "app_id": "cli_xxxxx",
  "app_secret": "xxxxx"
}''', language='bash'),
        creator.text_block('2. 文档 API', bold=True),
        creator.ordered_block('创建文档节点'),
        creator.ordered_block('创建文档块'),
        creator.quote_block('⚠️ 注意：单文档每秒最多 3 次编辑'),
    ]
    
    doc_id = creator.create_document_with_content(
        title='API 参考文档',
        source_url='https://open.feishu.cn/api-explorer',
        content_blocks=content_blocks
    )
    
    if doc_id:
        print(f"文档链接：https://bytedance.feishu.cn/docx/{doc_id}\n")
    
    print("="*60)
    print("✅ 所有示例完成！")
    print("="*60)


if __name__ == '__main__':
    main()
