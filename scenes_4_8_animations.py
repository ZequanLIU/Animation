from manim import *
import numpy as np
import random

# 配置中文字体支持（改进版，避免xeCJK依赖）
def get_chinese_tex_template():
    """获取支持中文的TeX模板，提供回退机制"""
    try:
        # 尝试使用xeCJK（如果可用）
        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage{xeCJK}")
        tex_template.add_to_preamble(r"\setCJKmainfont{SimHei}")
        return tex_template
    except:
        # 回退到基本模板
        return TexTemplate()

# 创建全局TeX模板
TEX_TEMPLATE = get_chinese_tex_template()

# 为了确保兼容性，我们也提供一个安全的文本创建函数
def safe_text(content, **kwargs):
    """安全创建文本对象，自动处理中文"""
    try:
        return Text(content, font="SimHei", **kwargs)
    except:
        # 如果SimHei不可用，使用默认字体
        return Text(content, **kwargs)

def safe_mathtex(content, **kwargs):
    """安全创建数学文本，处理字体问题"""
    try:
        return MathTex(content, tex_template=TEX_TEMPLATE, **kwargs)
    except:
        # 如果自定义模板失败，使用默认模板
        return MathTex(content, **kwargs)

class CumulantGeneratingFunctionScene_GIF1_CGFDefinition(Scene):
    """场景4.1: 累积量生成函数的定义与神奇特性"""
    
    def construct(self):
        title = safe_text("累积量生成函数 (CGF) 定义", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # MGF回顾
        mgf_formula = safe_mathtex(r"Z(j) = \langle e^{jx} \rangle")
        mgf_formula.shift(UP * 1.5)
        self.play(Write(mgf_formula))
        
        # CGF定义
        cgf_formula = safe_mathtex(r"K(j) = \ln Z(j) = \ln \langle e^{jx} \rangle")
        cgf_formula.next_to(mgf_formula, DOWN, buff=0.8)
        self.play(Write(cgf_formula))
        
        # 解释文本
        explanation = safe_text("CGF是MGF的对数变换", font_size=24, color=YELLOW)
        explanation.next_to(cgf_formula, DOWN, buff=0.8)
        self.play(Write(explanation))
        
        self.wait(2)

class CumulantGeneratingFunctionScene_GIF2_CumulantDefinition(Scene):
    """场景4.2: 累积量的定义与独立性的完美体现"""
    
    def construct(self):
        title = safe_text("累积量定义", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # CGF泰勒展开
        cgf_expansion = safe_mathtex(r"K(j) = \sum_{n=1}^{\infty} \frac{\kappa_n}{n!} j^n")
        cgf_expansion.shift(UP * 1)
        self.play(Write(cgf_expansion))
        
        # 前几个累积量
        kappa1 = safe_mathtex(r"\kappa_1 = \text{mean}", color=GREEN)
        kappa2 = safe_mathtex(r"\kappa_2 = \text{variance}", color=ORANGE)
        kappa3 = safe_mathtex(r"\kappa_3 = \text{skewness}", color=RED)
        
        kappa1.next_to(cgf_expansion, DOWN, buff=0.5)
        kappa2.next_to(kappa1, DOWN, buff=0.3)
        kappa3.next_to(kappa2, DOWN, buff=0.3)
        
        self.play(Write(kappa1))
        self.play(Write(kappa2))
        self.play(Write(kappa3))
        
        self.wait(2)

class CumulantGeneratingFunctionScene_GIF3_PhysicsAnalogy(Scene):
    """场景4.3: 物理类比：配分函数与自由能"""
    
    def construct(self):
        title = safe_text("物理类比：配分函数与自由能", font_size=32, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # 创建物理系统示意图
        # 左侧：统计物理
        physics_title = safe_text("统计物理", font_size=24, color=GREEN)
        physics_title.shift(LEFT * 4 + UP * 1.5)
        
        physics_eqs = VGroup(
            safe_mathtex(r"Z = \text{配分函数}", font_size=20, color=GREEN),
            safe_mathtex(r"F = -k_B T \ln Z", font_size=20, color=GREEN),
            safe_mathtex(r"F = \text{自由能}", font_size=20, color=GREEN)
        ).arrange(DOWN, buff=0.3)
        physics_eqs.shift(LEFT * 4)
        
        # 右侧：概率论
        prob_title = safe_text("概率论", font_size=24, color=RED)
        prob_title.shift(RIGHT * 4 + UP * 1.5)
        
        prob_eqs = VGroup(
            safe_mathtex(r"Z(j) = \text{矩生成函数}", font_size=20, color=RED),
            safe_mathtex(r"W(j) = \ln Z(j)", font_size=20, color=RED),
            safe_mathtex(r"W(j) = \text{累积量生成函数}", font_size=20, color=RED)
        ).arrange(DOWN, buff=0.3)
        prob_eqs.shift(RIGHT * 4)
        
        self.play(Write(physics_title), Write(prob_title))
        self.play(Write(physics_eqs), Write(prob_eqs))
        
        # 连接箭头显示类比
        arrow1 = Arrow(physics_eqs[0].get_right(), prob_eqs[0].get_left(), 
                      color=YELLOW, buff=0.5)
        arrow2 = Arrow(physics_eqs[1].get_right(), prob_eqs[1].get_left(), 
                      color=YELLOW, buff=0.5)
        
        self.play(GrowArrow(arrow1), GrowArrow(arrow2))
        
        # 加性特性说明
        additivity_text = VGroup(
            Text("自由能的加性 ↔ CGF的加性", font_size=24, color=YELLOW),
            Text("独立子系统的普遍规律", font_size=20, color=YELLOW)
        ).arrange(DOWN, buff=0.2)
        additivity_text.shift(DOWN * 2)
        
        self.play(Write(additivity_text))
        
        # W(0) = 0 的性质
        normalization = MathTex(r"W(0) = \ln Z(0) = \ln 1 = 0", 
                              font_size=24, color=WHITE)
        normalization.to_edge(DOWN)
        norm_text = Text("归一化性质", font_size=20, color=WHITE)
        norm_text.next_to(normalization, DOWN)
        
        self.play(Write(normalization), Write(norm_text))
        
        self.wait(3)

class MomentCumulantTransformScene_GIF1_ExponentialExpansion(Scene):
    """场景5.1: 指数函数的泰勒展开 — 变换的核心"""
    
    def construct(self):
        title = Text("指数函数泰勒展开：变换的核心", font_size=32, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # 基本关系
        basic_relation = MathTex(r"Z(j) = e^{W(j)}", font_size=36, color=WHITE)
        basic_relation.shift(UP * 1.5)
        self.play(Write(basic_relation))
        
        # 指数函数展开
        exp_expansion = MathTex(
            r"e^{W(j)} = 1 + W(j) + \frac{W(j)^2}{2!} + \frac{W(j)^3}{3!} + \cdots",
            font_size=28
        )
        exp_expansion.next_to(basic_relation, DOWN, buff=1)
        self.play(Write(exp_expansion))
        
        # W(j)的累积量展开
        w_expansion = MathTex(
            r"W(j) = \sum_k \frac{\langle\langle x^k \rangle\rangle}{k!} j^k",
            font_size=28, color=GREEN
        )
        w_expansion.next_to(exp_expansion, DOWN, buff=1)
        self.play(Write(w_expansion))
        
        # 变换魔法的可视化
        transform_arrow = CurvedArrow(
            w_expansion.get_bottom() + LEFT,
            exp_expansion.get_bottom() + RIGHT,
            color=YELLOW, angle=-PI/4
        )
        
        magic_text = Text("代入展开", font_size=20, color=YELLOW)
        magic_text.next_to(transform_arrow, DOWN)
        
        self.play(Create(transform_arrow), Write(magic_text))
        
        # 拼图比喻
        puzzle_pieces = VGroup()
        colors = [RED, GREEN, BLUE, PURPLE, ORANGE]
        for i in range(5):
            piece = RegularPolygon(n=6, radius=0.3, color=colors[i])
            piece.shift(DOWN * 2 + LEFT * 2 + RIGHT * i)
            puzzle_pieces.add(piece)
        
        puzzle_text = Text("数学拼图的完美契合", font_size=24, color=YELLOW)
        puzzle_text.next_to(puzzle_pieces, DOWN)
        
        self.play(Create(puzzle_pieces), Write(puzzle_text))
        
        # 拼图组合动画
        target_positions = [DOWN * 2 + LEFT * 0.3 + RIGHT * 0.3 * i for i in range(5)]
        for i, piece in enumerate(puzzle_pieces):
            self.play(piece.animate.move_to(target_positions[i]), run_time=0.5)
        
        self.wait(2)

class MomentCumulantTransformScene_GIF2_LowOrderConversion(Scene):
    """场景5.2: 低阶转换：简单而优雅"""
    
    def construct(self):
        title = Text("低阶转换：简单而优雅", font_size=32, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # 转换关系
        conversions = VGroup(
            MathTex(r"\text{一阶：} \langle x \rangle = \langle\langle x \rangle\rangle", 
                   font_size=28, color=GREEN),
            MathTex(r"\text{二阶：} \langle x^2 \rangle = \langle\langle x^2 \rangle\rangle + \langle\langle x \rangle\rangle^2", 
                   font_size=24, color=BLUE),
        ).arrange(DOWN, buff=1)
        conversions.shift(UP)
        
        for conv in conversions:
            self.play(Write(conv))
            self.wait(1)
        
        # 解释含义
        explanations = VGroup(
            Text("均值在两个体系中相同", font_size=20, color=GREEN),
            Text("二阶矩 = 方差 + 均值²", font_size=20, color=BLUE)
        ).arrange(DOWN, buff=1)
        explanations.next_to(conversions, RIGHT, buff=1)
        
        for exp in explanations:
            self.play(Write(exp))
            self.wait(0.8)
        
        # 多变量情况
        multivar_title = Text("多变量情况：", font_size=24, color=PURPLE)
        multivar_title.shift(DOWN * 0.5)
        self.play(Write(multivar_title))
        
        multivar_eq = MathTex(
            r"\langle x_1 x_2 \rangle = \langle\langle x_1 x_2 \rangle\rangle + " +
            r"\langle\langle x_1 \rangle\rangle \langle\langle x_2 \rangle\rangle",
            font_size=24
        )
        multivar_eq.next_to(multivar_title, DOWN)
        self.play(Write(multivar_eq))
        
        # 独立性的美妙展示
        independence_demo = VGroup(
            Text("如果 x₁ 和 x₂ 独立：", font_size=20, color=YELLOW),
            MathTex(r"\langle\langle x_1 x_2 \rangle\rangle = 0", font_size=20, color=RED),
            MathTex(r"\Rightarrow \langle x_1 x_2 \rangle = \langle x_1 \rangle \langle x_2 \rangle", 
                   font_size=20, color=GREEN)
        ).arrange(DOWN, buff=0.3)
        independence_demo.to_edge(DOWN)
        
        for item in independence_demo:
            self.play(Write(item))
            self.wait(0.8)
        
        self.wait(2)

class GaussianDistributionScene_GIF1_CumulantSimplicity(Scene):
    """场景6.1: 高斯分布的累积量：令人惊讶的简洁性"""
    
    def construct(self):
        title = Text("高斯分布：极简主义的化身", font_size=32, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # 高斯分布的MGF
        mgf_gaussian = MathTex(
            r"Z(j) = \langle e^{jx} \rangle = e^{j\mu + \frac{1}{2}j^2\sigma^2}",
            font_size=28, color=GREEN
        )
        mgf_gaussian.shift(UP * 1.5)
        self.play(Write(mgf_gaussian))
        
        # CGF（取对数）
        cgf_gaussian = MathTex(
            r"W(j) = \ln Z(j) = j\mu + \frac{1}{2}j^2\sigma^2",
            font_size=32, color=RED
        )
        cgf_gaussian.next_to(mgf_gaussian, DOWN, buff=1)
        
        # 对数箭头
        log_arrow = Arrow(mgf_gaussian.get_bottom(), cgf_gaussian.get_top(), 
                         color=YELLOW)
        log_text = Text("ln", font_size=24, color=YELLOW)
        log_text.next_to(log_arrow, RIGHT)
        
        self.play(GrowArrow(log_arrow), Write(log_text))
        self.play(Write(cgf_gaussian))
        
        # 突出显示二次多项式
        poly_highlight = SurroundingRectangle(cgf_gaussian, color=YELLOW, buff=0.1)
        poly_text = Text("纯二次多项式！", font_size=24, color=YELLOW)
        poly_text.next_to(poly_highlight, UP)
        
        self.play(Create(poly_highlight), Write(poly_text))
        self.wait(1)
        
        # 累积量的值
        cumulants = VGroup(
            MathTex(r"\kappa_1 = \mu", font_size=24, color=GREEN),
            MathTex(r"\kappa_2 = \sigma^2", font_size=24, color=GREEN),
            MathTex(r"\kappa_n = 0 \text{ for } n > 2", font_size=24, color=RED)
        ).arrange(DOWN, buff=0.5)
        cumulants.shift(DOWN * 1.5)
        
        for cum in cumulants:
            self.play(Write(cum))
            self.wait(0.8)
        
        # 重要结论
        conclusion = Text("累积量 = 偏离高斯分布的指标", 
                        font_size=28, color=PURPLE)
        conclusion.to_edge(DOWN)
        self.play(Write(conclusion))
        
        self.wait(2)

class CentralLimitTheoremScene_GIF1_CumulantScaling(Scene):
    """场景7.1: 样本平均的累积量缩放"""
    
    def construct(self):
        title = Text("中心极限定理：累积量的缩放规律", font_size=30, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # 样本平均定义
        sample_mean = MathTex(
            r"S_N = \frac{1}{N} \sum_{i=1}^N x_i",
            font_size=36, color=WHITE
        )
        sample_mean.shift(UP * 1.5)
        self.play(Write(sample_mean))
        
        # 缩放公式
        scaling_formula = MathTex(
            r"\langle\langle S_N^n \rangle\rangle = \frac{\kappa_n^{(x)}}{N^{n-1}}",
            font_size=32, color=RED
        )
        scaling_formula.next_to(sample_mean, DOWN, buff=1)
        
        scaling_box = SurroundingRectangle(scaling_formula, color=YELLOW, buff=0.1)
        self.play(Create(scaling_box), Write(scaling_formula))
        
        # 具体例子
        examples = VGroup(
            MathTex(r"\langle\langle S_N \rangle\rangle = \kappa_1^{(x)}", 
                   font_size=24, color=GREEN),
            MathTex(r"\langle\langle S_N^2 \rangle\rangle = \frac{\kappa_2^{(x)}}{N}", 
                   font_size=24, color=BLUE),
            MathTex(r"\langle\langle S_N^3 \rangle\rangle = \frac{\kappa_3^{(x)}}{N^2}", 
                   font_size=24, color=PURPLE),
            MathTex(r"\langle\langle S_N^4 \rangle\rangle = \frac{\kappa_4^{(x)}}{N^3}", 
                   font_size=24, color=ORANGE)
        ).arrange(DOWN, buff=0.4)
        examples.shift(DOWN * 0.5)
        
        for i, example in enumerate(examples):
            self.play(Write(example))
            # 为不同阶数添加不同的衰减效果
            if i > 0:
                decay_arrow = Arrow(example.get_right(), 
                                  example.get_right() + RIGHT * 0.5, 
                                  color=RED, stroke_width=2)
                decay_text = Text(f"∝1/N^{i}", font_size=16, color=RED)
                decay_text.next_to(decay_arrow, RIGHT)
                self.play(GrowArrow(decay_arrow), Write(decay_text), run_time=0.5)
            self.wait(0.5)
        
        # 规律总结
        pattern_text = Text("高阶累积量衰减更快！", font_size=24, color=YELLOW)
        pattern_text.to_edge(DOWN)
        self.play(Write(pattern_text))
        
        self.wait(2)

class CentralLimitTheoremScene_GIF2_ConvergenceToGaussian(Scene):
    """场景7.2: 收敛到高斯：累积量的"消失术" """
    
    def construct(self):
        title = Text("累积量的消失术：通往高斯之路", font_size=30, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # N趋于无穷的情况
        n_infinity = MathTex(r"N \to \infty", font_size=36, color=WHITE)
        n_infinity.shift(UP * 1.5)
        self.play(Write(n_infinity))
        
        # 累积量的命运
        cumulant_fates = VGroup(
            MathTex(r"\langle\langle S_N \rangle\rangle = \text{常数}", 
                   font_size=24, color=GREEN),
            MathTex(r"\langle\langle S_N^2 \rangle\rangle \to 0", 
                   font_size=24, color=BLUE),
            MathTex(r"\langle\langle S_N^n \rangle\rangle \to 0 \text{ (更快)}", 
                   font_size=24, color=RED)
        ).arrange(DOWN, buff=0.6)
        cumulant_fates.shift(UP * 0.5)
        
        # 逐个显示并添加消失效果
        for i, fate in enumerate(cumulant_fates):
            self.play(Write(fate))
            if i > 0:
                # 添加消失动画
                disappear_effect = VGroup()
                for j in range(5):
                    star = Star(n=5, outer_radius=0.1, color=YELLOW, fill_opacity=0.8)
                    star.move_to(fate.get_right() + RIGHT * 0.5 + 
                               UP * random.uniform(-0.3, 0.3) + 
                               RIGHT * random.uniform(-0.3, 0.3))
                    disappear_effect.add(star)
                
                self.play(Create(disappear_effect), run_time=0.8)
                self.play(FadeOut(disappear_effect), run_time=0.5)
            self.wait(0.8)
        
        # 结论：高斯分布特征
        conclusion_title = Text("结果：高斯分布的特征", font_size=24, color=PURPLE)
        conclusion_title.shift(DOWN * 1)
        self.play(Write(conclusion_title))
        
        gaussian_char = MathTex(
            r"\text{只有 } \kappa_1, \kappa_2 \text{ 非零，其他累积量} \approx 0",
            font_size=20, color=PURPLE
        )
        gaussian_char.next_to(conclusion_title, DOWN)
        self.play(Write(gaussian_char))
        
        # 普适性说明
        universality = VGroup(
            Text("无论原始分布是什么形状", font_size=20, color=YELLOW),
            Text("大量平均→高斯分布", font_size=24, color=YELLOW)
        ).arrange(DOWN, buff=0.3)
        universality.to_edge(DOWN)
        
        for item in universality:
            self.play(Write(item))
            self.wait(0.5)
        
        self.wait(2)

class ProbabilityReconstructionScene_GIF1_InverseTransform(Scene):
    """场景8.1: 从生成函数到概率密度：数学的"逆向工程" """
    
    def construct(self):
        title = Text("逆向工程：重构概率密度", font_size=32, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # 逆变换公式
        inverse_formula = MathTex(
            r"p(x) = \int \mathcal{D}j \exp(-j^T x + W(j))",
            font_size=28, color=WHITE
        )
        inverse_formula.shift(UP * 1)
        self.play(Write(inverse_formula))
        
        # 等价性说明
        equivalence = VGroup(
            Text("生成函数 ↔ 概率密度函数", font_size=24, color=GREEN),
            Text("完全等价的表示", font_size=20, color=GREEN)
        ).arrange(DOWN, buff=0.3)
        equivalence.next_to(inverse_formula, DOWN, buff=1)
        self.play(Write(equivalence))
        
        # 硬币比喻可视化
        coin = Circle(radius=1, color=YELLOW, fill_opacity=0.3)
        coin.shift(DOWN * 1.5)
        
        # 硬币的两面
        side1 = Text("MGF/CGF", font_size=20, color=BLUE)
        side1.move_to(coin.get_center() + LEFT * 0.8)
        
        side2 = Text("p(x)", font_size=20, color=RED)  
        side2.move_to(coin.get_center() + RIGHT * 0.8)
        
        self.play(Create(coin))
        self.play(Write(side1), Write(side2))
        
        # 硬币翻转动画
        self.play(Rotate(coin, PI, axis=UP), run_time=2)
        
        # 概率变换器比喻
        transformer = VGroup(
            Text("神奇的概率变换器", font_size=24, color=PURPLE),
            Text("输入：累积量信息", font_size=18, color=WHITE),
            Text("输出：完整概率分布", font_size=18, color=WHITE)
        ).arrange(DOWN, buff=0.2)
        transformer.to_edge(DOWN)
        
        for item in transformer:
            self.play(Write(item))
            self.wait(0.5)
        
        self.wait(2)

class ProbabilityReconstructionScene_GIF2_JourneySummary(Scene):
    """场景8.2: 旅程总结：统计物理工具箱的完整画像"""
    
    def construct(self):
        title = Text("统计物理工具箱：完整画像", font_size=32, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # 概念旅程地图
        journey_map = VGroup(
            MathTex(r"p(x)", font_size=24, color=GREEN),
            Text("→", font_size=20),
            MathTex(r"\langle x^n \rangle", font_size=24, color=BLUE),
            Text("→", font_size=20),
            MathTex(r"Z(j)", font_size=24, color=PURPLE),
            Text("→", font_size=20),
            MathTex(r"W(j)", font_size=24, color=RED),
            Text("→", font_size=20),
            MathTex(r"\langle\langle x^n \rangle\rangle", font_size=24, color=ORANGE)
        ).arrange(RIGHT, buff=0.3)
        journey_map.shift(UP * 1.5)
        
        # 逐步显示旅程
        for item in journey_map:
            self.play(Write(item), run_time=0.5)
        
        # 概念标签
        labels = VGroup(
            Text("概率密度", font_size=16, color=GREEN),
            Text("矩", font_size=16, color=BLUE),
            Text("MGF", font_size=16, color=PURPLE),
            Text("CGF", font_size=16, color=RED),
            Text("累积量", font_size=16, color=ORANGE)
        )
        
        # 定位标签
        concept_positions = [journey_map[0], journey_map[2], journey_map[4], 
                           journey_map[6], journey_map[8]]
        for i, (label, pos) in enumerate(zip(labels, concept_positions)):
            label.next_to(pos, DOWN, buff=0.3)
            self.play(Write(label), run_time=0.3)
        
        # 关键联系
        key_connections = VGroup(
            MathTex(r"W(j) = \ln Z(j)", font_size=20, color=YELLOW),
            MathTex(r"Z(j) = e^{W(j)}", font_size=20, color=YELLOW),
            MathTex(r"p(x) = \int \mathcal{D}j \exp(-j^T x + W(j))", font_size=16, color=YELLOW)
        ).arrange(DOWN, buff=0.3)
        key_connections.shift(DOWN * 0.5)
        
        connection_title = Text("关键联系：", font_size=20, color=YELLOW)
        connection_title.next_to(key_connections, UP)
        
        self.play(Write(connection_title))
        for conn in key_connections:
            self.play(Write(conn), run_time=0.8)
        
        # 核心洞察
        insights = VGroup(
            Text("🎯 核心洞察：", font_size=24, color=WHITE),
            Text("这些工具是理解复杂随机系统的基石", font_size=18, color=WHITE),
            Text("掌握它们 = 拥有分析随机世界的超能力", font_size=18, color=GOLD)
        ).arrange(DOWN, buff=0.2)
        insights.to_edge(DOWN)
        
        for insight in insights:
            self.play(Write(insight))
            self.wait(0.5)
        
        # 最终庆祝效果
        celebration = VGroup()
        for i in range(10):
            star = Star(n=5, outer_radius=0.2, color=random.choice([RED, GREEN, BLUE, YELLOW, PURPLE]))
            star.move_to([random.uniform(-6, 6), random.uniform(-3, 3), 0])
            celebration.add(star)
        
        self.play(Create(celebration), run_time=2)
        self.play(FadeOut(celebration), run_time=1)
        
        self.wait(2)

# 渲染命令示例
if __name__ == "__main__":
    # manim scenes_4_8_animations.py CumulantGeneratingFunctionScene_GIF1_CGFDefinition -pql
    # manim scenes_4_8_animations.py GaussianDistributionScene_GIF1_CumulantSimplicity -pql
    # manim scenes_4_8_animations.py ProbabilityReconstructionScene_GIF2_JourneySummary -pql
    pass 