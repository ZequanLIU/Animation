from manim import *
# from manim.constants import DEFAULT_FRAME_WIDTH # DEFAULT_FRAME_WIDTH 不存在于此版本
import numpy as np
import scipy.special
import scipy.stats

class IntroScene(Scene):
    def construct(self):
        # 1. 标题动画
        title = Text("第二章：概率、矩与累积量", font="Noto Sans CJK SC", font_size=48)
        subtitle = Text("从微观到宏观的统计描述", font="Noto Sans CJK SC", font_size=36, color=BLUE)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.3)
        title_group.to_edge(UP, buff=0.5)
        
        # 2. 创建动态示例
        def create_distribution_plot():
            axes = Axes(
                x_range=[-1.5, 1.5, 0.5],  # 缩小范围
                y_range=[0, 0.4, 0.1],     # 缩小范围
                axis_config={
                    "include_tip": True,
                    "stroke_width": 1,      # 减小线条宽度
                    "font_size": 12,        # 减小刻度字体
                },
            )
            curve = axes.plot(
                lambda x: np.exp(-x**2/2) / np.sqrt(2*np.pi),
                color=BLUE,
                x_range=[-1.5, 1.5]         # 缩小范围
            )
            return VGroup(axes, curve)
        
        def create_moment_visualization():
            axes = Axes(
                x_range=[-1.5, 1.5, 0.5],   # 缩小范围
                y_range=[-0.4, 0.4, 0.2],   # 缩小范围
                axis_config={
                    "include_tip": True,
                    "stroke_width": 1,      # 减小线条宽度
                    "font_size": 12,        # 减小刻度字体
                },
            )
            
            points = VGroup(*[
                Dot(point=[x, np.random.normal(0, 0.15), 0], color=GREEN, radius=0.02)  # 缩小点的大小
                for x in np.linspace(-1.2, 1.2, 8)  # 缩小范围
            ])
            
            mean_line = DashedLine(
                start=axes.c2p(-1.5, 0, 0),
                end=axes.c2p(1.5, 0, 0),
                color=GREEN_E,
                dash_length=0.05,           # 减小虚线长度
                stroke_width=1              # 减小线条宽度
            )
            
            variance_rect = Rectangle(
                height=0.3,                 # 缩小高度
                width=3,                    # 缩小宽度
                fill_opacity=0.2,
                fill_color=GREEN_E,
                stroke_width=0
            ).move_to(axes.c2p(0, 0, 0))
            
            mean_label = Text("均值", font="Noto Sans CJK SC", font_size=14, color=GREEN_E)
            mean_label.next_to(mean_line, UP, buff=0.05)
            variance_label = Text("方差", font="Noto Sans CJK SC", font_size=14, color=GREEN_E)
            variance_label.next_to(variance_rect, UP, buff=0.05)
            
            return VGroup(axes, points, mean_line, variance_rect, mean_label, variance_label)
        
        def create_cumulant_visualization():
            axes = Axes(
                x_range=[-1.5, 1.5, 0.5],   # 缩小范围
                y_range=[-0.4, 0.4, 0.2],   # 缩小范围
                axis_config={
                    "include_tip": True,
                    "stroke_width": 1,      # 减小线条宽度
                    "font_size": 12,        # 减小刻度字体
                },
            )
            
            points = VGroup(*[
                Dot(point=[x, np.random.normal(0, 0.15), 0], color=YELLOW, radius=0.02)  # 缩小点的大小
                for x in np.linspace(-1.2, 1.2, 8)  # 缩小范围
            ])
            
            curve_points = [
                axes.c2p(x, np.sin(x) * 0.2 + np.random.normal(0, 0.03), 0)  # 缩小振幅和噪声
                for x in np.linspace(-1.2, 1.2, 20)  # 缩小范围
            ]
            curve = VMobject()
            curve.set_points_as_corners(curve_points)
            curve.set_stroke(color=YELLOW, width=1.5)  # 减小线条宽度
            
            feature_dots = VGroup(*[
                Dot(point=curve_points[i], color=RED, radius=0.02)  # 缩小点的大小
                for i in [5, 10, 15]
            ])
            
            feature_label = Text("高阶特征", font="Noto Sans CJK SC", font_size=14, color=RED)
            feature_label.next_to(feature_dots[1], UP, buff=0.05)
            
            return VGroup(axes, points, curve, feature_dots, feature_label)
        
        # 创建示例组
        examples = VGroup(
            create_distribution_plot(),
            create_moment_visualization(),
            create_cumulant_visualization()
        ).arrange(RIGHT, buff=1.2)  # 减小间距
        examples.scale(0.4)  # 进一步缩小整体
        
        # 3. 创建核心概念组
        concepts = VGroup(
            VGroup(
                Text("概率密度", font="Noto Sans CJK SC", font_size=32, color=BLUE),
                Text("描述随机变量的分布", font="Noto Sans CJK SC", font_size=24, color=BLUE_E)
            ).arrange(DOWN, aligned_edge=LEFT),
            VGroup(
                Text("矩", font="Noto Sans CJK SC", font_size=32, color=GREEN),
                Text("描述分布的特征（均值、方差等）", font="Noto Sans CJK SC", font_size=24, color=GREEN_E)
            ).arrange(DOWN, aligned_edge=LEFT),
            VGroup(
                Text("累积量", font="Noto Sans CJK SC", font_size=32, color=YELLOW),
                Text("描述分布的高阶特征", font="Noto Sans CJK SC", font_size=24, color=YELLOW_E)
            ).arrange(DOWN, aligned_edge=LEFT)
        ).arrange(RIGHT, buff=1.2)  # 减小间距
        concepts.scale(0.9)
        
        # 将示例组放在概念组上方
        examples.next_to(concepts, UP, buff=0.2)  # 减小间距
        # 整体居中
        VGroup(examples, concepts).center()
        
        # 动画序列
        # 1. 显示标题
        self.play(
            Write(title),
            run_time=1.5
        )
        self.play(
            Write(subtitle),
            run_time=1
        )
        self.wait(1)
        
        # 2. 显示核心概念
        for concept in concepts:
            self.play(
                LaggedStartMap(
                    FadeIn, concept,
                    lag_ratio=0.3,
                    run_time=1
                )
            )
        self.wait(1)
        
        # 3. 显示动态示例
        for i, example in enumerate(examples):
            if i == 0:  # 概率密度图
                self.play(
                    FadeIn(example[0]),  # 坐标轴
                    run_time=0.5
                )
                self.play(
                    Create(example[1]),  # 曲线
                    run_time=1
                )
            elif i == 1:  # 矩的可视化
                self.play(
                    FadeIn(example[0]),  # 坐标轴
                    run_time=0.5
                )
                self.play(
                    LaggedStartMap(GrowFromCenter, example[1]),  # 数据点
                    run_time=1
                )
                self.play(
                    Create(example[2]),  # 均值线
                    FadeIn(example[3]),  # 方差区域
                    Write(example[4]),   # 均值标签
                    Write(example[5]),   # 方差标签
                    run_time=1
                )
            elif i == 2:  # 累积量的可视化
                self.play(
                    FadeIn(example[0]),  # 坐标轴
                    run_time=0.5
                )
                self.play(
                    LaggedStartMap(GrowFromCenter, example[1]),  # 数据点
                    run_time=1
                )
                self.play(
                    Create(example[2]),  # 累积量曲线
                    run_time=1
                )
                self.play(
                    LaggedStartMap(GrowFromCenter, example[3]),  # 特征点
                    Write(example[4]),   # 特征标签
                    run_time=1
                )
            self.wait(0.5)
        
        # 4. 最终强调
        self.play(
            *[mob.animate.set_opacity(0.3) for mob in self.mobjects if mob != title_group],
            title_group.animate.set_opacity(1),
            run_time=1
        )
        self.play(
            *[mob.animate.set_opacity(1) for mob in self.mobjects],
            run_time=1
        )
        
        # 5. 结束
        self.wait(1)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1.5
        )

