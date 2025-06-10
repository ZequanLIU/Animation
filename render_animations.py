#!/usr/bin/env python3
"""
统计物理动画渲染脚本
用于批量生成场景4-8的所有动画
"""

import subprocess
import sys
import os

# 所有要渲染的场景
SCENES = [
    # 场景4: 累积量生成函数
    "CumulantGeneratingFunctionScene_GIF1_CGFDefinition",
    "CumulantGeneratingFunctionScene_GIF2_CumulantDefinition", 
    "CumulantGeneratingFunctionScene_GIF3_PhysicsAnalogy",
    
    # 场景5: 矩与累积量的华丽变换
    "MomentCumulantTransformScene_GIF1_ExponentialExpansion",
    "MomentCumulantTransformScene_GIF2_LowOrderConversion",
    
    # 场景6: 高斯分布
    "GaussianDistributionScene_GIF1_CumulantSimplicity",
    
    # 场景7: 中心极限定理
    "CentralLimitTheoremScene_GIF1_CumulantScaling",
    "CentralLimitTheoremScene_GIF2_ConvergenceToGaussian",
    
    # 场景8: 概率密度重构
    "ProbabilityReconstructionScene_GIF1_InverseTransform",
    "ProbabilityReconstructionScene_GIF2_JourneySummary"
]

def render_scene(scene_name, quality="medium", format_type="gif"):
    """渲染单个场景"""
    print(f"🎬 正在渲染: {scene_name}")
    
    # 构建manim命令
    quality_flags = {
        "low": "-ql",
        "medium": "-qm", 
        "high": "-qh",
        "production": "-p"
    }
    
    cmd = [
        "manim",
        "scenes_4_8_animations.py",
        scene_name,
        quality_flags.get(quality, "-qm")
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ 成功渲染: {scene_name}")
            return True
        else:
            print(f"❌ 渲染失败: {scene_name}")
            print(f"错误信息: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 渲染出错: {scene_name} - {str(e)}")
        return False

def render_all_scenes(quality="medium"):
    """渲染所有场景"""
    print("🚀 开始批量渲染统计物理动画...")
    print(f"📊 总共 {len(SCENES)} 个场景")
    print(f"🎯 渲染质量: {quality}")
    print("-" * 50)
    
    success_count = 0
    failed_scenes = []
    
    for i, scene in enumerate(SCENES, 1):
        print(f"[{i}/{len(SCENES)}] ", end="")
        
        if render_scene(scene, quality):
            success_count += 1
        else:
            failed_scenes.append(scene)
        
        print()
    
    # 总结
    print("-" * 50)
    print(f"📈 渲染完成! 成功: {success_count}/{len(SCENES)}")
    
    if failed_scenes:
        print("❌ 失败的场景:")
        for scene in failed_scenes:
            print(f"  - {scene}")
    else:
        print("🎉 所有场景渲染成功!")

def render_by_category():
    """按场景分类渲染"""
    categories = {
        "场景4-累积量生成函数": SCENES[0:3],
        "场景5-矩与累积量变换": SCENES[3:5], 
        "场景6-高斯分布": SCENES[5:6],
        "场景7-中心极限定理": SCENES[6:8],
        "场景8-概率密度重构": SCENES[8:10]
    }
    
    print("📂 按场景分类渲染:")
    for category, scenes in categories.items():
        print(f"\n🎭 {category}")
        for scene in scenes:
            render_scene(scene)

def show_help():
    """显示帮助信息"""
    help_text = """
🎬 统计物理动画渲染脚本

用法:
    python render_animations.py [命令] [选项]

命令:
    all         渲染所有场景 (默认)
    category    按场景分类渲染
    single      渲染单个场景
    list        显示所有场景列表
    help        显示此帮助信息

质量选项:
    --quality low      低质量 (快速预览)
    --quality medium   中等质量 (默认)
    --quality high     高质量 
    --quality production 产品级质量

示例:
    python render_animations.py all --quality high
    python render_animations.py single CumulantGeneratingFunctionScene_GIF1_CGFDefinition
    python render_animations.py category
    """
    print(help_text)

def list_scenes():
    """列出所有场景"""
    print("📋 所有场景列表:")
    print("-" * 50)
    
    scene_groups = [
        ("场景4: 累积量生成函数", SCENES[0:3]),
        ("场景5: 矩与累积量的华丽变换", SCENES[3:5]),
        ("场景6: 高斯分布", SCENES[5:6]),
        ("场景7: 中心极限定理", SCENES[6:8]),
        ("场景8: 概率密度重构", SCENES[8:10])
    ]
    
    for group_name, scenes in scene_groups:
        print(f"\n🎭 {group_name}:")
        for i, scene in enumerate(scenes, 1):
            print(f"  {i}. {scene}")

def main():
    """主函数"""
    args = sys.argv[1:]
    
    # 默认参数
    command = "all"
    quality = "medium"
    target_scene = None
    
    # 解析参数
    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg in ["all", "category", "single", "list", "help"]:
            command = arg
        elif arg == "--quality" and i + 1 < len(args):
            quality = args[i + 1]
            i += 1
        elif command == "single" and not target_scene:
            target_scene = arg
        
        i += 1
    
    # 执行命令
    if command == "help":
        show_help()
    elif command == "list":
        list_scenes()
    elif command == "category":
        render_by_category()
    elif command == "single":
        if target_scene:
            render_scene(target_scene, quality)
        else:
            print("❌ 请指定要渲染的场景名称")
            print("💡 使用 'python render_animations.py list' 查看所有场景")
    else:  # 默认渲染所有场景
        render_all_scenes(quality)

if __name__ == "__main__":
    main() 