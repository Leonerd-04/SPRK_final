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

        self.wait(3)

        #"We can visualize the collision with a position vs time graph"
        self.pos_vs_time(3)

        self.wait(3)


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
        reaction = 2
        car_acc = 0.5

        def get_car_plot(axes: Axes, v: float) -> ParametricFunction:
            def function_interp(v: float) -> Callable[float, float]:
                def func(t: float) -> float:
                    return v * t - 0.5 * car_acc * (t - reaction) ** 2
                return func

            return axes.plot(function=function_interp(v), x_range=[0, axes.x_range[1]], color=YELLOW, use_vectorized=True)

        axes = Axes(
            x_range=[0, 7, 20],
            y_range=[0, 5, 20]
        )

        car_plot = get_car_plot(axes, 1)

        self.play(
            Create(axes),
            Create(car_plot)
        )
        def update_car_plot(beginning: float, end: float) \
            -> Callable[ParametricFunction, float]:
            def update_plot(plot: ParametricFunction, alpha: float) -> ParametricFunction:
                new_v = integer_interpolate(beginning, end, alpha)
                new_plot = get_car_plot(axes, new_v[0] + new_v[1])
                Transform(plot, new_plot).update_mobjects(1)
                return new_plot

            return update_plot

        self.wait(duration)

        self.play(
            UpdateFromAlphaFunc(
                car_plot,
                update_function=lambda d, a: update_car_plot(1, 4)(d, a),
                duration=2,
                rate_func=smooth
            )
        )