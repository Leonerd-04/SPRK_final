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
        self.add(velocity)

        ped_color = Color()
        ped_color.set_hex("#D80D8E")

        # Plot consists of a constant velocity line and a constant acceleration parabola, determined by the parameters
        # above.
        def get_car_plot(axes: Axes, v: float) -> ParametricFunction:

            def linear_func(t: float, v: float) -> float:
                return v * t

            def quadr_func(t: float, v: float) -> float:
                return v * t - 0.5 * car_acc * (t - reaction) ** 2


            return axes.plot(
                lambda t:
                quadr_func(t, v) if t >= reaction
                else linear_func(t, v),
                x_range=[0, reaction + v / car_acc + 0.1, 0.05],
                color=YELLOW
            )

        axes = Axes(
            x_range=[0, 7, 20],
            y_range=[0, 5, 20]
        )

        labels = axes.get_axis_labels(x_label=Tex("$t$"), y_label=Tex("$x$"))

        car_plot = get_car_plot(axes, velocity.get_value())
        car_plot.add_updater(
            lambda this: this.set_points(get_car_plot(axes, velocity.get_value()).get_all_points())
        )

        pedestrian_plot = axes.plot(lambda t: dist, color=ped_color)

        self.play(
            Create(axes),
            Create(car_plot),
            Create(pedestrian_plot),
            Write(labels)
        )

        self.wait(duration)

        #"If these two curves intersect..."
        self.play(
            velocity.animate.set_value(1.26),
            duration=0.7
        )

        self.wait(3)

        #(No speech)
        self.play(
            velocity.animate.set_value(0.6),
            duration=0.7
        )

        # Line to demonstrate where the acceleration starts
        line = axes.get_vertical_line(axes.c2p(reaction, velocity.get_value() * reaction, 0), color=TEAL)
        line.add_updater(
            lambda this: this.replace(
                axes.get_vertical_line(axes.c2p(reaction, velocity.get_value() * reaction, 0), color=TEAL),
                stretch=True
            )
        )
        self.add(line)

        temp_line = Line(start=axes.coords_to_point(0, 0), end=axes.coords_to_point(reaction))

        brace = Brace(temp_line)
        brace_text = Tex("Reaction Time", font_size=24).next_to(brace, DOWN * 1/2)

        self.add(brace, brace_text)

        #"Because human brains... driver won't react"
        self.play(
            Create(line),
            Write(brace),
            Write(brace_text)
        )

        #"We can see now that changing..."
        self.play(
            velocity.animate.set_value(0.76),
            rate_func=wiggle,
            duration=1.5
        )

        self.play(
            velocity.animate.set_value(0.5),
            duration=0.8
        )

        self.wait()
        #"Low enough cruising speeds"
        self.play(
            velocity.animate.set_value(1.1),
            duration=8
        )
