from colour import Color
from manim import *
import numpy as np


class MainScene(Scene):
    def construct(self):
        #(No speech)
        # self.make_title(2)
        #(No speech)

        # self.wait(2)

        #"One study found a ... the probability of death."
        # self.display_prob_func(2)
        #"The driver may be ... at some given distance"

        # self.wait(3)

        #"We can visualize the collision with a position vs time graph"
        self.pos_vs_time(2)

        self.wait(2.5)


    def make_title(self, duration: int):
        title = Tex(r"The Mathematics of Collisions", font_size=64)

        self.play(Write(title))
        self.wait(duration)
        self.play(Unwrite(title, duration=0.3))

    def display_prob_func(self, duration: int):
        prob_func = lambda v: 1 / (1 + np.exp(6.9 - 0.090 * v))
        prob_func_tex = MathTex(r"\frac{1}{1 + e^{6.9 - 0.090v}}").to_edge(edge=LEFT)

        axes = Axes(
            x_range=[0, 148, 20],
            y_range=[0, 1.1, 0.2],
            x_length=7,
            y_length=5,
            x_axis_config={
                "numbers_to_include": np.arange(0, 140.1, 20)
            },
            y_axis_config={
                "numbers_to_include": np.arange(0, 1.1, 0.2)
            },
            tips=False
        ).to_edge(edge=RIGHT)

        plot = axes.plot(prob_func, color=TEAL)

        labels = axes.get_axis_labels(x_label=Tex("$v$"), y_label=Tex("$P(v)$"))

        self.play(
            Write(prob_func_tex, duration=2),
            Create(axes, duration=2),
            Create(plot),
            Write(labels, duration=1)
        )

        self.wait(duration)

        self.play(
            Unwrite(prob_func_tex, duration=2),
            Uncreate(axes, duration=2),
            Uncreate(plot),
            Unwrite(labels, duration=1)
        )

    def pos_vs_time(self, duration: int):
        reaction = 3
        car_acc = 0.8
        dist = 4
        velocity = ValueTracker(0.8)

        ped_color = Color()
        ped_color.set_hex("#D80D8E")

        def get_car_plot(axes: Axes, v: float) -> ParametricFunction:

            def linear_func(t: float, v: float) -> float:
                return v * t

            def quadr_func(t: float, v: float) -> float:
                return v * t - 0.5 * car_acc * (t - reaction) ** 2


            return axes.plot(lambda t: quadr_func(t, v) if t > reaction else linear_func(t, v), x_range=[0, reaction + v / car_acc + 0.1, 0.08], color=YELLOW)

        def update_car_plot() -> Transform:
            return Transform(car_plot, get_car_plot(axes, velocity.get_value()), rate_function=smooth, duration=0.7)

        axes = Axes(
            x_range=[0, 7, 20],
            y_range=[0, 5, 20]
        )

        labels = axes.get_axis_labels(x_label=Tex("$t$"), y_label=Tex("$x$"))

        car_plot = get_car_plot(axes, 0.6)
        car_plot.add_updater(lambda this: this.replace(get_car_plot(axes, velocity.get_value()), stretch=True))

        pedestrian_plot = axes.plot(lambda t: dist, color=ped_color)

        self.play(
            Create(axes),
            Create(car_plot),
            Create(pedestrian_plot),
            Write(labels)
        )

        self.wait(duration)

        self.play(
            velocity.animate.set_value(1.26),
            duration=2
        )

        car_plot.get_point_from_function(reaction)
        axes.get_vertical_line(axes.input_to_graph_point(reaction, car_plot), color=TEAL)


