#!/usr/bin/env python3
"""
简化版动画渲染脚本 - 避免中文字体依赖
Simplified Animation Rendering Script - Avoiding Chinese Font Dependencies
使用方法：python render_animations_simple.py [质量选项] [场景编号]
Usage: python render_animations_simple.py [quality] [scene_number]
"""

import subprocess
import sys
import argparse
import os

# 场景列表 - 避免中文字体问题
SCENES = {
    "4.1": "CumulantGeneratingFunctionScene_GIF1_CGFDefinition",
    "4.2": "CumulantGeneratingFunctionScene_GIF2_CumulantDefinition", 
    "4.3": "CumulantGeneratingFunctionScene_GIF3_IndependenceProperty",
    "5.1": "MomentCumulantTransformScene_GIF1_ExponentialExpansion",
    "5.2": "MomentCumulantTransformScene_GIF2_LowOrderConversion",
    "6.1": "GaussianDistributionScene_GIF1_CumulantSimplicity",
    "6.2": "GaussianDistributionScene_GIF2_GoldenStandard",
    "7.1": "CentralLimitTheoremScene_GIF1_CumulantScaling",
    "8.1": "ProbabilityReconstructionScene_GIF1_InverseTransform",
    "8.2": "ProbabilityReconstructionScene_GIF2_JourneySummary"
}

# 质量设置
QUALITY_SETTINGS = {
    "low": "-ql",      # 480p15
    "medium": "-qm",   # 720p30
    "high": "-qh",     # 1080p60
    "production": "-qk" # 2160p60
}

def run_manim_command(scene_name, quality="medium"):
    """运行manim渲染命令"""
    quality_flag = QUALITY_SETTINGS.get(quality, "-qm")
    
    cmd = [
        "manim", 
        "scenes_4_8_animations_simple.py", 
        scene_name, 
        quality_flag
    ]
    
    print(f"正在渲染场景: {scene_name}")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ 成功渲染: {scene_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 渲染失败: {scene_name}")
        print(f"错误信息: {e.stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description="渲染统计物理动画")
    parser.add_argument("--quality", "-q", 
                       choices=list(QUALITY_SETTINGS.keys()),
                       default="medium",
                       help="渲染质量")
    parser.add_argument("--scene", "-s",
                       help="场景编号 (如: 4.1, 4.2, 等) 或 'all'")
    parser.add_argument("--list", "-l", 
                       action="store_true",
                       help="列出所有可用场景")
    
    args = parser.parse_args()
    
    if args.list:
        print("可用场景:")
        for scene_num, scene_name in SCENES.items():
            print(f"  {scene_num}: {scene_name}")
        return
    
    if not args.scene:
        print("请指定场景编号或使用 --list 查看可用场景")
        return
    
    # 检查是否有scenes_4_8_animations_simple.py文件
    if not os.path.exists("scenes_4_8_animations_simple.py"):
        print("错误: 找不到 scenes_4_8_animations_simple.py 文件")
        return
    
    success_count = 0
    total_count = 0
    
    if args.scene.lower() == "all":
        # 渲染所有场景
        for scene_num, scene_name in SCENES.items():
            total_count += 1
            if run_manim_command(scene_name, args.quality):
                success_count += 1
            print("-" * 50)
    else:
        # 渲染指定场景
        if args.scene in SCENES:
            total_count = 1
            scene_name = SCENES[args.scene]
            if run_manim_command(scene_name, args.quality):
                success_count = 1
        else:
            print(f"错误: 场景 '{args.scene}' 不存在")
            print("使用 --list 查看可用场景")
            return
    
    print(f"\n渲染完成: {success_count}/{total_count} 成功")

if __name__ == "__main__":
    main() 