#!/usr/bin/env python3
"""
验证场景4-8的动画是否正确生成并在HTML中引用
"""

import os
import re
from pathlib import Path

def check_video_files():
    """检查视频文件是否存在"""
    video_dir = Path("media/videos/scenes_4_8_animations_simple")
    
    expected_videos = [
        "480p15/CumulantGeneratingFunctionScene_GIF1_CGFDefinition.mp4",
        "480p15/CumulantGeneratingFunctionScene_GIF2_CumulantDefinition.mp4", 
        "480p15/CumulantGeneratingFunctionScene_GIF3_IndependenceProperty.mp4",
        "720p30/MomentCumulantTransformScene_GIF1_ExponentialExpansion.mp4",
        "480p15/MomentCumulantTransformScene_GIF2_LowOrderConversion.mp4",
        "480p15/GaussianDistributionScene_GIF1_CumulantSimplicity.mp4",
        "480p15/CentralLimitTheoremScene_GIF1_CumulantScaling.mp4",
        "480p15/ProbabilityReconstructionScene_GIF1_InverseTransform.mp4",
        "480p15/ProbabilityReconstructionScene_GIF2_JourneySummary.mp4"
    ]
    
    print("🎬 检查动画文件...")
    missing_videos = []
    existing_videos = []
    
    for video_path in expected_videos:
        full_path = video_dir / video_path
        if full_path.exists():
            size_mb = full_path.stat().st_size / (1024 * 1024)
            existing_videos.append((video_path, size_mb))
            print(f"✅ {video_path} ({size_mb:.1f} MB)")
        else:
            missing_videos.append(video_path)
            print(f"❌ {video_path} - 文件不存在")
    
    return existing_videos, missing_videos

def check_html_references():
    """检查HTML文件中的视频引用"""
    html_file = "statistical_animations_summary.html"
    
    if not os.path.exists(html_file):
        print(f"❌ HTML文件 {html_file} 不存在")
        return []
    
    print(f"\n📄 检查HTML文件 {html_file} 中的视频引用...")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找所有视频标签
    video_pattern = r'<source src="([^"]*scenes_4_8_animations_simple[^"]*)"'
    video_refs = re.findall(video_pattern, content)
    
    print(f"🔍 找到 {len(video_refs)} 个场景4-8的视频引用:")
    for i, ref in enumerate(video_refs, 1):
        print(f"   {i}. {ref}")
    
    # 检查引用的文件是否存在
    missing_refs = []
    for ref in video_refs:
        if not os.path.exists(ref):
            missing_refs.append(ref)
            print(f"❌ 引用的文件不存在: {ref}")
        else:
            print(f"✅ 引用正确: {ref}")
    
    return video_refs, missing_refs

def generate_summary():
    """生成总结报告"""
    print("\n" + "="*60)
    print("📊 验证总结报告")
    print("="*60)
    
    existing_videos, missing_videos = check_video_files()
    video_refs, missing_refs = check_html_references()
    
    print(f"\n🎯 动画文件状态:")
    print(f"   ✅ 已生成: {len(existing_videos)} 个")
    print(f"   ❌ 缺失: {len(missing_videos)} 个")
    
    print(f"\n🔗 HTML引用状态:")
    print(f"   ✅ 正确引用: {len(video_refs) - len(missing_refs)} 个")
    print(f"   ❌ 错误引用: {len(missing_refs)} 个")
    
    if len(missing_videos) == 0 and len(missing_refs) == 0:
        print(f"\n🎉 恭喜！所有场景4-8的动画都已正确生成并在HTML中引用！")
        print(f"   您可以打开 statistical_animations_summary.html 查看完整的动画演示。")
    else:
        print(f"\n⚠️ 发现问题:")
        if missing_videos:
            print(f"   需要生成的动画: {missing_videos}")
        if missing_refs:
            print(f"   需要修复的HTML引用: {missing_refs}")
    
    # 显示文件大小统计
    if existing_videos:
        total_size = sum(size for _, size in existing_videos)
        print(f"\n📦 动画文件总大小: {total_size:.1f} MB")

if __name__ == "__main__":
    generate_summary() 