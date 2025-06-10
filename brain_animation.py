from manim import *
# from manim.constants import DEFAULT_FRAME_WIDTH # DEFAULT_FRAME_WIDTH 不存在于此版本
import numpy as np
import scipy.special
import scipy.stats

class MomentScene_tempdisabled(MovingCameraScene):
    def construct(self):
        # Reuse status text from previous scene for consistency
        status_text_obj = Text("", font="Noto Sans CJK SC", font_size=20).to_corner(UP + LEFT) # Consistent font and size
        self.add(status_text_obj)

        # 1. Setup Axes (reused from ProbabilityAndObservablesScene)
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[0, 0.7, 0.1], # MODIFIED Y_RANGE to accommodate t-distribution peak
            axis_config={"include_numbers": True, "font_size": 24},
            x_length=7,
            y_length=4
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="P(x)")
        
        axes_group = VGroup(axes, axes_labels).center()
        self.play(Write(axes_group))
        self.wait(1)

        mean_val = 0
        std_dev_val = 1
        self.play(status_text_obj.animate.become(Text("我们从一个标准高斯分布 P(x) 开始", font="Noto Sans CJK SC", font_size=20).to_corner(UP + LEFT)))
        
        def gaussian_pdf(x_val):
            return (1 / (std_dev_val * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_val - mean_val) / std_dev_val) ** 2)

        pdf_curve = axes.plot(gaussian_pdf, color=BLUE)
        pdf_label = MathTex("P(x)", font_size=36).next_to(pdf_curve, UP, buff=0.2)
        
        self.play(Create(pdf_curve), Write(pdf_label))
        self.wait(1)

        # Animate calculation of the mean
        self.play(status_text_obj.animate.become(Text("现在来看矩。第一个矩是均值 (μ)，描述分布的中心。", font="Noto Sans CJK SC", font_size=20).to_corner(UP + LEFT)))
        mean_line = DashedLine(
            start=axes.c2p(mean_val, 0),
            end=axes.c2p(mean_val, gaussian_pdf(mean_val)),
            color=GREEN
        )
        mean_dot = Dot(axes.c2p(mean_val, gaussian_pdf(mean_val)), color=GREEN)
        mean_label_tex = MathTex("\\mu", font_size=36, color=GREEN).next_to(mean_line, DOWN, buff=0.2)
        mean_text = Text("(Mean)", font="Noto Sans CJK SC", font_size=20, color=GREEN).next_to(mean_label_tex, DOWN, buff=0.1) # Consistent font
        
        self.play(Create(mean_line), Create(mean_dot), Write(mean_label_tex), Write(mean_text))
        self.wait(2)

        # Animate calculation of the variance
        self.play(status_text_obj.animate.become(Text("第二个中心矩是方差 (σ²)，描述分布的离散程度。", font="Noto Sans CJK SC", font_size=20).to_corner(UP + LEFT)))
        variance_area = axes.get_area(
            pdf_curve,
            x_range=(mean_val - std_dev_val, mean_val + std_dev_val),
            color=YELLOW,
            opacity=0.5
        )
        std_dev_line_minus = DashedLine(
            axes.c2p(mean_val - std_dev_val, 0),
            axes.c2p(mean_val - std_dev_val, gaussian_pdf(mean_val - std_dev_val)),
            color=YELLOW_D
        )
        std_dev_line_plus = DashedLine(
            axes.c2p(mean_val + std_dev_val, 0),
            axes.c2p(mean_val + std_dev_val, gaussian_pdf(mean_val + std_dev_val)),
            color=YELLOW_D
        )
        variance_label_tex = MathTex("\\sigma^2", font_size=36, color=YELLOW_D).next_to(variance_area, UP, buff=0.1).align_to(axes.c2p(mean_val,0), RIGHT)
        variance_text = Text("(Variance)", font="Noto Sans CJK SC", font_size=20, color=YELLOW_D).next_to(variance_label_tex, DOWN, buff=0.1) # Consistent font

        self.play(
            FadeIn(variance_area), 
            Create(std_dev_line_minus), 
            Create(std_dev_line_plus),
            Write(variance_label_tex),
            Write(variance_text)
        )
        self.wait(2)

        # --- Start of NEW Skewness and Kurtosis section ---
        mean_variance_visuals = VGroup(
            mean_line, mean_dot, mean_label_tex, mean_text,
            variance_area, std_dev_line_minus, std_dev_line_plus,
            variance_label_tex, variance_text
        )
        self.play(FadeOut(mean_variance_visuals))
        self.wait(0.5)
        self.play(FadeOut(pdf_label)) # Fade out "P(x)" label
        self.wait(0.5)
        
        # --- Skewness Enhanced ---
        new_status_text_skew = Text("三阶矩与偏斜度 (Skewness) 相关", font="Noto Sans CJK SC", font_size=20).to_corner(UP + LEFT)
        self.play(status_text_obj.animate.become(new_status_text_skew))

        def skew_normal_pdf_scipy(x, mu, sigma, alpha):
            return scipy.stats.skewnorm.pdf(x, alpha, loc=mu, scale=sigma)

        # Positive Skew
        alpha_pos = 4
        positive_skew_curve = axes.plot(lambda x: skew_normal_pdf_scipy(x, mean_val, std_dev_val, alpha_pos), color=PURPLE)
        
        pos_skew_label_text = Text("正偏度 (Right Skew)", font="Noto Sans CJK SC", font_size=24, color=PURPLE)
        pos_skew_math = MathTex("\\gamma_1 > 0", font_size=30, color=PURPLE)
        pos_skew_labels = VGroup(pos_skew_label_text, pos_skew_math).arrange(DOWN, buff=0.15).next_to(axes_group, RIGHT, buff=0.3, aligned_edge=UP)

        self.play(Transform(pdf_curve, positive_skew_curve), Write(pos_skew_labels))
        self.wait(2.5)

        # Negative Skew
        alpha_neg = -4
        negative_skew_curve = axes.plot(lambda x: skew_normal_pdf_scipy(x, mean_val, std_dev_val, alpha_neg), color=DARK_BLUE) # Changed color
        
        neg_skew_label_text = Text("负偏度 (Left Skew)", font="Noto Sans CJK SC", font_size=24, color=DARK_BLUE)
        neg_skew_math = MathTex("\\gamma_1 < 0", font_size=30, color=DARK_BLUE)
        neg_skew_labels = VGroup(neg_skew_label_text, neg_skew_math).arrange(DOWN, buff=0.15).next_to(axes_group, RIGHT, buff=0.3, aligned_edge=UP)

        self.play(Transform(pdf_curve, negative_skew_curve), ReplacementTransform(pos_skew_labels, neg_skew_labels))
        self.wait(2.5)

        # Skewness Definition
        new_status_text_skew_def = Text("偏度定义式:", font="Noto Sans CJK SC", font_size=20).to_corner(UP + LEFT)
        self.play(status_text_obj.animate.become(new_status_text_skew_def))
        skew_formula = MathTex(r"\gamma_1 = E\left[ \left( \frac{X-\mu}{\sigma} \right)^3 \right]", font_size=36)
        skew_formula.next_to(neg_skew_labels, DOWN, buff=0.5).align_to(neg_skew_labels, LEFT)
        
        self.play(Write(skew_formula))
        self.wait(3)

        # Transition back to Gaussian for Kurtosis part
        gaussian_curve_ref = axes.plot(gaussian_pdf, color=BLUE) # Original blue
        self.play(
            FadeOut(neg_skew_labels), 
            FadeOut(skew_formula),
            Transform(pdf_curve, gaussian_curve_ref)
        )
        self.wait(1)

        # --- Kurtosis Enhanced ---
        new_status_text_kurt = Text("四阶矩与峰度 (Kurtosis) 相关", font="Noto Sans CJK SC", font_size=20).to_corner(UP + LEFT)
        self.play(status_text_obj.animate.become(new_status_text_kurt))
        
        # Mesokurtic (Normal Kurtosis)
        meso_label_text = Text("正态峰 (Mesokurtic)", font="Noto Sans CJK SC", font_size=24, color=BLUE)
        meso_math = MathTex("\\gamma_2 = 0", font_size=30, color=BLUE) # Excess kurtosis
        meso_labels = VGroup(meso_label_text, meso_math).arrange(DOWN, buff=0.15).next_to(axes_group, RIGHT, buff=0.3, aligned_edge=UP)
        
        self.play(Write(meso_labels))
        self.wait(2)
        
        gaussian_ref_translucent = pdf_curve.copy().set_opacity(0.3)
        self.add(gaussian_ref_translucent) # Add to scene, will stay behind transforming pdf_curve

        # Leptokurtic (Peaked)
        new_status_text_lepto = Text("尖峰 (Leptokurtic): 更尖的峰, 更厚的尾部", font="Noto Sans CJK SC", font_size=20).to_corner(UP + LEFT)
        self.play(status_text_obj.animate.become(new_status_text_lepto))
        df_lepto = 3
        scale_lepto = std_dev_val * np.sqrt((df_lepto - 2) / df_lepto)
        def student_t_pdf(x, df, mu, scale_param):
            return scipy.stats.t.pdf(x, df, loc=mu, scale=scale_param)

        lepto_curve = axes.plot(lambda x: student_t_pdf(x, df_lepto, mean_val, scale_lepto), color=ORANGE)
        
        lepto_label_text = Text("尖峰 (Leptokurtic)", font="Noto Sans CJK SC", font_size=24, color=ORANGE)
        lepto_math = MathTex("\\gamma_2 > 0", font_size=30, color=ORANGE)
        lepto_labels = VGroup(lepto_label_text, lepto_math).arrange(DOWN, buff=0.15).next_to(axes_group, RIGHT, buff=0.3, aligned_edge=UP)

        self.play(Transform(pdf_curve, lepto_curve), ReplacementTransform(meso_labels, lepto_labels))
        self.wait(3)

        # Platykurtic (Flat)
        new_status_text_platy = Text("平峰 (Platykurtic): 更平的峰, 更薄的尾部", font="Noto Sans CJK SC", font_size=20).to_corner(UP + LEFT)
        self.play(status_text_obj.animate.become(new_status_text_platy))
        uniform_a = -np.sqrt(3) * std_dev_val
        uniform_b = np.sqrt(3) * std_dev_val
        pdf_height_uniform = 1 / (uniform_b - uniform_a)

        def uniform_pdf(x):
            if uniform_a <= x <= uniform_b:
                return pdf_height_uniform
            return 0

        platy_curve = axes.plot(uniform_pdf, color=PINK, x_range=[uniform_a - 0.01, uniform_b + 0.01])
        
        platy_label_text = Text("平峰 (Platykurtic)", font="Noto Sans CJK SC", font_size=24, color=PINK)
        platy_math = MathTex("\\gamma_2 < 0", font_size=30, color=PINK)
        platy_labels = VGroup(platy_label_text, platy_math).arrange(DOWN, buff=0.15).next_to(axes_group, RIGHT, buff=0.3, aligned_edge=UP)

        self.play(Transform(pdf_curve, platy_curve), ReplacementTransform(lepto_labels, platy_labels))
        self.wait(3)

        # Kurtosis Definition (Excess Kurtosis)
        new_status_text_kurt_def = Text("峰度 (超额) 定义式:", font="Noto Sans CJK SC", font_size=20).to_corner(UP + LEFT)
        self.play(status_text_obj.animate.become(new_status_text_kurt_def))
        kurtosis_formula = MathTex(r"\gamma_2 = E\left[ \left( \frac{X-\mu}{\sigma} \right)^4 \right] - 3", font_size=36)
        kurtosis_formula.next_to(platy_labels, DOWN, buff=0.5).align_to(platy_labels, LEFT)

        self.play(Write(kurtosis_formula))
        self.wait(3.5)

        # Fade out Kurtosis visuals to prepare for "Misleading Moments"
        kurtosis_visuals = VGroup(pdf_curve, platy_labels, kurtosis_formula, gaussian_ref_translucent)
        self.play(FadeOut(kurtosis_visuals))
        self.wait(1)
        
        # --- END of NEW Skewness and Kurtosis section ---\n

        # --- Misleading Moments: Two different distributions with same mean and variance ---
        self.play(FadeOut(axes_group)) 
        self.wait(0.5)

        common_mean = 0
        common_variance = 1 
        
        shape_g1 = 4
        scale_g1 = 0.5
        loc_g1 = - (shape_g1 * scale_g1) 

        def dist1_pdf(x):
            pdf_val = scipy.stats.gamma.pdf(x, shape_g1, loc=loc_g1, scale=scale_g1)
            return pdf_val
        
        m2_peak_dist = 0.8
        s2_std = 0.6
        def dist2_pdf(x):
            g1 = 0.5 * (1/(s2_std*np.sqrt(2*np.pi))) * np.exp(-0.5*((x - (-m2_peak_dist))/s2_std)**2)
            g2 = 0.5 * (1/(s2_std*np.sqrt(2*np.pi))) * np.exp(-0.5*((x - m2_peak_dist)/s2_std)**2)
            return g1 + g2

        axes_x_range = [-4, 4, 1]
        axes_y_range_mislead = [0, 0.8, 0.1] # Adjusted y_range for these distributions
        axes_common_config = {"include_numbers": True, "font_size": 20}
        axes_length_x = 5
        axes_length_y = 3

        axes1 = Axes(x_range=axes_x_range, y_range=axes_y_range_mislead, axis_config=axes_common_config, x_length=axes_length_x, y_length=axes_length_y)
        axes1_labels = axes1.get_axis_labels(x_label="x", y_label="P(x)")
        dist1_curve = axes1.plot(dist1_pdf, color=RED)
        dist1_title = Text("Distribution A", font_size=24).next_to(axes1, UP)
        dist1_group = VGroup(axes1, axes1_labels, dist1_curve, dist1_title).to_edge(LEFT, buff=0.5)

        axes2 = Axes(x_range=axes_x_range, y_range=axes_y_range_mislead, axis_config=axes_common_config, x_length=axes_length_x, y_length=axes_length_y)
        axes2_labels = axes2.get_axis_labels(x_label="x", y_label="P(x)")
        dist2_curve = axes2.plot(dist2_pdf, color=GREEN)
        dist2_title = Text("Distribution B", font_size=24).next_to(axes2, UP)
        dist2_group = VGroup(axes2, axes2_labels, dist2_curve, dist2_title).to_edge(RIGHT, buff=0.5)

        self.play(LaggedStart(
            Write(dist1_group),
            Write(dist2_group),
            lag_ratio=0.5
        ))
        self.wait(1)

        mean_dist1_val = 0 
        var_dist1_val = 1   
        mean_dist2_val = 0 
        var_dist2_val = 1   

        stats_text_template = "Mean ≈ {:.2f}, Variance ≈ {:.2f}"
        stats1_text = Text(stats_text_template.format(mean_dist1_val, var_dist1_val), font_size=20).next_to(dist1_title, DOWN, buff=0.1)
        stats2_text = Text(stats_text_template.format(mean_dist2_val, var_dist2_val), font_size=20).next_to(dist2_title, DOWN, buff=0.1)

        self.play(Write(stats1_text), Write(stats2_text))
        self.wait(2)
        
        misleading_text = Text("Same Mean & Variance, Different Shapes!", font_size=30, color=YELLOW).to_edge(DOWN, buff=0.5)
        self.play(Write(misleading_text))
        self.wait(3)
        
        # --- Introduce Cumulants (MODIFIED POSITIONING) ---
        new_status_text_cumulant_intro = Text("这就是累积量的用武之地。它提供了描述形状的另一种方式。", font="Noto Sans CJK SC", font_size=20).to_corner(UP + LEFT)
        self.play(status_text_obj.animate.become(new_status_text_cumulant_intro))
        
        self.play(
            FadeOut(dist1_group), FadeOut(dist2_group),
            FadeOut(stats1_text), FadeOut(stats2_text),
            FadeOut(misleading_text)
        )
        self.wait(1)

        cumulants_title = Text("Cumulants (κ)", font_size=40).to_corner(UP + LEFT, buff=0.3)
        self.play(Write(cumulants_title))
        self.wait(1)

        kappa1_text = MathTex("\\kappa_1 = \\text{Mean}", font_size=32)
        kappa2_text = MathTex("\\kappa_2 = \\text{Variance}", font_size=32)
        kappa_higher_text = MathTex("\\kappa_3, \\kappa_4, ...", "\\text{ capture other shape details}", font_size=32)
        
        cumulant_eqs = VGroup(kappa1_text, kappa2_text, kappa_higher_text).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        cumulant_eqs.next_to(cumulants_title, DOWN, buff=0.2).align_to(cumulants_title, LEFT)

        self.play(Write(cumulant_eqs))
        self.wait(3)

        new_status_text_higher_cumulants_diff = Text("高阶累积量能区分这些矩难以区分的形状差异。", font="Noto Sans CJK SC", font_size=20).to_corner(UP + LEFT)
        self.play(status_text_obj.animate.become(new_status_text_higher_cumulants_diff))
        self.wait(0.5)

        self.play(kappa_higher_text[0].animate.set_color(YELLOW), run_time=1)
        self.wait(0.5)

        current_scene_elements = VGroup(cumulants_title, cumulant_eqs, status_text_obj) # status_text_obj also to be moved
        
        dist1_group_small = dist1_group.copy().scale(0.6)
        dist2_group_small = dist2_group.copy().scale(0.6)

        dist_display_group = VGroup(dist1_group_small, dist2_group_small).arrange(RIGHT, buff=1.0)
        # Position distributions in the center, ensure they don't overlap with top-left cumulants
        dist_display_group.center().shift(DOWN*0.5)


        self.play(
            # current_scene_elements remain in topleft
            FadeIn(dist_display_group)
        )
        self.wait(1)
        
        # Arrows pointing from kappa_higher_text to the distributions
        arrow_A_start_point = kappa_higher_text[0].get_right() + RIGHT * 0.2
        arrow_A_target = dist1_group_small.get_top() + DOWN * 0.3 # Point to upper part of dist A

        arrow_B_start_point = kappa_higher_text[0].get_right() + RIGHT * 0.2 # Same start
        arrow_B_target = dist2_group_small.get_top() + DOWN * 0.3 # Point to upper part of dist B
        
        arrow_A = Arrow(arrow_A_start_point, arrow_A_target, buff=0.1, color=RED_E, stroke_width=5, max_tip_length_to_length_ratio=0.15)
        label_A_diff = Text("Different Shape (e.g., Skew)", font_size=18, color=RED_E).next_to(dist1_group_small, DOWN, buff=0.1)

        arrow_B = Arrow(arrow_B_start_point, arrow_B_target, buff=0.1, color=GREEN_E, stroke_width=5, max_tip_length_to_length_ratio=0.15)
        label_B_diff = Text("Different Shape (e.g., Bimodality)", font_size=18, color=GREEN_E).next_to(dist2_group_small, DOWN, buff=0.1)

        self.play(GrowArrow(arrow_A), Write(label_A_diff))
        self.wait(1.5)
        # Instead of transform, fade out A and fade in B for clarity with fixed arrow start
        self.play(FadeOut(arrow_A), FadeOut(label_A_diff))
        self.play(GrowArrow(arrow_B), Write(label_B_diff))
        self.wait(1.5)

        final_message = Text("Higher cumulants (κ₃, κ₄, ...) quantify these distinct features.", font_size=24, color=YELLOW)
        final_message.to_edge(DOWN, buff=0.75)
        self.play(Write(final_message))
        self.wait(4)

        all_elements = VGroup(status_text_obj, current_scene_elements, dist_display_group, arrow_B, label_B_diff, final_message)
        self.play(FadeOut(all_elements))
        self.wait(1)

