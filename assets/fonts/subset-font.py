#!/usr/bin/env python3
"""
生成字体子集（简体标题）
运行方式: python3 subset-font.py
需要先安装: pip3 install fonttools brotli
"""

from fontTools.subset import main as subset_main

# 所有页面标题需要的简体字符
titles = [
    "中国性少数历史档案",  # 首页
    "宗旨",              # about
    "档案库",            # archive
    "背景",              # background
    "联系我们",          # contact
    "参与",              # contribute
    "文库",              # library
    "纪念",              # memorial
    "序言",              # entry
    "专题文章",          # library/topics
    "网站发起人文辑",    # library/founder
]

chars = ''.join(titles)

# 去重
unique_chars = ''.join(sorted(set(chars)))
print(f"需要的字符 ({len(unique_chars)} 个): {unique_chars}")

# 生成 SanJi 字体子集
print("\n正在生成 SanJi 字体子集...")
args = [
    "SanJiXingKaiJianTi-Cu-2.ttf",    # 输入文件
    f"--text={unique_chars}",         # 要保留的字符
    "--output-file=SanJi-subset.woff2",  # 输出文件
    "--flavor=woff2",                 # 输出格式
    "--layout-features=*",            # 保留所有布局特性
]
subset_main(args)
print("完成! 输出文件: SanJi-subset.woff2")
