from manim import *
import numpy as np

# 场景4：累积量生成函数 - GIF1：CGF定义
class CumulantGeneratingFunctionScene_GIF1_CGFDefinition(Scene):
    def construct(self):
        # 标题
        title = Text("Cumulant Generating Function (CGF) Definition", font_size=32, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # MGF回顾
        mgf_formula = MathTex(r"Z(j) = \langle e^{jx} \rangle")
        mgf_formula.shift(UP * 1.5)
        self.play(Write(mgf_formula))
        
        # CGF定义
        cgf_formula = MathTex(r"K(j) = \ln Z(j) = \ln \langle e^{jx} \rangle")
        cgf_formula.next_to(mgf_formula, DOWN, buff=0.8)
        self.play(Write(cgf_formula))
        
        # 解释文本
        explanation = Text("CGF is the logarithmic transform of MGF", font_size=24, color=YELLOW)
        explanation.next_to(cgf_formula, DOWN, buff=0.8)
        self.play(Write(explanation))
        
        self.wait(2)

# 场景4：累积量生成函数 - GIF2：累积量定义
class CumulantGeneratingFunctionScene_GIF2_CumulantDefinition(Scene):
    def construct(self):
        title = Text("Cumulant Definition", font_size=32, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # CGF泰勒展开
        cgf_expansion = MathTex(r"K(j) = \sum_{n=1}^{\infty} \frac{\kappa_n}{n!} j^n")
        cgf_expansion.shift(UP * 1)
        self.play(Write(cgf_expansion))
        
        # 前几个累积量
        kappa1 = MathTex(r"\kappa_1 = \text{mean}", color=GREEN)
        kappa2 = MathTex(r"\kappa_2 = \text{variance}", color=ORANGE)
        kappa3 = MathTex(r"\kappa_3 = \text{skewness}", color=RED)
        
        kappa1.next_to(cgf_expansion, DOWN, buff=0.5)
        kappa2.next_to(kappa1, DOWN, buff=0.3)
        kappa3.next_to(kappa2, DOWN, buff=0.3)
        
        self.play(Write(kappa1))
        self.play(Write(kappa2))
        self.play(Write(kappa3))
        
        self.wait(2)

# 场景4：累积量生成函数 - GIF3：独立性性质
class CumulantGeneratingFunctionScene_GIF3_IndependenceProperty(Scene):
    def construct(self):
        title = Text("Independence Property of Cumulants", font_size=32, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # 独立随机变量
        independent_text = Text("If X and Y are independent:", font_size=24)
        independent_text.shift(UP * 1.5)
        self.play(Write(independent_text))
        
        # MGF相乘
        mgf_property = MathTex(r"Z_{X+Y}(j) = Z_X(j) \cdot Z_Y(j)")
        mgf_property.next_to(independent_text, DOWN, buff=0.5)
        self.play(Write(mgf_property))
        
        # CGF相加
        cgf_property = MathTex(r"K_{X+Y}(j) = K_X(j) + K_Y(j)", color=GREEN)
        cgf_property.next_to(mgf_property, DOWN, buff=0.5)
        self.play(Write(cgf_property))
        
        # 累积量相加
        cumulant_add = MathTex(r"\kappa_n(X+Y) = \kappa_n(X) + \kappa_n(Y)", color=YELLOW)
        cumulant_add.next_to(cgf_property, DOWN, buff=0.5)
        self.play(Write(cumulant_add))
        
        self.wait(2)

# 场景5：矩-累积量变换 - GIF1：指数展开
class MomentCumulantTransformScene_GIF1_ExponentialExpansion(Scene):
    def construct(self):
        title = Text("Exponential Expansion: Core of Transformation", font_size=28, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # 基本关系
        basic_relation = MathTex(r"Z(j) = e^{K(j)}", font_size=36, color=WHITE)
        basic_relation.shift(UP * 1.5)
        self.play(Write(basic_relation))
        
        # 指数函数展开
        exp_expansion = MathTex(
            r"e^{K(j)} = 1 + K(j) + \frac{K(j)^2}{2!} + \frac{K(j)^3}{3!} + \cdots",
            font_size=24
        )
        exp_expansion.next_to(basic_relation, DOWN, buff=1)
        self.play(Write(exp_expansion))
        
        # K(j)的累积量展开
        k_expansion = MathTex(
            r"K(j) = \sum_n \frac{\kappa_n}{n!} j^n",
            font_size=28, color=GREEN
        )
        k_expansion.next_to(exp_expansion, DOWN, buff=1)
        self.play(Write(k_expansion))
        
        self.wait(2)

# 场景5：矩-累积量变换 - GIF2：低阶转换
class MomentCumulantTransformScene_GIF2_LowOrderConversion(Scene):
    def construct(self):
        title = Text("Low-Order Conversions: Simple and Elegant", font_size=28, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # 转换关系
        conversions = VGroup(
            MathTex(r"m_1 = \kappa_1", font_size=28, color=GREEN),
            MathTex(r"m_2 = \kappa_2 + \kappa_1^2", font_size=24, color=BLUE),
        ).arrange(DOWN, buff=1)
        conversions.shift(UP)
        
        for conv in conversions:
            self.play(Write(conv))
            self.wait(1)
        
        # 解释含义
        explanations = VGroup(
            Text("First moment = First cumulant", font_size=20, color=GREEN),
            Text("Second moment = Variance + Mean²", font_size=20, color=BLUE)
        ).arrange(DOWN, buff=1)
        explanations.next_to(conversions, DOWN, buff=1)
        
        for exp in explanations:
            self.play(Write(exp))
            self.wait(0.8)
        
        self.wait(2)

# 场景6：高斯分布 - GIF1：累积量的简洁性
class GaussianDistributionScene_GIF1_CumulantSimplicity(Scene):
    def construct(self):
        title = Text("Gaussian Distribution: Embodiment of Minimalism", font_size=28, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # 高斯分布的MGF
        mgf_gaussian = MathTex(
            r"Z(j) = e^{j\mu + \frac{1}{2}j^2\sigma^2}",
            font_size=28, color=GREEN
        )
        mgf_gaussian.shift(UP * 1.5)
        self.play(Write(mgf_gaussian))
        
        # CGF
        cgf_gaussian = MathTex(
            r"K(j) = j\mu + \frac{1}{2}j^2\sigma^2",
            font_size=28, color=RED
        )
        cgf_gaussian.next_to(mgf_gaussian, DOWN, buff=1)
        self.play(Write(cgf_gaussian))
        
        # 累积量
        cumulants = VGroup(
            MathTex(r"\kappa_1 = \mu", color=GREEN),
            MathTex(r"\kappa_2 = \sigma^2", color=ORANGE),
            MathTex(r"\kappa_n = 0 \text{ for } n \geq 3", color=RED)
        ).arrange(DOWN, buff=0.3)
        cumulants.next_to(cgf_gaussian, DOWN, buff=1)
        
        for cum in cumulants:
            self.play(Write(cum))
            self.wait(0.5)
        
        self.wait(2)

# 场景6：高斯分布 - GIF2：独特地位
class GaussianDistributionScene_GIF2_GoldenStandard(Scene):
    def construct(self):
        title = Text("Gaussian Distribution: The Golden Standard", font_size=28, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # 创建黄金标准标志
        golden_star = Star(n=5, outer_radius=1, color=GOLD)
        golden_star.set_fill(GOLD, opacity=0.8)
        golden_star.shift(UP * 1)
        self.play(Create(golden_star))
        
        # 高斯特性说明
        properties = VGroup(
            Text("Central Limit Theorem", font_size=20, color=GREEN),
            Text("Maximum Entropy", font_size=20, color=ORANGE),  
            Text("Minimal Cumulants", font_size=20, color=RED),
            Text("Universal Behavior", font_size=20, color=PURPLE)
        ).arrange(DOWN, buff=0.3)
        properties.next_to(golden_star, DOWN, buff=1)
        
        for prop in properties:
            self.play(Write(prop))
            self.wait(0.5)
        
        # 公式回顾
        gaussian_formula = MathTex(
            r"p(x) = \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}",
            font_size=20, color=WHITE
        )
        gaussian_formula.to_edge(DOWN)
        self.play(Write(gaussian_formula))
        
        self.wait(2)

# 场景7：中心极限定理 - GIF1：累积量的标度行为
class CentralLimitTheoremScene_GIF1_CumulantScaling(Scene):
    def construct(self):
        title = Text("Central Limit Theorem: Cumulant Scaling", font_size=28, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # n个独立变量的和
        sum_formula = MathTex(r"S_n = X_1 + X_2 + \cdots + X_n", font_size=28)
        sum_formula.shift(UP * 1.5)
        self.play(Write(sum_formula))
        
        # 累积量的标度
        scaling_relations = VGroup(
            MathTex(r"\kappa_1(S_n) = n\kappa_1", color=GREEN),
            MathTex(r"\kappa_2(S_n) = n\kappa_2", color=ORANGE),
            MathTex(r"\kappa_k(S_n) = n\kappa_k", color=RED)
        ).arrange(DOWN, buff=0.5)
        scaling_relations.next_to(sum_formula, DOWN, buff=1)
        
        for rel in scaling_relations:
            self.play(Write(rel))
            self.wait(0.5)
        
        # 标准化后的行为
        standardized = MathTex(
            r"\text{Standardized: } \frac{S_n - n\mu}{\sqrt{n}\sigma}",
            font_size=24, color=YELLOW
        )
        standardized.next_to(scaling_relations, DOWN, buff=1)
        self.play(Write(standardized))
        
        self.wait(2)

# 场景8：概率密度重构 - GIF1：逆变换
class ProbabilityReconstructionScene_GIF1_InverseTransform(Scene):
    def construct(self):
        title = Text("Probability Density Reconstruction", font_size=28, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # 傅里叶逆变换
        fourier_inverse = MathTex(
            r"p(x) = \frac{1}{2\pi} \int_{-\infty}^{\infty} Z(j) e^{-ijx} dj",
            font_size=24
        )
        fourier_inverse.shift(UP * 1)
        self.play(Write(fourier_inverse))
        
        # CGF形式
        cgf_form = MathTex(
            r"p(x) = \frac{1}{2\pi} \int_{-\infty}^{\infty} e^{K(j) - ijx} dj",
            font_size=24, color=GREEN
        )
        cgf_form.next_to(fourier_inverse, DOWN, buff=1)
        self.play(Write(cgf_form))
        
        # 鞍点方法
        saddle_point = Text("Saddle Point Method for approximation", font_size=20, color=YELLOW)
        saddle_point.next_to(cgf_form, DOWN, buff=1)
        self.play(Write(saddle_point))
        
        self.wait(2)

# 场景8：概率密度重构 - GIF2：旅程总结
class ProbabilityReconstructionScene_GIF2_JourneySummary(Scene):
    def construct(self):
        title = Text("Journey Summary: From Moments to Reconstruction", font_size=24, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # 旅程步骤
        journey_steps = VGroup(
            Text("1. Moments → MGF", font_size=20, color=GREEN),
            Text("2. MGF → CGF (logarithm)", font_size=20, color=ORANGE),
            Text("3. CGF → Cumulants", font_size=20, color=RED),
            Text("4. Independence → Additivity", font_size=20, color=PURPLE),
            Text("5. CLT → Gaussian limit", font_size=20, color=BLUE),
            Text("6. Inverse transform → Reconstruction", font_size=20, color=YELLOW)
        ).arrange(DOWN, buff=0.5)
        journey_steps.shift(UP * 0.5)
        
        for step in journey_steps:
            self.play(Write(step))
            self.wait(0.5)
        
        # 最终总结
        summary = Text("Complete mathematical framework for statistical analysis", 
                      font_size=18, color=WHITE)
        summary.to_edge(DOWN)
        self.play(Write(summary))
        
        self.wait(3) 