class IntroScene_tempdisabled(Scene):
    def construct(self):
        # 0. 片头文字
        scene_title = Text("场景 1：概率与可观测量", font="Noto Sans CJK SC", font_size=40).to_edge(UP)
        scene_subtitle = Text("随机性的画像", font="Noto Sans CJK SC", font_size=30, color=BLUE_C).next_to(scene_title, DOWN, buff=0.2)
        self.play(Write(scene_title), Write(scene_subtitle))
        self.wait(1)
        self.play(FadeOut(scene_title), FadeOut(scene_subtitle))

        # 恢复统一的动态 status_text_obj
        status_text_obj = Text("", font="Noto Sans CJK SC", font_size=20).to_edge(UP)
        self.add(status_text_obj)

        # --- GIF 1: 随机变量概念引入 (新的动画流程) ---
        self.play(status_text_obj.animate.become(Text("想象随机过程，如粒子运动...", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))

        particles = VGroup(*[Dot(radius=0.05, color=BLUE) for _ in range(50)])
        for particle in particles:
            particle.move_to(np.random.uniform(-3, 3, 3)) # Spread particles initially
        
        self.play(LaggedStartMap(FadeIn, particles, lag_ratio=0.1, run_time=1))
        self.wait(0.5)

        # --- Define positions for text blocks ---
        pos_x_group = UP * 2.8 + LEFT * 4.5
        pos_px_group = UP * 2.8 + RIGHT * 4.5
        pos_fx_group = DOWN * 1.5 # Position for f(x) text group

        # 1. Introduce x
        state_x_text_obj = MathTex("x", font_size=48)
        state_x_desc_obj = Text("代表系统状态", font="Noto Sans CJK SC", font_size=24).next_to(state_x_text_obj, DOWN, buff=0.2)
        x_group = VGroup(state_x_text_obj, state_x_desc_obj).move_to(pos_x_group)
        self.play(Write(x_group))
        self.wait(1)

        # 2. Introduce x in R^N with particle "变换排列" animation
        self.play(status_text_obj.animate.become(Text("每个状态是一个N维向量: x ∈ R^N", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))
        
        state_vector_text_obj = MathTex("x \\in \\mathbb{R}^N", font_size=48)
        state_vector_desc_obj = Text("(N维向量)", font="Noto Sans CJK SC", font_size=24).next_to(state_vector_text_obj, DOWN, buff=0.2)
        x_in_RN_group = VGroup(state_vector_text_obj, state_vector_desc_obj).move_to(pos_x_group)

        # Particle animation: arrange into a line
        num_particles = len(particles)
        line_length = 6 # Length of the line the particles will form
        line_y_position = 0 # y-coordinate for the horizontal line
        start_x = -line_length / 2
        end_x = line_length / 2

        line_up_animations = []
        if num_particles > 0: # Ensure particles exist
            for i, particle in enumerate(particles):
                target_x = np.linspace(start_x, end_x, num_particles)[i]
                target_position = np.array([target_x, line_y_position, 0])
                line_up_animations.append(
                    particle.animate.set_opacity(1.0).move_to(target_position)
                )
            anim_line_up_final = LaggedStart(*line_up_animations, lag_ratio=0.02, run_time=1.5)
        else:
            anim_line_up_final = Wait(0) # If no particles, do nothing for this part

        # Play animations
        if line_up_animations: # Check if there are actual animations to play for particles
            self.play(
                ReplacementTransform(x_group, x_in_RN_group), # Text transforms
                anim_line_up_final, # Particles arrange into a line
                run_time=1.5
            )
        else: # Only play text transform if no particle animations
            self.play(
                ReplacementTransform(x_group, x_in_RN_group),
                run_time=1.5
            )
        self.wait(1.5) # x_in_RN_group is now on screen

        # 3. Introduce p(x) (Probability Density)
        self.play(status_text_obj.animate.become(Text("p(x) 描述状态x的概率密度...", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))
        prob_density_text_obj = MathTex("p(x)", font_size=60, color=YELLOW)
        prob_density_desc_obj = Text("概率密度", font="Noto Sans CJK SC", font_size=24).next_to(prob_density_text_obj, DOWN, buff=0.2)
        px_group = VGroup(prob_density_text_obj, prob_density_desc_obj).move_to(pos_px_group)
        self.play(GrowFromPoint(px_group, x_in_RN_group.get_center())) # MODIFIED ANIMATION
        self.wait(1)
        
        # 4. Introduce f(x) (Observable) briefly, linking to a "point" (state x)
        self.play(status_text_obj.animate.become(Text("f(x) 是对特定状态x的一次测量 (可观测量)...", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))
        
        pos_fx_group = DOWN * 1.5 # Position for f(x) text group

        # Create a distinct highlighted dot for f(x) explanation
        # Position it centrally or near where f(x) text will appear
        highlighted_particle_for_fx = Dot(ORIGIN + DOWN * 0.5, color=RED, radius=0.1).set_stroke(WHITE, width=2)
        
        observable_f_text_obj = MathTex("f(x)", font_size=48, color=ORANGE)
        observable_f_desc_obj = Text("一个可观测量", font="Noto Sans CJK SC", font_size=24).next_to(observable_f_text_obj, DOWN, buff=0.2)
        fx_group = VGroup(observable_f_text_obj, observable_f_desc_obj)
        fx_group.move_to(np.array([x_in_RN_group.get_center()[0], pos_fx_group[1], 0]))
        
        highlighted_particle_for_fx.next_to(fx_group, UP, buff=0.5) # Position above fx text

        self.play(
            GrowFromCenter(highlighted_particle_for_fx),
            Write(fx_group)
        )
        self.wait(2)

        # ADDED: Arrow from particle line to f(x)
        arrow_to_fx = None 
        if particles and len(particles) > 0:
            arrow_to_fx = Arrow(
                start=particles.get_center(), 
                end=highlighted_particle_for_fx.get_center(),
                buff=0.1,
                color=WHITE,
                stroke_width=4, 
                max_tip_length_to_length_ratio=0.15 
            )
            self.play(GrowArrow(arrow_to_fx))
            self.wait(1) 

        # NEW: Explanation for p(f(x)) or p(x_i)
        self.play(status_text_obj.animate.become(Text("我们通常关注这个可观测量的概率分布 p(f(x))", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))
        
        p_fx_text_obj = MathTex("p(f(x))", font_size=48, color=GREEN)
        p_fx_desc_obj = Text("可观测量的概率分布", font="Noto Sans CJK SC", font_size=24).next_to(p_fx_text_obj, DOWN, buff=0.2)
        p_fx_group = VGroup(p_fx_text_obj, p_fx_desc_obj)
        p_fx_group.move_to(np.array([px_group.get_center()[0], fx_group.get_center()[1], 0]))

        self.play(Write(p_fx_group))
        self.wait(2.5)

        # Original particle dynamics and fade out logic
        # 5. Particles continue moving with symbols present (x_in_RN, p(x), f(x) and p(f(x)) now)
        def update_particles_dynamic(mobj, dt):
            for particle_obj in mobj: 
                particle_obj.shift(np.random.uniform(-0.1, 0.1, 3) * dt * 2.5) 
                center_pos = particle_obj.get_center()
                if abs(center_pos[0]) > 5 or abs(center_pos[1]) > 3: 
                    particle_obj.move_to(np.random.uniform(-2, 2, 3))
        
        if particles:
            particles.add_updater(update_particles_dynamic)
            self.wait(3) 
            particles.remove_updater(update_particles_dynamic)
        else:
            self.wait(3)
        
        # 6. Fade out everything from this introductory segment
        elements_to_fade = VGroup(x_in_RN_group, px_group, fx_group, p_fx_group, highlighted_particle_for_fx)
        if particles:
            elements_to_fade.add(particles)
        if arrow_to_fx:
            elements_to_fade.add(arrow_to_fx)
            
        self.play(FadeOut(elements_to_fade))
        self.wait(0.5)

class IntroScene_GIF1(Scene):
    def construct(self):
        # 0. 片头文字
        scene_title = Text("场景 1：概率与可观测量", font="Noto Sans CJK SC", font_size=40).to_edge(UP)
        scene_subtitle = Text("随机性的画像", font="Noto Sans CJK SC", font_size=30, color=BLUE_C).next_to(scene_title, DOWN, buff=0.2)
        self.play(Write(scene_title), Write(scene_subtitle))
        self.wait(1)
        self.play(FadeOut(scene_title), FadeOut(scene_subtitle))

        # 恢复统一的动态 status_text_obj
        status_text_obj = Text("", font="Noto Sans CJK SC", font_size=20).to_edge(UP)
        self.add(status_text_obj)

        # --- GIF 1: 随机变量概念引入 (新的动画流程) ---
        self.play(status_text_obj.animate.become(Text("想象随机过程，如粒子运动...", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))

        particles = VGroup(*[Dot(radius=0.05, color=BLUE) for _ in range(50)])
        for particle in particles:
            particle.move_to(np.random.uniform(-3, 3, 3)) # Spread particles initially
        
        self.play(LaggedStartMap(FadeIn, particles, lag_ratio=0.1, run_time=1))
        self.wait(0.5)

        # --- Define positions for text blocks ---
        pos_x_group = UP * 2.8 + LEFT * 4.5
        pos_px_group = UP * 2.8 + RIGHT * 4.5
        pos_fx_group = DOWN * 1.5 # Position for f(x) text group

        # 1. Introduce x
        state_x_text_obj = MathTex("x", font_size=48)
        state_x_desc_obj = Text("代表系统状态", font="Noto Sans CJK SC", font_size=24).next_to(state_x_text_obj, DOWN, buff=0.2)
        x_group = VGroup(state_x_text_obj, state_x_desc_obj).move_to(pos_x_group)
        self.play(Write(x_group))
        self.wait(1)

        # 2. Introduce x in R^N with particle "变换排列" animation
        self.play(status_text_obj.animate.become(Text("每个状态是一个N维向量: x ∈ R^N", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))
        
        state_vector_text_obj = MathTex("x \\in \\mathbb{R}^N", font_size=48)
        state_vector_desc_obj = Text("(N维向量)", font="Noto Sans CJK SC", font_size=24).next_to(state_vector_text_obj, DOWN, buff=0.2)
        x_in_RN_group = VGroup(state_vector_text_obj, state_vector_desc_obj).move_to(pos_x_group)

        # Particle animation: arrange into a line
        num_particles = len(particles)
        line_length = 6 # Length of the line the particles will form
        line_y_position = 0 # y-coordinate for the horizontal line
        start_x = -line_length / 2
        end_x = line_length / 2

        line_up_animations = []
        if num_particles > 0: # Ensure particles exist
            for i, particle in enumerate(particles):
                target_x = np.linspace(start_x, end_x, num_particles)[i]
                target_position = np.array([target_x, line_y_position, 0])
                line_up_animations.append(
                    particle.animate.set_opacity(1.0).move_to(target_position)
                )
            anim_line_up_final = LaggedStart(*line_up_animations, lag_ratio=0.02, run_time=1.5)
        else:
            anim_line_up_final = Wait(0) # If no particles, do nothing for this part

        # Play animations
        if line_up_animations: # Check if there are actual animations to play for particles
            self.play(
                ReplacementTransform(x_group, x_in_RN_group), # Text transforms
                anim_line_up_final, # Particles arrange into a line
                run_time=1.5
            )
        else: # Only play text transform if no particle animations
            self.play(
                ReplacementTransform(x_group, x_in_RN_group),
                run_time=1.5
            )
        self.wait(1.5) # x_in_RN_group is now on screen

        # 3. Introduce p(x) (Probability Density)
        self.play(status_text_obj.animate.become(Text("p(x) 描述状态x的概率密度...", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))
        prob_density_text_obj = MathTex("p(x)", font_size=60, color=YELLOW)
        prob_density_desc_obj = Text("概率密度", font="Noto Sans CJK SC", font_size=24).next_to(prob_density_text_obj, DOWN, buff=0.2)
        px_group = VGroup(prob_density_text_obj, prob_density_desc_obj).move_to(pos_px_group)
        self.play(GrowFromPoint(px_group, x_in_RN_group.get_center())) # MODIFIED ANIMATION
        self.wait(1)
        
        # 4. Introduce f(x) (Observable) briefly, linking to a "point" (state x)
        self.play(status_text_obj.animate.become(Text("f(x) 是对特定状态x的一次测量 (可观测量)...", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))
        
        pos_fx_group = DOWN * 1.5 # Position for f(x) text group

        # Create a distinct highlighted dot for f(x) explanation
        # Position it centrally or near where f(x) text will appear
        highlighted_particle_for_fx = Dot(ORIGIN + DOWN * 0.5, color=RED, radius=0.1).set_stroke(WHITE, width=2)
        
        observable_f_text_obj = MathTex("f(x)", font_size=48, color=ORANGE)
        observable_f_desc_obj = Text("一个可观测量", font="Noto Sans CJK SC", font_size=24).next_to(observable_f_text_obj, DOWN, buff=0.2)
        fx_group = VGroup(observable_f_text_obj, observable_f_desc_obj)
        fx_group.move_to(np.array([x_in_RN_group.get_center()[0], pos_fx_group[1], 0]))
        
        highlighted_particle_for_fx.next_to(fx_group, UP, buff=0.5) # Position above fx text

        self.play(
            GrowFromCenter(highlighted_particle_for_fx),
            Write(fx_group)
        )
        self.wait(2)

        # ADDED: Arrow from particle line to f(x)
        arrow_to_fx = None 
        if particles and len(particles) > 0:
            arrow_to_fx = Arrow(
                start=particles.get_center(), 
                end=highlighted_particle_for_fx.get_center(),
                buff=0.1,
                color=WHITE,
                stroke_width=4, 
                max_tip_length_to_length_ratio=0.15 
            )
            self.play(GrowArrow(arrow_to_fx))
            self.wait(1) 

        # NEW: Explanation for p(f(x)) or p(x_i)
        self.play(status_text_obj.animate.become(Text("我们通常关注这个可观测量的概率分布 p(f(x))", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))
        
        p_fx_text_obj = MathTex("p(f(x))", font_size=48, color=GREEN)
        p_fx_desc_obj = Text("可观测量的概率分布", font="Noto Sans CJK SC", font_size=24).next_to(p_fx_text_obj, DOWN, buff=0.2)
        p_fx_group = VGroup(p_fx_text_obj, p_fx_desc_obj)
        p_fx_group.move_to(np.array([px_group.get_center()[0], fx_group.get_center()[1], 0]))

        self.play(Write(p_fx_group))
        self.wait(2.5)

        # Original particle dynamics and fade out logic
        # 5. Particles continue moving with symbols present (x_in_RN, p(x), f(x) and p(f(x)) now)
        def update_particles_dynamic(mobj, dt):
            for particle_obj in mobj: 
                particle_obj.shift(np.random.uniform(-0.1, 0.1, 3) * dt * 2.5) 
                center_pos = particle_obj.get_center()
                if abs(center_pos[0]) > 5 or abs(center_pos[1]) > 3: 
                    particle_obj.move_to(np.random.uniform(-2, 2, 3))
        
        if particles:
            particles.add_updater(update_particles_dynamic)
            self.wait(3) 
            particles.remove_updater(update_particles_dynamic)
        else:
            self.wait(3)
        
        # 6. Fade out everything from this introductory segment
        elements_to_fade = VGroup(x_in_RN_group, px_group, fx_group, p_fx_group, highlighted_particle_for_fx)
        if particles:
            elements_to_fade.add(particles)
        if arrow_to_fx:
            elements_to_fade.add(arrow_to_fx)
            
        self.play(FadeOut(elements_to_fade))
        self.wait(0.5)

class IntroScene_GIF2(Scene):
    def construct(self):
        # 恢复统一的动态 status_text_obj
        status_text_obj = Text("", font="Noto Sans CJK SC", font_size=20).to_edge(UP)
        self.add(status_text_obj)
        
        # --- New Data to PDF Sequence ---
        
        # 1. Setup Axes and Plotting Area
        self.play(status_text_obj.animate.become(Text("我们将分析可观测量的测量数据...", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))
        
        # Define parameters for data and axes
        data_mean = 5
        data_std_dev = 1.5
        axes_x_min, axes_x_max = 0, 10
        
        # Calculate a suitable y_range for the PDF and histogram visualization
        pdf_peak_value = 1 / (data_std_dev * np.sqrt(2 * np.pi))
        axes_y_max_data_units = pdf_peak_value * 1.2 # Add some headroom
        
        axes = Axes(
            x_range=[axes_x_min, axes_x_max, 1], 
            y_range=[0, axes_y_max_data_units, pdf_peak_value / 2],
            x_length=7,
            y_length=3.5,
            axis_config={"include_numbers": True, "font_size": 20}
        )
        axes_labels = axes.get_axis_labels(x_label="f(x)", y_label="p(f(x))")
        axes_group = VGroup(axes, axes_labels)

        axes_group.to_edge(UP, buff=0.8)
                                        
        self.play(Create(axes_group))
        self.wait(0.5)

        # Initial batch of data points
        self.play(status_text_obj.animate.become(Text("屏幕上出现大量数据点...", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))
        num_initial_points = 50
        initial_data_x = np.random.normal(data_mean, data_std_dev, num_initial_points)
        initial_data_x = np.clip(initial_data_x, axes_x_min, axes_x_max)
        
        initial_dots = VGroup()
        initial_dots_target_positions = []
        start_y_world_initial = axes.get_top()[1] + 0.8

        for x_val in initial_data_x:
            dot_target_y_on_axes = axes.y_range[0] + 0.01 * axes_y_max_data_units
            target_pos_world = axes.c2p(x_val, dot_target_y_on_axes)
            initial_dots_target_positions.append(target_pos_world)

            start_x_world = target_pos_world[0]
            dot = Dot(np.array([start_x_world, start_y_world_initial, 0]), color=TEAL_A, radius=0.04)
            initial_dots.add(dot)
        
        # Create drop animations for initial_dots
        initial_drop_animations = []
        if initial_dots:
            for i, dot_obj in enumerate(initial_dots):
                initial_drop_animations.append(
                    AnimationGroup(
                        dot_obj.animate(run_time=0.3, rate_func=rush_into).move_to(initial_dots_target_positions[i]),
                    )
                )
        
        # Play drop animations for initial_dots
        if initial_drop_animations:
            self.play(LaggedStart(*initial_drop_animations, lag_ratio=0.02, run_time=2))
        self.wait(1)

        # 2. Vertical Bin Lines (Minimalist Histogram)
        self.play(status_text_obj.animate.become(Text("这些点代表了多次测量活动值...", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))
        
        bin_width = 1.0
        bins = np.arange(axes_x_min, axes_x_max + bin_width, bin_width)
        counts_initial, _ = np.histogram(initial_data_x, bins=bins, range=(axes_x_min, axes_x_max))
        
        density_initial = counts_initial / (num_initial_points * bin_width)
        
        histogram_lines = VGroup()
        for i in range(len(density_initial)):
            bin_center_x = (bins[i] + bins[i+1]) / 2
            line_height_data_units = density_initial[i]
            line_height_data_units = min(line_height_data_units, axes.y_range[1] * 0.95)

            if line_height_data_units > 0:
                line = Line(
                    start=axes.c2p(bin_center_x, axes.y_range[0]),
                    end=axes.c2p(bin_center_x, line_height_data_units),
                    stroke_color=BLUE_B,
                    stroke_width=15 
                )
                histogram_lines.add(line)
        
        if len(histogram_lines) > 0:
            self.play(LaggedStartMap(Create, histogram_lines, lag_ratio=0.1, run_time=1.5))
        self.wait(1)

        # 3. More Data Points & Line Growth
        self.play(status_text_obj.animate.become(Text("...随着测量次数增加，数据点越来越多...", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))
        num_additional_points = 450
        additional_data_x = np.random.normal(data_mean, data_std_dev, num_additional_points)
        additional_data_x = np.clip(additional_data_x, axes_x_min, axes_x_max)
        
        additional_dots = VGroup()
        additional_dots_target_positions = []
        start_y_world = axes.get_top()[1] + 0.8

        for x_val in additional_data_x:
            dot_target_y_on_axes = axes.y_range[0] + 0.01 * axes_y_max_data_units 
            target_pos_world = axes.c2p(x_val, dot_target_y_on_axes)
            additional_dots_target_positions.append(target_pos_world)

            start_x_world = target_pos_world[0]
            dot = Dot(np.array([start_x_world, start_y_world, 0]), color=TEAL_B, radius=0.04)
            additional_dots.add(dot)
        
        all_data_x_combined = np.concatenate([initial_data_x, additional_data_x])
        total_points = len(all_data_x_combined)
        counts_final, _ = np.histogram(all_data_x_combined, bins=bins, range=(axes_x_min, axes_x_max))
        density_final = counts_final / (total_points * bin_width)

        new_lines_animations = []
        if len(histogram_lines) == len(density_final):
            for i, line in enumerate(histogram_lines):
                bin_center_x_val = axes.p2c(line.get_start())[0]
                new_height_data_units = density_final[i]
                new_height_data_units = min(new_height_data_units, axes.y_range[1] * 0.95)

                if new_height_data_units > 0:
                    new_lines_animations.append(
                        line.animate.put_start_and_end_on(
                            axes.c2p(bin_center_x_val, axes.y_range[0]),
                            axes.c2p(bin_center_x_val, new_height_data_units)
                        )
                    )
                else:
                    new_lines_animations.append(FadeOut(line))
        
        elif len(histogram_lines) == 0 and len(density_final) > 0:
            new_histogram_lines = VGroup()
            for i in range(len(density_final)):
                bin_center_x = (bins[i] + bins[i+1]) / 2
                line_height_data_units = density_final[i]
                line_height_data_units = min(line_height_data_units, axes.y_range[1] * 0.95)
                if line_height_data_units > 0:
                    line = Line(
                        start=axes.c2p(bin_center_x, axes.y_range[0]),
                        end=axes.c2p(bin_center_x, line_height_data_units),
                        stroke_color=BLUE_B, stroke_width=15
                    )
                    new_histogram_lines.add(line)
            if len(new_histogram_lines) > 0:
                 new_lines_animations.append(LaggedStartMap(Create, new_histogram_lines, lag_ratio=0.1))
                 histogram_lines = new_histogram_lines

        # Create drop animations for dots
        drop_animations = []
        if additional_dots:
            for i, dot in enumerate(additional_dots):
                drop_animations.append(
                    AnimationGroup(
                        dot.animate(run_time=0.3, rate_func=rush_into).move_to(additional_dots_target_positions[i]),
                    )
                )

        if len(new_lines_animations) > 0:
            self.play(
                LaggedStart(*drop_animations, lag_ratio=0.005, run_time=2.5),
                LaggedStart(*new_lines_animations, lag_ratio=0.05, run_time=2)
            )
        elif drop_animations:
             self.play(LaggedStart(*drop_animations, lag_ratio=0.005, run_time=2.5))

        all_dots = VGroup(initial_dots, additional_dots)
        self.wait(1)

        # 4. Smoothing Lines to PDF
        self.play(status_text_obj.animate.become(Text("...条形逐渐平滑，最终浮现出概率密度函数的形状。", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))
        
        pdf_curve_final = axes.plot(
            lambda x_val: (1/(data_std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_val - data_mean) / data_std_dev) ** 2),
            color=RED,
            x_range=[axes_x_min, axes_x_max]
        )
        
        if len(histogram_lines) > 0:
            self.play(
                FadeOut(all_dots, run_time=1),
                Transform(histogram_lines, pdf_curve_final, run_time=2)
            )
            pdf_mobject_on_screen = histogram_lines
        else:
            self.play(
                FadeOut(all_dots, run_time=1),
                Create(pdf_curve_final, run_time=2)
            )
            pdf_mobject_on_screen = pdf_curve_final
        
        self.wait(1)

        # Fade out everything
        self.play(
            FadeOut(axes_group),
            FadeOut(pdf_mobject_on_screen),
            FadeOut(status_text_obj)
        )
        self.wait(0.5)

class IntroScene_GIF3(Scene):
    def construct(self):
        # 恢复统一的动态 status_text_obj
        status_text_obj = Text("", font="Noto Sans CJK SC", font_size=20).to_edge(UP)
        self.add(status_text_obj)

        # --- PDF Properties ---
        self.play(status_text_obj.animate.become(Text("PDF 定义与性质...", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))
        
        # 定义高斯PDF函数和相关参数
        data_mean = 5
        data_std_dev = 1.5
        pdf_peak_value = 1 / (data_std_dev * np.sqrt(2 * np.pi))
        axes_y_max_data_units = pdf_peak_value * 1.2

        def gaussian_pdf(x_val):
            return (1 / (data_std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_val - data_mean) / data_std_dev) ** 2)

        # Setup axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, axes_y_max_data_units, pdf_peak_value / 2],
            x_length=7,
            y_length=3.5,
            axis_config={"include_numbers": True, "font_size": 20}
        )
        axes_labels = axes.get_axis_labels(x_label="f(x)", y_label="p(f(x))")
        axes_group = VGroup(axes, axes_labels)
        axes_group.to_edge(UP, buff=0.8)
        
        self.play(Create(axes_group))
        self.wait(0.5)

        # Create PDF curve
        pdf_curve = axes.plot(gaussian_pdf, color=RED)
        self.play(Create(pdf_curve))
        self.wait(1)

        # 添加垂直分区线
        vertical_lines = VGroup()
        num_divisions = 20
        x_step = (10 - 0) / num_divisions
        for i in range(num_divisions + 1):
            x_val = 0 + i * x_step
            line = Line(
                start=axes.c2p(x_val, axes.y_range[0]),
                end=axes.c2p(x_val, axes.y_range[1] * 0.8),
                color=GRAY,
                stroke_width=1
            )
            line.scale(0, about_point=line.get_start())
            vertical_lines.add(line)
        
        self.play(LaggedStartMap(
            lambda m: m.animate.scale(1, about_point=m.get_start()),
            vertical_lines,
            lag_ratio=0.05,
            run_time=2
        ))
        self.wait(0.5)

        # 在曲线上选取一个点（选择在均值处，即x=5）
        y_val = 5
        y_point = Dot(
            axes.c2p(y_val, gaussian_pdf(y_val)),
            color=RED,
            radius=0.08
        )
        y_line = DashedLine(
            start=axes.c2p(y_val, axes.y_range[0]),
            end=y_point.get_center(),
            color=RED_A,
            stroke_width=2
        )
        y_label = MathTex("y", color=RED).next_to(axes.c2p(y_val, axes.y_range[0]), DOWN)
        py_label = MathTex("p(y)", color=RED).next_to(y_point, RIGHT)

        self.play(
            Create(y_line),
            GrowFromCenter(y_point),
            Write(y_label),
            Write(py_label)
        )
        self.wait(1)

        formula_pdf_text = MathTex(r"p(y) = \langle \delta(x-y) \rangle_x", font_size=40)
        explanation_pdf = Text("系统处于状态y附近的概率", font="Noto Sans CJK SC", font_size=24)
        
        pdf_expl_group = VGroup(formula_pdf_text, explanation_pdf).arrange(DOWN, buff=0.2)
        pdf_expl_group.next_to(py_label, RIGHT, buff=1.0)
        
        formula_integral = MathTex(r"\int p(x)dx = 1", font_size=40)
        explanation_integral_text = Text("总概率为1", font="Noto Sans CJK SC", font_size=24)
        
        integral_expl_group = VGroup(formula_integral, explanation_integral_text).arrange(DOWN, buff=0.2)
        integral_expl_group.move_to(axes.c2p(5, gaussian_pdf(5) * 0.5))

        area_under_curve = axes.get_area(
             pdf_curve, 
             x_range=[0, 10],
            color=YELLOW,
            opacity=0.5
        ).set_z_index(-1)

        self.play(
            Write(pdf_expl_group),
            Write(integral_expl_group),
            FadeIn(area_under_curve),
            run_time=2
        )
        self.wait(2)

        # Fade out everything
        mobjects_to_fade = [axes_group, pdf_curve, pdf_expl_group, integral_expl_group, area_under_curve, 
                          vertical_lines, y_line, y_point, y_label, py_label]
        self.play(FadeOut(*[mob for mob in mobjects_to_fade if mob in self.mobjects]))
        self.wait(0.5)

class TaylorExpansionScene(Scene):
    def construct(self):
        # 设置标题
        title = Text("泰勒展开与矩", font="Noto Sans CJK SC", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 创建坐标系 - 进一步缩小并移到右侧
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-1, 4, 1],
            x_length=5,  # 进一步减小坐标轴长度
            y_length=3.5,  # 进一步减小坐标轴长度
            axis_config={"include_numbers": True}
        ).scale(0.7)  # 整体缩放
        
        # 将坐标系移到右侧
        axes_group = VGroup(axes)
        axes_group.shift(RIGHT * 3.5)  # 稍微往右移动一点
        
        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        axes_group.add(axes_labels)
        
        # 首先只显示空白坐标系
        self.play(
            Create(axes),
            Create(axes_labels)
        )
        self.wait(1)

        # 创建原函数 f(x) = x^2
        def f(x):
            return x**2
            
        original_function = axes.plot(f, color=BLUE)
        
        # 泰勒展开公式（分步显示）- 放在左侧，添加颜色
        taylor_expansion = MathTex(
            "f(x)", "&=", 
            "\\underbrace{f(0)}_{c}", "+", 
            "\\underbrace{f'(0)x}_{l}", "+",
            "\\underbrace{\\frac{f''(0)}{2!}x^2}_{q}", "+",
            "\\frac{f'''(0)}{3!}x^3", "+", "\\cdots",
            font_size=36
        ).shift(LEFT * 3 + UP * 1.5)

        # 设置不同项的颜色
        taylor_expansion[2].set_color(RED)  # 常数项
        taylor_expansion[4].set_color(YELLOW)  # 一阶项
        taylor_expansion[6].set_color(GREEN)  # 二阶项

        # 常数项 f(0)
        self.play(Write(taylor_expansion[:3]))  # f(x) = f(0)
        dot_at_zero = Dot(axes.c2p(0, 0), color=RED)
        constant_term = axes.plot(lambda x: 0, color=RED)
        
        # 用动画强调这个点
        self.play(
            GrowFromCenter(dot_at_zero, scale_factor=2),
            run_time=1
        )
        self.play(
            Create(constant_term),
            Flash(dot_at_zero, color=RED, flash_radius=0.3),
            run_time=1
        )
        self.wait(1)

        # 一阶项 f'(0)x
        self.play(Write(taylor_expansion[3:5]))  # + f'(0)x
        def taylor_1(x):
            return 0 + 0 * x  # f'(0) = 0 for f(x) = x^2
        tangent_line = axes.plot(taylor_1, color=YELLOW)
        
        # 用动画强调切线
        self.play(
            Create(tangent_line),
            constant_term.animate.set_color(YELLOW),
            Flash(dot_at_zero, color=YELLOW, flash_radius=0.3),
            run_time=1.5
        )
        self.wait(1)

        # 二阶项 f''(0)x^2/2!
        self.play(Write(taylor_expansion[5:7]))  # + f''(0)x^2/2!
        def taylor_2(x):
            return x**2  # f''(0) = 2 for f(x) = x^2
        approx_2 = axes.plot(taylor_2, color=GREEN)
        
        # 用动画强调抛物线的出现
        self.play(
            Create(approx_2),
            tangent_line.animate.set_color(GREEN),
            constant_term.animate.set_color(GREEN),
            Flash(dot_at_zero, color=GREEN, flash_radius=0.3),
            run_time=2
        )
        self.wait(1)

        # 显示原函数并与近似对比
        self.play(
            Create(original_function),
            approx_2.animate.set_color(BLUE_A),
            tangent_line.animate.set_color(BLUE_A),
            constant_term.animate.set_color(BLUE_A),
            run_time=2
        )
        self.wait(1)

        # 添加标注说明每一项的贡献 - 放在公式下方对应位置
        term_explanations = VGroup(
            Text("常数项", font="Noto Sans CJK SC", font_size=24, color=RED),
            Text("一阶项", font="Noto Sans CJK SC", font_size=24, color=YELLOW),
            Text("二阶项", font="Noto Sans CJK SC", font_size=24, color=GREEN)
        ).arrange(RIGHT, buff=1.5)
        
        # 将说明文字放在泰勒展开公式下方
        term_explanations.next_to(taylor_expansion, DOWN, buff=0.5)
        term_explanations[0].align_to(taylor_expansion[2], LEFT)  # 对齐常数项
        term_explanations[1].align_to(taylor_expansion[4], LEFT)  # 对齐一阶项
        term_explanations[2].align_to(taylor_expansion[6], LEFT)  # 对齐二阶项
        
        self.play(Write(term_explanations))
        self.wait(1)

        # 期望值公式 - 放在左侧下方
        expectation = MathTex(
            "\\langle f(x) \\rangle", "=", 
            "f(0)", "+", 
            "f'(0)\\langle x \\rangle", "+", 
            "\\frac{f''(0)}{2!}\\langle x^2 \\rangle", "+",
            "\\frac{f'''(0)}{3!}\\langle x^3 \\rangle", "+", "\\cdots",
            font_size=32
        ).shift(LEFT * 3 + DOWN * 2)

        # 设置颜色
        expectation[2].set_color(RED)  # f(0)
        expectation[4].set_color(YELLOW)  # f'(0)⟨x⟩
        expectation[6].set_color(GREEN)  # f''(0)⟨x²⟩/2!

        self.play(Write(expectation))
        self.wait(1)

        # 用方框框住矩符号
        moments = VGroup(
            expectation[4][-3:],  # ⟨x⟩
            expectation[6][-3:],  # ⟨x²⟩
            expectation[8][-3:]   # ⟨x³⟩
        )
        
        moment_boxes = VGroup(*[
            SurroundingRectangle(moment, buff=0.1, color=BLUE)
            for moment in moments
        ])
        
        self.play(
            Create(moment_boxes),
            run_time=2
        )
        self.wait(1)

        # 矩的定义 - 放在最下方
        moment_def = MathTex(
            "\\langle x^n \\rangle = \\int_{-\\infty}^{\\infty} x^n p(x) dx",
            font_size=32
        ).shift(DOWN * 3)

        self.play(Write(moment_def))
        self.wait(2)

        # 淡出所有内容
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        self.wait(1)

        # 添加新的复杂函数示例：f(x) = e^(-x²/4) * cos(2x)
        new_title = Text("复杂函数展开：e^(-x²/4)cos(2x)", font="Noto Sans CJK SC", font_size=40).to_edge(UP)
        self.play(Write(new_title))
        self.wait(1)

        # 创建新的坐标系
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=5,
            y_length=3.5,
            axis_config={"include_numbers": True}
        ).scale(0.7)
        
        axes_group = VGroup(axes)
        axes_group.shift(RIGHT * 3.5)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        axes_group.add(axes_labels)
        
        self.play(Create(axes_group))
        self.wait(1)

        # 原函数
        def f(x):
            return np.exp(-x**2/4) * np.cos(2*x)
            
        original_function = axes.plot(f, color=BLUE)

        # 泰勒展开公式（分步显示）
        taylor_expansion = MathTex(
            "f(x)", "&=", 
            "\\underbrace{1}_{c}", "+",
            "\\underbrace{0x}_{l}", "+",
            "\\underbrace{(-2-\\frac{1}{4})\\frac{x^2}{2!}}_{q}", "+",
            "\\underbrace{0\\frac{x^3}{3!}}_{3}", "+",
            "\\underbrace{(4+\\frac{3}{4})\\frac{x^4}{4!}}_{4}", "+", "\\cdots",
            font_size=32
        ).shift(LEFT * 3 + UP * 1.5)

        # 设置不同项的颜色
        taylor_expansion[2].set_color(RED)      # 常数项
        taylor_expansion[4].set_color(YELLOW)   # 一阶项
        taylor_expansion[6].set_color(GREEN)    # 二阶项
        taylor_expansion[8].set_color(PURPLE)   # 三阶项
        taylor_expansion[10].set_color(ORANGE)  # 四阶项

        # 添加标注
        term_explanations = VGroup(
            Text("常数项", font="Noto Sans CJK SC", font_size=24, color=RED),
            Text("一阶项", font="Noto Sans CJK SC", font_size=24, color=YELLOW),
            Text("二阶项", font="Noto Sans CJK SC", font_size=24, color=GREEN),
            Text("三阶项", font="Noto Sans CJK SC", font_size=24, color=PURPLE),
            Text("四阶项", font="Noto Sans CJK SC", font_size=24, color=ORANGE)
        ).arrange(RIGHT, buff=0.8)
        term_explanations.scale(0.8)  # 缩小文字大小
        term_explanations.next_to(taylor_expansion, DOWN, buff=0.5)

        # 逐项显示泰勒展开
        self.play(Write(taylor_expansion[:3]))  # f(x) = 1
        
        def taylor_0(x):
            return 1
        approx_0 = axes.plot(taylor_0, color=RED)
        self.play(Create(approx_0))
        self.wait(1)

        self.play(Write(taylor_expansion[3:5]))  # + 0x
        def taylor_1(x):
            return 1 + 0*x
        approx_1 = axes.plot(taylor_1, color=YELLOW)
        self.play(
            Transform(approx_0, approx_1),
            run_time=1.5
        )
        self.wait(1)

        self.play(Write(taylor_expansion[5:7]))  # + (-2-1/4)x²/2!
        def taylor_2(x):
            return 1 + 0*x + (-2-1/4)*(x**2)/2
        approx_2 = axes.plot(taylor_2, color=GREEN)
        self.play(
            Transform(approx_0, approx_2),
            run_time=1.5
        )
        self.wait(1)

        self.play(Write(taylor_expansion[7:9]))  # + 0x³/3!
        def taylor_3(x):
            return 1 + 0*x + (-2-1/4)*(x**2)/2 + 0*(x**3)/6
        approx_3 = axes.plot(taylor_3, color=PURPLE)
        self.play(
            Transform(approx_0, approx_3),
            run_time=1.5
        )
        self.wait(1)

        self.play(Write(taylor_expansion[9:]))  # + (4+3/4)x⁴/4!
        def taylor_4(x):
            return 1 + 0*x + (-2-1/4)*(x**2)/2 + 0*(x**3)/6 + (4+3/4)*(x**4)/24
        approx_4 = axes.plot(taylor_4, color=ORANGE)
        self.play(
            Transform(approx_0, approx_4),
            run_time=1.5
        )
        self.wait(1)

        # 显示原函数并与近似对比
        self.play(
            Create(original_function),
            approx_0.animate.set_color(BLUE_A),
            Write(term_explanations),
            run_time=2
        )
        self.wait(2)

        # 添加生物学意义的解释
        bio_meaning = VGroup(
            Text("• v=0: 静息电位", font="Noto Sans CJK SC", font_size=24),
            Text("• v>0: 去极化", font="Noto Sans CJK SC", font_size=24),
            Text("• v<0: 超极化", font="Noto Sans CJK SC", font_size=24),
            Text("• 三阶项提供负反馈", font="Noto Sans CJK SC", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        bio_meaning.scale(0.8)
        bio_meaning.next_to(term_explanations, DOWN, buff=0.5)

        self.play(Write(bio_meaning))
        self.wait(2)

        # 最后淡出所有内容
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        self.wait(1)

        # 添加完整的 HH 方程
        new_title = Text("Hodgkin-Huxley 方程", font="Noto Sans CJK SC", font_size=48).to_edge(UP)
        subtitle = Text("完整模型 vs 简化模型", font="Noto Sans CJK SC", font_size=36).next_to(new_title, DOWN)
        self.play(Write(new_title), Write(subtitle))
        self.wait(1)

        # HH 方程组 - 重新定位和布局
        hh_equations = VGroup(
            MathTex("C_m\\frac{dV}{dt}", "=", "-g_{Na}m^3h(V-E_{Na})", "-g_Kn^4(V-E_K)", "-g_L(V-E_L)", "+I_{ext}", font_size=44),
            MathTex("\\frac{dm}{dt}", "=", "\\alpha_m(V)(1-m)", "-\\beta_m(V)m", font_size=44),
            MathTex("\\frac{dh}{dt}", "=", "\\alpha_h(V)(1-h)", "-\\beta_h(V)h", font_size=44),
            MathTex("\\frac{dn}{dt}", "=", "\\alpha_n(V)(1-n)", "-\\beta_n(V)n", font_size=44)
        ).arrange(DOWN, buff=0.6, aligned_edge=LEFT)  # 增加方程间距
        
        # 将方程组整体向左移动并居中
        hh_equations.move_to(ORIGIN).shift(LEFT * 3 + UP * 0.5)

        # 为不同离子通道添加颜色
        hh_equations[0][2].set_color(YELLOW)  # Na+ 通道
        hh_equations[0][3].set_color(BLUE)    # K+ 通道
        hh_equations[0][4].set_color(GREEN)   # 漏电流
        
        # 添加方程说明 - 调整位置
        explanations = VGroup(
            Text("• Na+ 通道: 快速激活和失活", font="Noto Sans CJK SC", font_size=32, color=YELLOW),
            Text("• K+ 通道: 缓慢激活", font="Noto Sans CJK SC", font_size=32, color=BLUE),
            Text("• 漏电流: 静息电导", font="Noto Sans CJK SC", font_size=32, color=GREEN),
            Text("• m, h, n: 门控变量", font="Noto Sans CJK SC", font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        explanations.next_to(hh_equations, DOWN, buff=0.8)

        self.play(Write(hh_equations))
        self.wait(1)
        self.play(Write(explanations))
        self.wait(1)

        # 时间尺度分离 - 调整位置
        timescale_text = VGroup(
            Text("时间尺度分离：", font="Noto Sans CJK SC", font_size=36),
            Text("• Na+ 通道: ~0.1ms", font="Noto Sans CJK SC", font_size=32),
            Text("• K+ 通道: ~1ms", font="Noto Sans CJK SC", font_size=32),
            Text("• 膜电位: ~1ms", font="Noto Sans CJK SC", font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        # 将时间尺度说明移到右侧
        timescale_text.move_to(ORIGIN).shift(RIGHT * 3 + UP * 1)

        self.play(Write(timescale_text))
        self.wait(1)

        # 显示简化后的FN方程 - 调整位置
        fn_equation = MathTex(
            "\\frac{dv}{dt}", "=", "v - \\frac{v^3}{3} - w + I_{ext}",
            font_size=48
        ).scale(1.2)
        
        # 将FN方程放在时间尺度说明下方
        fn_equation.next_to(timescale_text, DOWN, buff=1.5)

        # 调整箭头，使其从HH方程组指向FN方程
        arrow = Arrow(
            start=hh_equations[1].get_right(),  # 从HH方程组中间指向
            end=fn_equation.get_left(),         # 指向FN方程左侧
            buff=0.3,
            color=WHITE,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15  # 调整箭头头部大小
        )

        self.play(
            GrowArrow(arrow),
            Write(fn_equation)
        )
        self.wait(1)

        # 添加简化说明 - 调整位置
        simplification_notes = VGroup(
            Text("• 合并离子通道动力学", font="Noto Sans CJK SC", font_size=32),
            Text("• 保留关键非线性特征", font="Noto Sans CJK SC", font_size=32),
            Text("• 捕捉兴奋性阈值行为", font="Noto Sans CJK SC", font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        # 将简化说明放在FN方程下方
        simplification_notes.next_to(fn_equation, DOWN, buff=0.8)

        self.play(Write(simplification_notes))
        self.wait(2)

        # 最后淡出所有内容
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        self.wait(1)

config.scene_names = ["IntroScene_GIF1", "IntroScene_GIF2", "IntroScene_GIF3", "TaylorExpansionScene"]

 