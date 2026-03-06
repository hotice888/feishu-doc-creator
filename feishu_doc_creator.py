# -*- coding: utf-8 -*-
"""
Feishu Doc Creator - 飞书文档创建助手
自动创建飞书云文档，支持原文链接、图片链接、代码块等
"""

import requests
import time
import json
import os
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

class FeishuDocCreator:
    """飞书文档创建器"""
    
    def __init__(self, app_id=None, app_secret=None, space_id=None):
        """
        初始化创建器
        
        Args:
            app_id: 飞书 App ID
            app_secret: 飞书 App Secret
            space_id: 知识库 Space ID
        """
        # 优先使用参数，其次使用环境变量，最后从配置文件读取
        self.app_id = app_id or os.getenv('FEISHU_APP_ID') or self._load_credentials().get('app_id')
        self.app_secret = app_secret or os.getenv('FEISHU_APP_SECRET') or self._load_credentials().get('app_secret')
        self.space_id = space_id or os.getenv('FEISHU_SPACE_ID') or self._load_credentials().get('space_id')
        
        if not all([self.app_id, self.app_secret, self.space_id]):
            raise ValueError("必须配置 App ID、App Secret 和 Space ID")
        
        self.token = None
        self.doc_id = None
    
    def _load_credentials(self):
        """从配置文件加载凭证"""
        config_paths = [
            os.path.expanduser('~/.feishu/credentials.json'),
            os.path.expanduser('~/.copaw/feishu_credentials.json'),
            'feishu_credentials.json'
        ]
        
        for path in config_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except:
                    continue
        
        return {}
    
    def get_tenant_token(self):
        """获取租户访问令牌"""
        url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
        r = requests.post(url, json={
            'app_id': self.app_id,
            'app_secret': self.app_secret
        })
        result = r.json()
        if result.get('code') == 0:
            self.token = result.get('tenant_access_token')
            return self.token
        else:
            print(f"获取 Token 失败：{result}")
            return None
    
    def create_document(self, title):
        """
        创建文档
        
        Args:
            title: 文档标题
            
        Returns:
            doc_id: 文档 ID
        """
        if not self.token:
            if not self.get_tenant_token():
                return None
        
        url = f'https://open.feishu.cn/open-apis/wiki/v2/spaces/{self.space_id}/nodes'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        data = {
            'title': title,
            'obj_type': 'docx',
            'node_type': 'origin'
        }
        
        r = requests.post(url, headers=headers, json=data)
        result = r.json()
        
        if result.get('code') == 0:
            self.doc_id = result.get('data', {}).get('node', {}).get('obj_token')
            print(f"✅ 文档创建成功：{self.doc_id}")
            print(f"🔗 URL: https://bytedance.feishu.cn/docx/{self.doc_id}")
            return self.doc_id
        else:
            print(f"❌ 文档创建失败：{result}")
            return None
    
    def create_blocks(self, blocks, batch_size=15, delay=0.5):
        """
        创建块
        
        Args:
            blocks: 块列表
            batch_size: 每批块数量
            delay: 批次间延迟（秒）
            
        Returns:
            bool: 是否全部成功
        """
        if not self.doc_id or not self.token:
            print("❌ 请先创建文档")
            return False
        
        url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{self.doc_id}/blocks/{self.doc_id}/children'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        # 分批创建
        batches = [blocks[i:i+batch_size] for i in range(0, len(blocks), batch_size)]
        
        all_success = True
        for i, batch in enumerate(batches, 1):
            data = {
                'index': -1,
                'children': batch
            }
            
            r = requests.post(url, headers=headers, json=data)
            result = r.json()
            
            if result.get('code') == 0:
                print(f"✅ 批次 {i}/{len(batches)} 创建成功")
            else:
                print(f"❌ 批次 {i}/{len(batches)} 创建失败：{result.get('msg')}")
                all_success = False
            
            if i < len(batches):
                time.sleep(delay)
        
        return all_success
    
    def create_document_with_content(self, title, source_url, content_blocks):
        """
        创建带内容的文档（自动添加原文链接）
        
        Args:
            title: 文档标题
            source_url: 原文链接
            content_blocks: 内容块列表（不包含原文链接）
            
        Returns:
            doc_id: 文档 ID
        """
        # 创建文档
        doc_id = self.create_document(title)
        if not doc_id:
            return None
        
        # 构建完整块列表（原文链接在第一行）
        all_blocks = [
            {'block_type': 2, 'text': {'elements': [{'text_run': {'content': f'📎 原文链接：{source_url}'}}]}},
            {'block_type': 22, 'divider': {}}
        ] + content_blocks
        
        # 创建块
        if self.create_blocks(all_blocks):
            print(f"\n✅ 文档内容创建完成")
            return doc_id
        else:
            print(f"\n⚠️ 文档内容部分创建失败")
            return doc_id
    
    @staticmethod
    def text_block(content, bold=False, italic=False):
        """创建文本块"""
        return {
            'block_type': 2,
            'text': {
                'elements': [{
                    'text_run': {
                        'content': content,
                        'bold': bold,
                        'italic': italic
                    }
                }]
            }
        }
    
    @staticmethod
    def bullet_block(content):
        """创建无序列表块"""
        return {
            'block_type': 12,
            'bullet': {
                'elements': [{'text_run': {'content': content}}]
            }
        }
    
    @staticmethod
    def ordered_block(content):
        """创建有序列表块"""
        return {
            'block_type': 13,
            'ordered': {
                'elements': [{'text_run': {'content': content}}]
            }
        }
    
    @staticmethod
    def code_block(code, language='python'):
        """创建代码块"""
        return {
            'block_type': 14,
            'code': {
                'elements': [{'text_run': {'content': code}}],
                'language': language
            }
        }
    
    @staticmethod
    def quote_block(content):
        """创建引用块"""
        return {
            'block_type': 15,
            'quote': {
                'elements': [{'text_run': {'content': content}}]
            }
        }
    
    @staticmethod
    def divider_block():
        """创建分割线"""
        return {'block_type': 22, 'divider': {}}


def main():
    """示例用法"""
    # 初始化创建器
    creator = FeishuDocCreator(
        app_id='cli_a92c40fae038dbde',
        app_secret='USpxv0LPvEcNB6ofv3iW6fA07NIGQ76J',
        space_id='7613425678519634889'
    )
    
    # 构建内容
    content_blocks = [
        creator.text_block('示例文档标题', bold=True),
        creator.text_block('这是正文内容。'),
        creator.bullet_block('列表项 1'),
        creator.bullet_block('列表项 2'),
        creator.code_block('npm install example', language='bash'),
        creator.quote_block('这是一个提示框'),
    ]
    
    # 创建文档
    doc_id = creator.create_document_with_content(
        title='示例文档',
        source_url='https://github.com/example/repo',
        content_blocks=content_blocks
    )
    
    if doc_id:
        print(f"\n🎉 完成！文档链接：https://bytedance.feishu.cn/docx/{doc_id}")


if __name__ == '__main__':
    main()
