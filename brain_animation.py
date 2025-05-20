from manim import *
# from manim.constants import DEFAULT_FRAME_WIDTH # DEFAULT_FRAME_WIDTH 不存在于此版本

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

# 更新场景配置
config.scene_names = ["BrainIntroScene", "MultiScaleScene", "MeasurementLimitationsScene", "NetworkDynamicsScene", "RenormalizationScene", "PathIntegralScene"] 