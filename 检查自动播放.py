#!/usr/bin/env python3
"""
检查HTML文件中的视频自动播放设置
"""

import re
from pathlib import Path

def check_autoplay_settings():
    """检查HTML文件中的自动播放设置"""
    html_file = "statistical_animations_summary.html"
    
    if not Path(html_file).exists():
        print(f"❌ HTML文件 {html_file} 不存在")
        return
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找所有video标签
    video_pattern = r'<video[^>]*>'
    video_tags = re.findall(video_pattern, content)
    
    print("🎬 视频自动播放设置检查")
    print("=" * 50)
    
    autoplay_count = 0
    total_count = len(video_tags)
    
    for i, tag in enumerate(video_tags, 1):
        print(f"\n{i}. {tag}")
        
        # 检查是否包含必要的自动播放属性
        has_autoplay = 'autoplay' in tag
        has_muted = 'muted' in tag
        has_loop = 'loop' in tag
        has_controls = 'controls' in tag
        
        if has_autoplay and has_muted and has_loop and has_controls:
            print("   ✅ 设置完整: autoplay + muted + loop + controls")
            autoplay_count += 1
        else:
            print("   ❌ 设置不完整:")
            if not has_autoplay: print("      - 缺少 autoplay")
            if not has_muted: print("      - 缺少 muted")
            if not has_loop: print("      - 缺少 loop")
            if not has_controls: print("      - 缺少 controls")
    
    print("\n" + "=" * 50)
    print("📊 总结:")
    print(f"   总视频数量: {total_count}")
    print(f"   自动播放设置完整: {autoplay_count}")
    print(f"   设置不完整: {total_count - autoplay_count}")
    
    if autoplay_count == total_count:
        print("\n🎉 太棒了！所有视频都已正确设置为自动播放！")
        print("📝 自动播放功能说明:")
        print("   • autoplay: 页面加载时自动开始播放")
        print("   • muted: 静音播放（浏览器要求）")
        print("   • loop: 播放结束后自动重复")
        print("   • controls: 显示播放控制栏")
    else:
        print(f"\n⚠️ 还有 {total_count - autoplay_count} 个视频需要设置自动播放")

if __name__ == "__main__":
    check_autoplay_settings() 