class ProbabilityAndObservablesScene(Scene):
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

        # --- GIF 1: 随机变量概念引入 ---
        self.play(status_text_obj.animate.become(Text("想象随机过程，如粒子运动...", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))

        particles = VGroup(*[Dot(radius=0.05, color=BLUE) for _ in range(50)])
        for particle in particles:
            particle.move_to(np.random.uniform(-3, 3, 3))
        
        self.play(LaggedStartMap(FadeIn, particles, lag_ratio=0.1, run_time=1))

        def update_particles(mobj, dt):
            for particle_obj in mobj: 
                particle_obj.shift(np.random.uniform(-0.1, 0.1, 3) * dt * 5)
                if not (-4 < particle_obj.get_x() < 4 and -2.5 < particle_obj.get_y() < 2.5):
                    particle_obj.move_to(np.random.uniform(-3, 3, 3))
        particles.add_updater(update_particles)
        self.add(particles) 
        self.wait(3) 
        particles.remove_updater(update_particles)
        
        self.play(FadeOut(particles)) # 只淡出粒子，status_text_obj 会在下一步更新

        # --- New Data to PDF Sequence (Replaces old GIF 2 and part of GIF 3 logic) ---
        
        # 1. Axes and Initial Data Points
        axes = Axes(
            x_range=[0, 10, 1], y_range=[0, 0.6, 0.1], # Adjusted y_range slightly for potentially taller PDF/lines
            x_length=7, y_length=3, # Made axes slightly larger for clarity in the lower part
            axis_config={"include_numbers": True, "font_size": 20}
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="p(x)")
        axes_group = VGroup(axes, axes_labels)

        self.play(status_text_obj.animate.become(Text("创建坐标系以分析测量数据...", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))
        self.play(Create(axes_group))
        self.wait(0.5)
        # Position axes at the top, and the data/histogram/PDF will be below it.
        self.play(axes_group.animate.to_edge(UP, buff=0.3))
        self.wait(0.5)

        # Define data generation parameters
        mean_data = 5
        std_dev_data = 1.5
        
        # Initial batch of data points
        self.play(status_text_obj.animate.become(Text("屏幕上出现坐标轴上的大量数据点。", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))
        num_initial_points = 150
        initial_data_x = np.random.normal(mean_data, std_dev_data, num_initial_points)
        initial_data_x = np.clip(initial_data_x, axes.x_range[0], axes.x_range[1])
        
        # Position initial points near x-axis, within the designated plotting area (below axes_group)
        plot_area_center_y = axes_group.get_bottom()[1] - 2.0 # Approximate center for plot area below axes
        
        initial_dots = VGroup(*[
            Dot(axes.c2p(x, 0) + DOWN * (1.7 + np.random.uniform(-0.1, 0.1)) , color=TEAL_A, radius=0.025) # Spread out slightly below x-axis line in plot area
            for x in initial_data_x
        ])
        initial_dots.set_opacity(0.7)
        self.play(LaggedStartMap(FadeIn, initial_dots, lag_ratio=0.02, run_time=2))
        self.wait(1)

        # 2. Vertical Bin Lines
        self.play(status_text_obj.animate.become(Text("这些点代表了多次测量神经元活动值...", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))
        
        bin_width = 1.0
        bins = np.arange(axes.x_range[0], axes.x_range[1] + bin_width, bin_width)
        counts_initial, _ = np.histogram(initial_data_x, bins=bins)
        
        max_initial_count = np.max(counts_initial) if len(counts_initial) > 0 else 1
        line_scale_factor = 2.0 / (max_initial_count if max_initial_count > 0 else 1) # Scale lines to fit in y_length=3 roughly

        histogram_lines = VGroup()
        for i in range(len(counts_initial)):
            bin_center_x = (bins[i] + bins[i+1]) / 2
            line_height = counts_initial[i] * line_scale_factor
            line = Line(
                start=axes.c2p(bin_center_x, 0) + DOWN * 1.7, # Start at x-axis level in plot area
                end=axes.c2p(bin_center_x, line_height) + DOWN * 1.7, # Extend upwards
                stroke_color=BLUE_B,
                stroke_width=15 # Make lines thick enough to look like bars
            )
            histogram_lines.add(line)
        
        self.play(LaggedStartMap(Create, histogram_lines, lag_ratio=0.1, run_time=1.5))
        self.wait(1)

        # 3. More Data Points & Line Growth
        self.play(status_text_obj.animate.become(Text("...随着测量次数增加，数据点越来越多...", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))
        num_additional_points = 350
        additional_data_x = np.random.normal(mean_data, std_dev_data, num_additional_points)
        additional_data_x = np.clip(additional_data_x, axes.x_range[0], axes.x_range[1])
        
        additional_dots = VGroup(*[
            Dot(axes.c2p(x, 0) + DOWN * (1.7 + np.random.uniform(-0.1, 0.1)), color=TEAL_B, radius=0.025)
            for x in additional_data_x
        ])
        additional_dots.set_opacity(0.7)

        all_data_x = np.concatenate([initial_data_x, additional_data_x])
        counts_final, _ = np.histogram(all_data_x, bins=bins)
        max_final_count = np.max(counts_final) if len(counts_final) > 0 else 1
        # Adjust line_scale_factor if total counts exceed previous assumptions, or keep fixed to show relative increase
        final_line_scale_factor = 2.0 / (max_final_count if max_final_count > 0 else 1)


        new_lines_animations = []
        for i, line in enumerate(histogram_lines):
            old_end = line.get_end()
            new_height = counts_final[i] * final_line_scale_factor
            new_end_y = new_height # y-value in axes's scale
            # Ensure new_end_y doesn't exceed the plotting area too much
            # new_end_y = min(new_end_y, axes.y_range[1]*0.8) # Cap height if needed
            
            # Target point in screen coordinates for the top of the line
            target_point = axes.c2p(line.get_start()[0], 0) + UP * new_height + DOWN*1.7 # line.get_start()[0] is screen x
                                                                                         # for axes.c2p to work correctly with x from screen, need to convert
            bin_center_x_val = axes.p2c(line.get_start())[0] # Convert screen point back to axes value

            new_lines_animations.append(
                line.animate.put_start_and_end_on(
                    axes.c2p(bin_center_x_val, 0) + DOWN * 1.7,
                    axes.c2p(bin_center_x_val, new_height) + DOWN * 1.7
                )
            )

        self.play(
            LaggedStartMap(FadeIn, additional_dots, lag_ratio=0.01, run_time=2),
            LaggedStart(*new_lines_animations, lag_ratio=0.05, run_time=2)
        )
        all_dots = VGroup(initial_dots, additional_dots)
        self.wait(1)

        # 4. Smoothing Lines to PDF
        self.play(status_text_obj.animate.become(Text("...条形逐渐平滑，最终浮现出概率密度函数的形状。", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))
        
        # Define the PDF curve object that will appear in the lower plotting area
        # The PDF should be scaled to match the visual height of the histogram lines
        pdf_curve_lower = axes.plot(
            lambda x_val: (1/(std_dev_data * np.sqrt(2 * np.pi))) * np.exp( - (x_val - mean_data)**2 / (2 * std_dev_data**2) ),
            color=RED,
            x_range=[axes.x_range[0], axes.x_range[1]]
        )
        # We need to scale and position this PDF curve to match where the histogram lines are
        # The histogram lines have a y_length of `final_line_scale_factor * count`, max height is around 2.0 screen units
        # The axes has y_length of 3. PDF from axes.plot will use axes's y_range [0, 0.6]
        # Scale pdf_curve_lower to visually match the histogram heights
        pdf_max_y_val_in_axes_coords = (1/(std_dev_data * np.sqrt(2 * np.pi))) # Peak of Gaussian
        # We want this peak to correspond to the visual height of `max_final_count * final_line_scale_factor` (which is 2.0)
        # The axes plots p(x) from 0 to 0.6. We need to scale our PDF plotted on these axes.
        # Let's scale the function itself to make it visually larger on these axes.
        # Target visual height for PDF peak is ~2.0 screen units.
        # Axes y_length is 3, corresponding to y_range[1] (0.6 data units). So 1 screen unit = 0.6/3 = 0.2 data units.
        # Target peak height in data units: 2.0 screen units * (0.6 data units / 3 screen units) = 0.4 data units
        
        pdf_visual_scale_factor = 0.4 / pdf_max_y_val_in_axes_coords

        pdf_curve_final = axes.plot(
            lambda x_val: pdf_visual_scale_factor * (1/(std_dev_data * np.sqrt(2 * np.pi))) * np.exp( - (x_val - mean_data)**2 / (2 * std_dev_data**2) ),
            color=RED,
            x_range=[axes.x_range[0], axes.x_range[1]]
        )
        pdf_curve_final.move_to(histogram_lines.get_center() + UP * (pdf_curve_final.get_height()/2 - histogram_lines.get_height()/2) ) # Align centers better
        
        self.play(
            FadeOut(all_dots, run_time=1),
            Transform(histogram_lines, pdf_curve_final, run_time=2)
        )
        # pdf_curve_obj was histogram_lines, which is a VGroup.
        # After transform, histogram_lines visually becomes pdf_curve_final.
        # For subsequent operations needing the curve, we should use pdf_curve_final directly.
        # However, if we want to fade out what was transformed, we use histogram_lines.
        # Let's keep pdf_curve_obj as the mobject that holds the visual of the PDF curve after transform.
        pdf_mobject_on_screen = histogram_lines # This is what was transformed and is on screen as the PDF
        self.wait(1)

        # --- GIF 3 (Now GIF 2 or 3 depending on cut): PDF Properties ---
        self.play(status_text_obj.animate.become(Text("PDF 定义与性质...", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))
        
        formula_pdf_text = MathTex(r"p(y) = \\langle \\delta(x-y) \\rangle_x").scale(0.8).set_z_index(1)
        explanation_pdf = Text("系统处于状态y附近的概率", font="Noto Sans CJK SC", font_size=16).scale(0.8).set_z_index(1)
        
        # Add definitions for formula_integral and explanation_integral_text here
        formula_integral = MathTex(r"\\int p(x)dx = 1").scale(0.8).set_z_index(1)
        explanation_integral_text = Text("总概率为1", font="Noto Sans CJK SC", font_size=16).scale(0.8).set_z_index(1)

        # Adjust positioning of PDF property texts
        pdf_expl_group_new_pos = VGroup(formula_pdf_text, explanation_pdf).arrange(DOWN, buff=0.1).next_to(axes_group, RIGHT, buff=0.2).shift(DOWN*1.8) # Shift down
        integral_expl_group_new_pos = VGroup(formula_integral, explanation_integral_text).arrange(DOWN, buff=0.1).next_to(pdf_expl_group_new_pos, UP, buff=0.2)


        # Recreate area_under_curve based on the actual PDF curve definition (pdf_curve_final)
        area_under_curve = axes.get_area(
             pdf_curve_final, # Use the actual ParametricFunction object
             x_range=[axes.x_range[0], axes.x_range[1]],
             color=YELLOW,
             opacity=0.5
        ).set_z_index(0)
        # Ensure area is correctly positioned with pdf_curve_final (which is already positioned correctly)
        # area_under_curve.move_to(pdf_curve_final.get_center()).align_to(pdf_curve_final, DOWN) # pdf_curve_final is already aligned to axes
        # The area should be aligned with pdf_curve_final, which is plotted on 'axes' in the lower part of the screen.
        # pdf_curve_final's y-values are scaled. We need to ensure the area matches this visual.
        # No, get_area uses the function from pdf_curve_final and plots it on 'axes', so its position should be correct by default
        # if pdf_curve_final itself is correctly positioned (which it is, relative to the visual space of histogram_lines).
        # The issue might be that pdf_curve_final is positioned based on histogram_lines.get_center().
        # Let's ensure the area is added correctly relative to the on-screen PDF mobject.
        # The area calculation uses the mathematical function of pdf_curve_final with 'axes'.
        # It should be drawn correctly on 'axes'. We then need to ensure its visual position matches pdf_mobject_on_screen.
        # Since pdf_mobject_on_screen IS pdf_curve_final visually, aligning to it should be correct.
        area_under_curve.move_to(pdf_mobject_on_screen.get_center()).align_to(pdf_mobject_on_screen, DOWN)


        self.play(
            Write(pdf_expl_group_new_pos),
            Write(integral_expl_group_new_pos),
            FadeIn(area_under_curve),
            run_time=2
        )
        self.wait(2)

        # Adjust mobjects_to_fade for the new structure
        mobjects_to_fade_gif3 = [axes_group, pdf_mobject_on_screen, integral_expl_group_new_pos, pdf_expl_group_new_pos, area_under_curve]
        self.play(FadeOut(*[mob for mob in mobjects_to_fade_gif3 if mob in self.mobjects]))
        self.wait(0.5)
        
        # --- GIF 4 & 5 (Observables) should be fine but check status_text_obj positioning ---
        # Ensure status_text_obj is consistently at .to_edge(UP)
        self.play(status_text_obj.animate.become(Text("引入可观测量概念...", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))
        # self.wait(0.5) # 可选

        signal_axes = Axes(x_range=[0,10,1], y_range=[-1,1,0.5], x_length=5, y_length=2.5).shift(LEFT*3)

class BrainIntroScene(Scene):
    def construct(self):
        title = Text("大脑皮层的多尺度组织", font_size=48)
        self.play(Write(title))
        
        intro_text_lines = [
            "哺乳动物大脑皮层的组织结构",
            "跨越了广泛的空间尺度，",
            "从神经元集群间的精细连接特异性，",
            "到整个皮层区域的层级网络。"
        ]
        intro_mobjects = VGroup(*[Text(line, font_size=28) for line in intro_text_lines]).arrange(DOWN, buff=0.3)
        intro_mobjects.next_to(title, DOWN, buff=0.5)
        
        self.play(LaggedStart(*[FadeIn(line, shift=UP) for line in intro_mobjects], lag_ratio=0.2))
        self.wait(3)
        self.play(FadeOut(title), FadeOut(intro_mobjects))
        self.wait(1)

class MultiScaleScene(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()
        initial_frame_width = self.camera.frame.get_width() # 保存初始帧宽度

        scale_title = Text("大脑的多尺度结构", font_size=40).to_edge(UP)
        scale_title.add_updater(lambda m: m.to_edge(UP))
        self.add(scale_title)
        self.wait(1)

        # 宏观层面
        brain_outline = Circle(radius=2, color=BLUE, fill_opacity=0.3).shift(LEFT*3)
        macro_label = Text("宏观：皮层区域", font_size=32).next_to(brain_outline, RIGHT, buff=0.5)
        
        self.play(DrawBorderThenFill(brain_outline), run_time=2)
        self.play(Write(macro_label), run_time=1.5)
        self.wait(2)

        # 中观层面
        self.play(
            self.camera.frame.animate.scale(0.4).move_to(brain_outline.get_center() + RIGHT*0.2 + DOWN*0.2),
            FadeOut(macro_label)
        )
        self.wait(0.5)

        cluster_nodes = VGroup()
        cluster_positions = [
            brain_outline.get_center() + RIGHT*0.2 + DOWN*0.2 + UP*0.5 + LEFT*0.3,
            brain_outline.get_center() + RIGHT*0.2 + DOWN*0.2 + RIGHT*0.4,
            brain_outline.get_center() + RIGHT*0.2 + DOWN*0.2 + DOWN*0.5 + LEFT*0.2
        ]
        for pos in cluster_positions:
            cluster_nodes.add(Circle(radius=0.2, color=GREEN, fill_opacity=0.5).move_to(pos))
        
        cluster_edges = VGroup(
            Line(cluster_nodes[0].get_center(), cluster_nodes[1].get_center(), stroke_width=2, color=GREEN),
            Line(cluster_nodes[1].get_center(), cluster_nodes[2].get_center(), stroke_width=2, color=GREEN),
            Line(cluster_nodes[2].get_center(), cluster_nodes[0].get_center(), stroke_width=2, color=GREEN)
        )
        neural_clusters = VGroup(cluster_edges, cluster_nodes)
        meso_label = Text("中观：神经元集群", font_size=24) # 初始大小
        # 当相机缩放时，反向缩放标签以保持视觉大小稳定
        meso_label.add_updater(
            lambda m: m.become(Text("中观：神经元集群", font_size=24))
                       .scale(initial_frame_width / self.camera.frame.get_width())
                       .next_to(self.camera.frame, DOWN, buff=0.3)
        )

        self.play(LaggedStartMap(Create, neural_clusters, lag_ratio=0.5), Write(meso_label))
        self.wait(2)

        # 微观层面
        target_cluster_node = cluster_nodes[0]
        self.play(
            self.camera.frame.animate.scale(0.3).move_to(target_cluster_node.get_center()),
            FadeOut(meso_label) # 在此动画中，updater仍然会作用于meso_label直到它完全消失
        )
        # 移除updater，避免在FadeOut后继续尝试更新
        meso_label.clear_updaters()
        self.wait(0.5)

        neuron_dots = VGroup()
        neuron_positions = [
            target_cluster_node.get_center() + LEFT*0.1 + UP*0.1,
            target_cluster_node.get_center() + RIGHT*0.15,
            target_cluster_node.get_center() + LEFT*0.05 + DOWN*0.1,
            target_cluster_node.get_center() + RIGHT*0.05 + UP*0.05
        ]
        for pos in neuron_positions:
            neuron_dots.add(Dot(point=pos, radius=0.03, color=YELLOW))

        neuron_connections = VGroup()
        for i in range(len(neuron_dots)):
            for j in range(i + 1, len(neuron_dots)):
                if np.random.rand() > 0.4:
                    neuron_connections.add(Line(neuron_dots[i].get_center(), neuron_dots[j].get_center(), stroke_width=1, color=YELLOW))
        
        single_neurons = VGroup(neuron_connections, neuron_dots)
        micro_label = Text("微观：单个神经元", font_size=18) # 初始大小
        micro_label.add_updater(
            lambda m: m.become(Text("微观：单个神经元", font_size=18))
                       .scale(initial_frame_width / self.camera.frame.get_width())
                       .next_to(self.camera.frame, DOWN, buff=0.3)
        )

        self.play(LaggedStartMap(GrowFromCenter, single_neurons, lag_ratio=0.3), Write(micro_label))
        self.wait(3)

        # 恢复镜头并清理
        self.play(Restore(self.camera.frame), FadeOut(micro_label), FadeOut(single_neurons), FadeOut(neural_clusters), FadeOut(brain_outline))
        micro_label.clear_updaters() # 清理updater
        self.remove(scale_title)
        self.wait(1)

class MeasurementLimitationsScene(Scene):
    def construct(self):
        # 标题
        title = Text("测量方法的局限性", font_size=48)
        self.play(Write(title))
        self.wait(1)
        
        # 创建三个测量方法的说明
        methods = VGroup(
            VGroup(
                Text("单神经元记录", font_size=36, color=YELLOW),
                Text("• 高时间分辨率", font_size=28),
                Text("• 采样数量有限", font_size=28),
                Text("• 仅能记录数百到数千个神经元", font_size=28)
            ).arrange(DOWN, aligned_edge=LEFT),
            VGroup(
                Text("局部场电位记录", font_size=36, color=GREEN),
                Text("• 中等时间分辨率", font_size=28),
                Text("• 测量数十万到数百万神经元", font_size=28),
                Text("• 无法重建单个神经元活动", font_size=28)
            ).arrange(DOWN, aligned_edge=LEFT),
            VGroup(
                Text("全脑成像", font_size=36, color=BLUE),
                Text("• 低时间分辨率", font_size=28),
                Text("• 覆盖整个皮层", font_size=28),
                Text("• 空间分辨率有限", font_size=28)
            ).arrange(DOWN, aligned_edge=LEFT)
        ).arrange(RIGHT, buff=1.5)
        
        # 将方法组移动到标题下方
        methods.next_to(title, DOWN, buff=1)
        
        # 动画展示每个方法
        for method in methods:
            self.play(
                LaggedStartMap(FadeIn, method, shift=UP, lag_ratio=0.2),
                run_time=2
            )
            self.wait(1)
        
        # 添加总结文本
        summary_text = Text(
            "测量方法的互补性：\n需要整合不同尺度的数据来理解大脑功能",
            font_size=32,
            color=WHITE
        ).to_edge(DOWN, buff=1)
        
        self.play(Write(summary_text))
        self.wait(2)
        
        # 淡出所有元素
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

class NetworkDynamicsScene(MovingCameraScene):
    def construct(self):
        # 标题
        title = Text("神经元网络的动力学特性", font_size=48).to_edge(UP)
        self.add(title)
        
        # 创建神经元网络
        n_neurons = 20
        neurons = VGroup(*[
            Dot(radius=0.1, color=YELLOW)
            for _ in range(n_neurons)
        ])
        
        # 随机分布神经元
        for neuron in neurons:
            neuron.move_to([
                np.random.uniform(-4, 4),
                np.random.uniform(-2, 2),
                0
            ])
        
        # 创建连接
        connections = VGroup()
        for i in range(n_neurons):
            for j in range(i+1, n_neurons):
                if np.random.random() < 0.2:  # 20%的连接概率
                    connections.add(
                        Line(
                            neurons[i].get_center(),
                            neurons[j].get_center(),
                            stroke_width=1,
                            color=BLUE_E
                        )
                    )
        
        # 创建网络组
        network = VGroup(connections, neurons)
        network.scale(0.8)
        
        # 动画展示网络形成
        self.play(
            LaggedStartMap(Create, connections, lag_ratio=0.1),
            run_time=2
        )
        self.play(
            LaggedStartMap(GrowFromCenter, neurons, lag_ratio=0.1),
            run_time=2
        )
        
        # 展示网络活动
        for _ in range(3):
            # 随机激活一些神经元
            active_neurons = VGroup(*[
                neurons[i] for i in np.random.choice(n_neurons, 5)
            ])
            
            self.play(
                *[neuron.animate.set_color(RED) for neuron in active_neurons],
                run_time=0.5
            )
            self.wait(0.5)
            self.play(
                *[neuron.animate.set_color(YELLOW) for neuron in active_neurons],
                run_time=0.5
            )
        
        # 添加说明文本
        explanation = Text(
            "简单的神经元个体\n产生复杂的网络行为",
            font_size=36,
            color=WHITE
        ).to_edge(RIGHT, buff=1)
        
        self.play(Write(explanation))
        self.wait(2)
        
        # 淡出所有元素
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

class RenormalizationScene(MovingCameraScene):
    def construct(self):
        # 标题
        title = Text("大脑网络的重整化", font_size=48).to_edge(UP)
        self.add(title)
        
        # 创建微观尺度的神经元网络
        def create_neuron_network(n_neurons, scale=1.0, color=YELLOW):
            neurons = VGroup(*[
                Dot(radius=0.1 * scale, color=color)
                for _ in range(n_neurons)
            ])
            
            # 在圆形区域内随机分布神经元
            for neuron in neurons:
                angle = np.random.uniform(0, TAU)
                radius = np.random.uniform(0, 2) * scale
                neuron.move_to([
                    radius * np.cos(angle),
                    radius * np.sin(angle),
                    0
                ])
            
            # 创建连接
            connections = VGroup()
            for i in range(n_neurons):
                for j in range(i+1, n_neurons):
                    if np.random.random() < 0.2:  # 20%的连接概率
                        connections.add(
                            Line(
                                neurons[i].get_center(),
                                neurons[j].get_center(),
                                stroke_width=1 * scale,
                                color=color,
                                stroke_opacity=0.5
                            )
                        )
            
            return VGroup(connections, neurons)
        
        # 创建三个尺度的网络
        micro_network = create_neuron_network(30, scale=0.8, color=YELLOW)
        meso_network = create_neuron_network(15, scale=1.2, color=GREEN)
        macro_network = create_neuron_network(8, scale=1.6, color=BLUE)
        
        # 初始位置
        micro_network.move_to(LEFT * 4)
        meso_network.move_to(ORIGIN)
        macro_network.move_to(RIGHT * 4)
        
        # 添加尺度标签
        scale_labels = VGroup(
            Text("微观尺度\n(神经元)", font_size=24, color=YELLOW),
            Text("中观尺度\n(神经元集群)", font_size=24, color=GREEN),
            Text("宏观尺度\n(皮层区域)", font_size=24, color=BLUE)
        ).arrange(RIGHT, buff=4)
        scale_labels.to_edge(DOWN, buff=1)
        
        # 动画展示网络形成
        self.play(
            LaggedStartMap(Create, micro_network[0], lag_ratio=0.1),
            LaggedStartMap(GrowFromCenter, micro_network[1], lag_ratio=0.1),
            Write(scale_labels[0]),
            run_time=2
        )
        self.wait(1)
        
        # 展示重整化过程：微观到中观
        self.play(
            ReplacementTransform(
                micro_network.copy(),
                meso_network,
                path_arc=PI/4
            ),
            Write(scale_labels[1]),
            run_time=2
        )
        self.wait(1)
        
        # 展示重整化过程：中观到宏观
        self.play(
            ReplacementTransform(
                meso_network.copy(),
                macro_network,
                path_arc=PI/4
            ),
            Write(scale_labels[2]),
            run_time=2
        )
        self.wait(1)
        
        # 添加说明文本
        explanation = Text(
            "重整化：\n通过粗粒化将微观细节\n转化为宏观规律",
            font_size=32,
            color=WHITE
        ).to_edge(RIGHT, buff=1)
        
        self.play(Write(explanation))
        self.wait(2)
        
        # 展示网络活动
        for network in [micro_network, meso_network, macro_network]:
            neurons = network[1]
            n_neurons = len(neurons)
            active_neurons = VGroup(*[
                neurons[i] for i in np.random.choice(n_neurons, max(2, n_neurons//4))
            ])
            
            self.play(
                *[neuron.animate.set_color(RED) for neuron in active_neurons],
                run_time=0.5
            )
            self.wait(0.5)
            self.play(
                *[neuron.animate.set_color(neurons[0].get_color()) for neuron in active_neurons],
                run_time=0.5
            )
        
        # 淡出所有元素
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

class PathIntegralScene(Scene):
    def construct(self):
        # 标题
        title = Text("路径积分与系统演化", font="Noto Sans CJK SC")
        title.to_edge(UP)
        self.add(title)  # 直接add，不做动画

        # 创建多条路径
        num_paths = 15
        paths = []
        weights = []
        dots = []
        
        # 创建路径和权重
        for i in range(num_paths):
            weight = np.random.uniform(0.1, 1.0)
            weights.append(weight)
            points = []
            x = -5
            y = 0
            for _ in range(30):
                x += 0.3
                y += np.random.normal(0, 0.2)
                points.append(np.array([x, y, 0]))
            path = VMobject()
            path.set_points_as_corners(points)
            path.set_stroke(width=2, opacity=0.3)
            paths.append(path)
            path_dots = VGroup()
            for point in points[::3]:
                dot = Dot(point, radius=0.03)
                dot.set_opacity(0.3)
                path_dots.add(dot)
            dots.append(path_dots)

        # 直接add所有路径云
        for path in paths:
            self.add(path)

        # 创建权重标签（只显示部分权重）
        weight_labels = VGroup()
        for i, (path, weight) in enumerate(zip(paths, weights)):
            if i % 3 == 0:
                label = MathTex(f"w_{{{i+1}}}={weight:.2f}")
                label.scale(0.5)
                point = path.point_from_proportion(0.5)
                label.next_to(point, UP, buff=0.1)
                weight_labels.add(label)

        # 创建平均路径
        avg_points = []
        for i in range(30):
            x = -5 + i * 0.3
            y = 0
            total_weight = 0
            weighted_y = 0
            for path, weight in zip(paths, weights):
                point = path.point_from_proportion(i/29)
                weighted_y += point[1] * weight
                total_weight += weight
            y = weighted_y / total_weight
            avg_points.append(np.array([x, y, 0]))
        avg_path = VMobject()
        avg_path.set_points_as_corners(avg_points)
        avg_path.set_stroke(color=YELLOW, width=4)

        # 1. 权重标签淡入
        self.play(Write(weight_labels), run_time=1)

        # 2. 粒子运动动画
        for path_dots in dots:
            self.add(*path_dots)
        for _ in range(2):
            for path_dots in dots:
                self.play(
                    *[dot.animate.move_to(path_dots[i+1].get_center()) 
                      for i, dot in enumerate(path_dots[:-1])],
                    run_time=0.3,
                    rate_func=linear
                )

        # 3. 显示平均路径
        self.play(Create(avg_path), run_time=1.5)

        # 4. 添加说明文字
        explanation = Text(
            "系统演化是所有可能路径的加权平均",
            font="Noto Sans CJK SC",
            font_size=24
        )
        explanation.next_to(avg_path, DOWN, buff=0.5)
        self.play(Write(explanation), run_time=1)

        # 5. 最终效果：突出显示平均路径
        self.play(
            avg_path.animate.set_stroke(width=6),
            *[path.animate.set_opacity(0.1) for path in paths],
            *[dot.animate.set_opacity(0.1) for path_dots in dots for dot in path_dots],
            weight_labels.animate.set_opacity(0.3),
            run_time=1
        )
        self.wait(1)

class MomentScene(MovingCameraScene):
    def construct(self):
        # Reuse status text from previous scene for consistency
        status_text_obj = Text("", font_size=24).to_corner(UP + LEFT)
        self.add(status_text_obj)

        # 1. Setup Axes (reused from ProbabilityAndObservablesScene)
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[0, 0.5, 0.1],
            axis_config={"include_numbers": True, "font_size": 24},
            x_length=7,
            y_length=4
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="P(x)")
        
        # Position axes and labels initially
        axes_group = VGroup(axes, axes_labels).center()
        self.play(Write(axes_group))
        self.wait(1)

        # PDF (Gaussian)
        mean_val = 0
        std_dev_val = 1
        self.play(status_text_obj.animate.become(Text("我们从一个标准高斯分布 P(x) 开始", font="Noto Sans CJK SC", font_size=20).to_edge(UP)))
        def gaussian_pdf(x):
            return (1 / (std_dev_val * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean_val) / std_dev_val) ** 2)

        pdf_curve = axes.plot(gaussian_pdf, color=BLUE)
        pdf_label = MathTex("P(x)", font_size=36).next_to(pdf_curve, UP, buff=0.2)
        
        self.play(Create(pdf_curve), Write(pdf_label))
        self.wait(1)

        # Animate calculation of the mean
        status_text_obj.become(Text("现在来看矩。第一个矩是均值 (μ)，描述分布的中心。", font="Noto Sans CJK SC", font_size=20).to_edge(UP))
        mean_line = DashedLine(
            start=axes.c2p(mean_val, 0),
            end=axes.c2p(mean_val, gaussian_pdf(mean_val)),
            color=GREEN
        )
        mean_dot = Dot(axes.c2p(mean_val, gaussian_pdf(mean_val)), color=GREEN)
        mean_label_tex = MathTex("\\mu", font_size=36, color=GREEN).next_to(mean_line, DOWN, buff=0.2)
        mean_text = Text("(Mean)", font_size=24, color=GREEN).next_to(mean_label_tex, DOWN, buff=0.1)
        
        self.play(Create(mean_line), Create(mean_dot), Write(mean_label_tex), Write(mean_text))
        self.wait(2)

        # Animate calculation of the variance
        status_text_obj.become(Text("第二个中心矩是方差 (σ²)，描述分布的离散程度。", font="Noto Sans CJK SC", font_size=20).to_edge(UP))
        
        # Shade area for variance (±1 std_dev)
        variance_area = axes.get_area(
            pdf_curve,
            x_range=(mean_val - std_dev_val, mean_val + std_dev_val),
            color=YELLOW,
            opacity=0.5
        )
        
        # Lines for ±1 std_dev
        std_dev_line_minus = DashedLine(
            axes.c2p(mean_val - std_dev_val, 0),
            axes.c2p(mean_val - std_dev_val, gaussian_pdf(mean_val - std_dev_val)),
            color=YELLOW_D # A darker yellow for lines
        )
        std_dev_line_plus = DashedLine(
            axes.c2p(mean_val + std_dev_val, 0),
            axes.c2p(mean_val + std_dev_val, gaussian_pdf(mean_val + std_dev_val)),
            color=YELLOW_D
        )
        
        variance_label_tex = MathTex("\\sigma^2", font_size=36, color=YELLOW_D).next_to(variance_area, UP, buff=0.1).align_to(axes.c2p(mean_val,0), RIGHT)
        variance_text = Text("(Variance)", font_size=24, color=YELLOW_D).next_to(variance_label_tex, DOWN, buff=0.1)

        self.play(
            FadeIn(variance_area), 
            Create(std_dev_line_minus), 
            Create(std_dev_line_plus),
            Write(variance_label_tex),
            Write(variance_text)
        )
        self.wait(2)

        # --- Skewness --- 
        status_text_obj.become(Text("更高阶的矩，如偏度，描述分布的形状。", font="Noto Sans CJK SC", font_size=20).to_edge(UP))
        self.wait(0.5)

        # Store original curve and label for restoring later if needed
        original_pdf_curve = pdf_curve
        original_pdf_label = pdf_label

        # Define a skewed distribution (e.g., skew normal)
        # For simplicity, we'll use a lambda that's easy to manipulate for skewness visually
        # This is a conceptual illustration, not a strict skew normal PDF.
        def skewed_gaussian_pdf(x):
            skew_factor = 2 # Positive for right skew
            # A simple way to introduce skewness by modifying the x term
            # This is a custom function for visual effect, not a standard skewed distribution formula.
            # We'll use a gamma distribution shape for visual skewness.
            # scipy.stats.gamma.pdf(x, a, loc, scale) where a is shape parameter
            # Let's try a simpler visual skew by scaling and shifting parts of the gaussian.
            # For a simple visual skew, we can make one side decay faster.
            if x < mean_val:
                 return (1 / (std_dev_val * np.sqrt(2 * np.pi))) * np.exp(-0.5 * (((x - mean_val) / std_dev_val)) ** 2)
            else:
                 return (1 / (std_dev_val * np.sqrt(2 * np.pi))) * np.exp(-0.5 * (((x - mean_val) / (std_dev_val * 0.5))) ** 2) 
        
        # A more common way to show skew is to use a distribution known for skewness, e.g. Chi-squared or Gamma.
        # Let's try a skew normal for a more controlled skew effect.
        # alpha > 0 means right skewed, alpha < 0 means left skewed.
        alpha_skew = 4 # Skewness parameter
        def skew_normal_pdf(x):
            t = (x - mean_val) / std_dev_val
            phi_t = (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * t**2) # Standard normal PDF
            Phi_alpha_t = 0.5 * (1 + scipy.special.erf(alpha_skew * t / np.sqrt(2))) # Standard normal CDF of alpha*t
            return (2 / std_dev_val) * phi_t * Phi_alpha_t

        skewed_pdf_curve = axes.plot(skew_normal_pdf, color=PURPLE)
        skewness_label = Text("Skewness", font_size=36, color=PURPLE).next_to(skewed_pdf_curve, UP, buff=0.5).shift(RIGHT*1.5)

        # Fade out mean/variance specific visuals before transforming PDF
        self.play(
            FadeOut(mean_line), FadeOut(mean_dot), FadeOut(mean_label_tex), FadeOut(mean_text),
            FadeOut(variance_area), FadeOut(std_dev_line_minus), FadeOut(std_dev_line_plus),
            FadeOut(variance_label_tex), FadeOut(variance_text)
        )
        self.wait(0.5)

        self.play(Transform(pdf_curve, skewed_pdf_curve), FadeOut(pdf_label), Write(skewness_label))
        self.wait(2)

        # --- Kurtosis --- 
        status_text_obj.become(Text("峰度也是描述分布形状的重要高阶矩。", font="Noto Sans CJK SC", font_size=20).to_edge(UP))
        self.wait(0.5)

        # Define a distribution with different kurtosis (e.g., more peaked or flatter)
        # We can adjust the standard deviation or power in the exponent for a simple visual effect.
        # Higher kurtosis (leptokurtic) - more peaked, fatter tails
        # Lower kurtosis (platykurtic) - flatter, thinner tails
        def leptokurtic_gaussian_pdf(x): # Higher peak, fatter tails
            # Effectively a smaller std_dev for the central part, but we need to ensure area is ~1
            # A common example is Student's t-distribution with few degrees of freedom.
            # For visual simplicity, let's make a sharper peak:
            return (1 / (0.6 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean_val) / 0.6) ** 2) 
            # This will make it more peaked but also narrower overall. Fatter tails are harder with simple Gaussian mod.

        # Let's use a modified Gaussian where the power is different, e.g., exp(-|x|^gamma) (generalized normal)
        # For higher kurtosis (more peaked), gamma > 2. For lower (flatter), gamma < 2. (gamma=2 is Gaussian)
        gamma_kurtosis = 4 # For leptokurtic (peaked)
        # Normalization constant for generalized normal is tricky. Let's simplify for visuals.
        # We'll keep the same std_dev but change the 'peakedness'
        # This is not a true PDF but for visual illustration of kurtosis. We'll use a scaled Gaussian
        def high_kurtosis_visual_pdf(x):
            # A simple visual: make the peak higher and tails relatively fatter than a narrow Gaussian.
            # This is a superposition for effect.
            return 0.8 * (1 / (0.7 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean_val) / 0.7)**2) + \
                   0.2 * (1 / (2.0 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean_val) / 2.0)**2)

        kurtosis_pdf_curve = axes.plot(high_kurtosis_visual_pdf, color=ORANGE)
        kurtosis_label = Text("Kurtosis", font_size=36, color=ORANGE).next_to(kurtosis_pdf_curve, UP, buff=0.1).shift(LEFT*0.5)

        # Transform from skewed to kurtotic
        self.play(Transform(pdf_curve, kurtosis_pdf_curve), FadeOut(skewness_label), Write(kurtosis_label))
        self.wait(2)

        # Restore original PDF for next steps (or fade out current one)
        # For now, let's just fade out the kurtosis visuals and original curve placeholder
        self.play(FadeOut(pdf_curve), FadeOut(kurtosis_label))
        status_text_obj.become(Text("但仅凭矩有时会产生误导...", font="Noto Sans CJK SC", font_size=20).to_edge(UP))
        self.wait(1)

        # --- Misleading Moments: Two different distributions with same mean and variance ---
        self.play(FadeOut(axes_group), FadeOut(pdf_label)) # Clean up previous axes and labels
        self.wait(0.5)

        # Define common mean and variance
        common_mean = 0
        common_variance = 1 # so std_dev = 1
        common_std_dev = np.sqrt(common_variance)

        # Distribution 1: A Skewed Distribution (e.g., a specific skew-normal)
        # We need to set parameters such that it has the target mean and variance.
        # For skew-normal: mean = xi + omega * delta * sqrt(2/pi), var = omega^2 * (1 - 2*delta^2/pi)
        # where delta = alpha / sqrt(1+alpha^2)
        # Let omega = 1 for simplicity in variance calculation for now.
        # If omega = 1, var = 1 - 2*delta^2/pi. To make var = 1, this doesn't work unless delta = 0 (normal dist).
        # So we need to choose alpha (skewness) and then adjust omega (scale) and xi (location) to match.

        # Let's use a sum of Gaussians to create a custom shape, then numerically verify mean/variance.
        # For visual clarity, let's create a bimodal distribution and a unimodal skewed one.

        # Distribution 1: Unimodal Skewed (e.g., Gamma distribution)
        # Gamma(k, theta): mean = k*theta, variance = k*theta^2
        # To get mean=0, var=1: k*theta = 0 (implies k=0 or theta=0, not useful)
        # We need to shift it. Gamma(k, theta, loc): mean = k*theta + loc, var = k*theta^2
        # Let k*theta^2 = 1 (variance). Let k*theta + loc = 0 (mean).
        # E.g., k=4, theta=0.5 => var = 4*0.25 = 1. mean_unshifed = k*theta = 4*0.5 = 2.
        # So, loc = -2. This means the distribution is Gamma(shape=4, scale=0.5) shifted by -2.
        shape_g1 = 4
        scale_g1 = 0.5
        loc_g1 = - (shape_g1 * scale_g1) # To make mean = 0

        def dist1_pdf(x):
            # scipy.stats.gamma.pdf(x, a, loc=0, scale=1)
            # Here x is the original variable, for plotting we use x_shifted = x - loc_g1
            # So pdf_val = scipy.stats.gamma.pdf(x - loc_g1, shape_g1, scale=scale_g1)
            # No, this is scipy's `loc` parameter, which is a shift of the random variable itself.
            # So, the pdf is at x, using loc_g1 in the call.
            pdf_val = scipy.stats.gamma.pdf(x, shape_g1, loc=loc_g1, scale=scale_g1)
            return pdf_val
        
        # Distribution 2: Bimodal distribution (sum of two Gaussians)
        # G1: mean m1, std s1, weight w1; G2: mean m2, std s2, weight w2 (w1+w2=1)
        # Overall mean = w1*m1 + w2*m2
        # Overall variance = w1*(s1^2+m1^2) + w2*(s2^2+m2^2) - (overall mean)^2
        # Let's aim for mean=0, var=1.
        # Symmetrical bimodal: m1 = -m, m2 = m. s1=s2=s. w1=w2=0.5.
        # Overall mean = 0.5*(-m) + 0.5*m = 0.
        # Overall var = 0.5*(s^2+(-m)^2) + 0.5*(s^2+m^2) - 0^2 = 0.5*(s^2+m^2) + 0.5*(s^2+m^2) = s^2+m^2.
        # We need s^2+m^2 = 1 (variance). 
        # Let m = 0.8, then m^2 = 0.64. So s^2 = 1 - 0.64 = 0.36. s = 0.6.
        m2_peak_dist = 0.8
        s2_std = 0.6
        def dist2_pdf(x):
            g1 = 0.5 * (1/(s2_std*np.sqrt(2*np.pi))) * np.exp(-0.5*((x - (-m2_peak_dist))/s2_std)**2)
            g2 = 0.5 * (1/(s2_std*np.sqrt(2*np.pi))) * np.exp(-0.5*((x - m2_peak_dist)/s2_std)**2)
            return g1 + g2

        # Create two axes side by side
        axes_x_range = [-4, 4, 1]
        axes_y_range = [0, 0.7, 0.1] # Adjusted y_range based on typical PDF heights
        axes_common_config = {"include_numbers": True, "font_size": 20}
        axes_length_x = 5
        axes_length_y = 3

        axes1 = Axes(x_range=axes_x_range, y_range=axes_y_range, axis_config=axes_common_config, x_length=axes_length_x, y_length=axes_length_y)
        axes1_labels = axes1.get_axis_labels(x_label="x", y_label="P(x)")
        dist1_curve = axes1.plot(dist1_pdf, color=RED)
        dist1_title = Text("Distribution A", font_size=24).next_to(axes1, UP)
        dist1_group = VGroup(axes1, axes1_labels, dist1_curve, dist1_title).to_edge(LEFT, buff=0.5)

        axes2 = Axes(x_range=axes_x_range, y_range=axes_y_range, axis_config=axes_common_config, x_length=axes_length_x, y_length=axes_length_y)
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

        # Highlight that mean and variance are the same for both
        # For Gamma(shape_g1, loc_g1, scale_g1): 
        # Mean = shape_g1*scale_g1 + loc_g1 = 4*0.5 + (-2) = 2 - 2 = 0
        # Var = shape_g1*scale_g1^2 = 4 * (0.5)^2 = 4 * 0.25 = 1
        mean_dist1_val = 0 # By construction
        var_dist1_val = 1   # By construction

        # For Bimodal symmetric sum of Gaussians:
        # Mean = 0 (by symmetry and construction)
        # Var = s^2 + m^2 = 0.6^2 + 0.8^2 = 0.36 + 0.64 = 1
        mean_dist2_val = 0 # By construction
        var_dist2_val = 1   # By construction

        stats_text_template = "Mean ≈ {:.2f}, Variance ≈ {:.2f}"
        
        stats1_text = Text(stats_text_template.format(mean_dist1_val, var_dist1_val), font_size=20).next_to(dist1_title, DOWN, buff=0.1)
        stats2_text = Text(stats_text_template.format(mean_dist2_val, var_dist2_val), font_size=20).next_to(dist2_title, DOWN, buff=0.1)

        self.play(Write(stats1_text), Write(stats2_text))
        self.wait(2)
        
        misleading_text = Text("Same Mean & Variance, Different Shapes!", font_size=30, color=YELLOW).to_edge(DOWN, buff=0.5)
        self.play(Write(misleading_text))
        self.wait(3)
        
        # --- Introduce Cumulants ---
        status_text_obj.become(Text("这就是累积量的用武之地。它提供了描述形状的另一种方式。", font="Noto Sans CJK SC", font_size=20).to_edge(UP))
        # Fade out the two distributions and their stats for now
        self.play(
            FadeOut(dist1_group), FadeOut(dist2_group),
            FadeOut(stats1_text), FadeOut(stats2_text),
            FadeOut(misleading_text)
        )
        self.wait(1)

        cumulants_title = Text("Cumulants (κ)", font_size=48).to_edge(UP)
        self.play(Write(cumulants_title))
        self.wait(1)

        # Show 1st cumulant = mean
        kappa1_text = MathTex("\\kappa_1 = \\text{Mean}", font_size=36)
        # Show 2nd cumulant = variance
        kappa2_text = MathTex("\\kappa_2 = \\text{Variance}", font_size=36)
        # Higher cumulants
        kappa_higher_text = MathTex("\\kappa_3, \\kappa_4, ...", "\\text{ capture other shape details}", font_size=36)
        
        cumulant_eqs = VGroup(kappa1_text, kappa2_text, kappa_higher_text).arrange(DOWN, buff=0.5).next_to(cumulants_title, DOWN, buff=0.5)

        self.play(Write(cumulant_eqs))
        self.wait(3)

        # Visually imply higher cumulants (κ₃, κ₄) capture the *differences*
        status_text_obj.become(Text("高阶累积量能区分这些矩难以区分的形状差异。", font="Noto Sans CJK SC", font_size=20).to_edge(UP))
        self.wait(0.5)

        # Highlight κ₃, κ₄, ... part
        # The MathTex for higher kappa is kappa_higher_text[0] for symbols, kappa_higher_text[1] for text
        self.play(kappa_higher_text[0].animate.set_color(YELLOW), run_time=1)
        self.wait(0.5)

        # Reintroduce the two distributions, scaled down and shifted
        # Clean up previous displays before bringing back dists
        current_scene_elements = VGroup(cumulants_title, cumulant_eqs)
        
        # Scale down the distribution groups
        dist1_group_small = dist1_group.copy().scale(0.6)
        dist2_group_small = dist2_group.copy().scale(0.6)

        # Position them appropriately (e.g., below the cumulant equations or to the sides)
        dist_display_group = VGroup(dist1_group_small, dist2_group_small).arrange(RIGHT, buff=1.0)
        dist_display_group.next_to(current_scene_elements, DOWN, buff=0.75)

        # Fade out current elements and fade in the distributions
        self.play(
            # FadeOut(current_scene_elements), # Keep cumulant text as context
            Transform(current_scene_elements, current_scene_elements.copy().to_edge(UP).shift(DOWN*0.5)), # Move text up
            FadeIn(dist_display_group)
        )
        self.wait(1)

        # Now, visually connect κ₃, κ₄ to the differences.
        # For Distribution A (Gamma - skewed), highlight its tail or general asymmetry.
        # For Distribution B (Bimodal), highlight the two peaks or the dip in the middle.

        # Create highlighting for Dist1 (skewed)
        # Example: a flashing arrow pointing to the skewed tail of dist1_curve (part of dist1_group_small)
        # The dist1_curve is the 2nd element in axes1_group which is the 0th element of dist1_group_small
        # dist1_group_small = VGroup(axes1, axes1_labels, dist1_curve, dist1_title)
        # axes1_group contains axes1, axes1_labels, dist1_curve, dist1_title
        # curve_in_dist1_small = dist1_group_small[2]

        # To highlight part of a curve, it's easier to draw over it or use an indicator.
        # Let's try to make the curves themselves pulse or change color briefly in the differing regions.
        # This is complex. A simpler approach: draw attention with arrows/circles.

        # Arrow for Dist A (skewness)
        # Target point on dist1_curve (skewed tail)
        # axes1_small = dist1_group_small[0]
        # approx_skew_point_x = loc_g1 + shape_g1 * scale_g1 + 2*np.sqrt(shape_g1*scale_g1**2) # Mean + 2*std_dev for this gamma
        # approx_skew_point = axes1_small.c2p(approx_skew_point_x, dist1_pdf(approx_skew_point_x)*0.5) # Lower part of tail
        # Let's pick a point on the right tail of dist1_pdf (which is left skewed, so its longer tail is to the left)
        # Gamma(shape=4, scale=0.5, loc=-2). Mean=0. It is right-skewed (tail to the right)
        # loc_g1 is -2. Mean is 0. Peak is around x=1 for shape=4, scale=0.5, before shift. Shifted peak near x = -1.
        # Tail is to the right of 0.
        skew_highlight_point_x_dist1 = 1.5 # Point on the right tail
        skew_highlight_y_dist1 = dist1_pdf(skew_highlight_point_x_dist1)
        arrow_A_target = dist1_group_small[0].c2p(skew_highlight_point_x_dist1, skew_highlight_y_dist1)
        arrow_A = Arrow(kappa_higher_text[0].get_bottom() + DOWN*0.2, arrow_A_target, buff=0.1, color=RED_E, stroke_width=5)
        label_A_diff = Text("Different Shape (e.g., Skew)", font_size=18, color=RED_E).next_to(arrow_A.get_center(), RIGHT, buff=0.1)

        # Arrow for Dist B (bimodality)
        # Target one of the peaks or the dip of dist2_curve
        # axes2_small = dist2_group_small[0]
        # Peaks are at m2_peak_dist and -m2_peak_dist (0.8 and -0.8)
        bimodal_highlight_point_x_dist2 = m2_peak_dist
        bimodal_highlight_y_dist2 = dist2_pdf(bimodal_highlight_point_x_dist2)
        arrow_B_target = dist2_group_small[0].c2p(bimodal_highlight_point_x_dist2, bimodal_highlight_y_dist2)
        arrow_B = Arrow(kappa_higher_text[0].get_bottom() + DOWN*0.2, arrow_B_target, buff=0.1, color=GREEN_E, stroke_width=5)
        label_B_diff = Text("Different Shape (e.g., Bimodality)", font_size=18, color=GREEN_E).next_to(arrow_B.get_center(), LEFT, buff=0.1)

        self.play(GrowArrow(arrow_A), Write(label_A_diff))
        self.wait(1.5)
        self.play(ReplacementTransform(arrow_A, arrow_B), ReplacementTransform(label_A_diff, label_B_diff))
        self.wait(1.5)

        final_message = Text("Higher cumulants (κ₃, κ₄, ...) quantify these distinct features.", font_size=24, color=YELLOW)
        final_message.next_to(dist_display_group, DOWN, buff=0.75)
        self.play(Write(final_message))
        self.wait(4)

        # End Scene: Fade out everything
        all_elements = VGroup(status_text_obj, current_scene_elements, dist_display_group, arrow_B, label_B_diff, final_message)
        self.play(FadeOut(all_elements))
        self.wait(1)

# Entry point for Manim
# To render a specific scene, set its name in config.scene_names
# For example: config.scene_names = ["IntroScene"]
# To render all scenes, you might need a custom script or run manim for each scene name.

# Test lines for local execution (optional)
if __name__ == "__main__":
    # This part is for direct execution with Python, not for Manim rendering
    # For Manim, use: manim -pql brain_animation.py SceneName
    print("To render a scene, use 'manim -pql brain_animation.py SceneName'")
    print("For example: manim -pql brain_animation.py IntroScene")

# 更新场景配置
config.scene_names = ["ProbabilityAndObservablesScene"]  # 只播放此场景以进行GIF生成
# config.scene_names = ["IntroScene", "ProbabilityAndObservablesScene", "BrainIntroScene", "MultiScaleScene", "MeasurementLimitationsScene", "NetworkDynamicsScene", "RenormalizationScene", "PathIntegralScene", "MomentScene"]