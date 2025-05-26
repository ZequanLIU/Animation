from manim import *
import numpy as np

class PathIntegralScene(Scene):
    def construct(self):
        # 1. Scene Title
        title = Text("路径积分与泛函形式", font="Noto Sans CJK SC", font_size=36)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)

        # 2. Path Integral Formula (Z)
        path_integral_formula_Z = MathTex(
            r"\mathcal{Z} = \int \mathcal{D}\phi \, e^{-S[\phi]}", 
            font_size=48
        )
        path_integral_formula_Z.next_to(title, DOWN, buff=0.7)
        
        # 3. Action Functional Formula (S)
        action_functional_S = MathTex(
            r"S[\phi] = \int dt \, L(\phi, \dot{\phi})",
            font_size=48
        )
        action_functional_S.next_to(path_integral_formula_Z, DOWN, buff=0.7)

        formulas = VGroup(path_integral_formula_Z, action_functional_S)
        self.play(Write(formulas))
        self.wait(2)

        # Placeholder for future elements -  TEMPORARILY REMOVED FOR INITIAL TEST
        # self.play(FadeOut(title), FadeOut(formulas))
        # self.wait(1)

config.scene_names = ["PathIntegralScene"] 