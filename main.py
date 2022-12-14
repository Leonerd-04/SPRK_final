from colour import Color
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import numpy as np


class MainScene(VoiceoverScene):

    def add_voiceover_ssml(self, ssml: str, **kwargs) -> None:
        pass

    def construct(self):
        self.set_speech_service(GTTSService(transcription_model="base"))
        self.play_introduction_scene()
        self.play_pedestrian_graph_scene()
        self.play_roadside_tree_scene()
        self.play_site_visit_scene()
        self.play_conclusion_scene()
        self.show_credits()

    def make_title(self, text: str, duration: float):
        title = Tex(text, font_size=64)

        self.play(Write(title, run_time=0.8))
        self.wait(duration)
        self.play(Unwrite(title, run_time=0.8))

    def play_introduction_scene(self):
        fatalities = VGroup()
        initial = Circle(0.07, stroke_opacity=0, fill_opacity=1, fill_color="#D80D8E")

        for i in range(30):
            for j in range(40):
                fatalities.add(initial.copy().shift(RIGHT * j / 4 + DOWN * i / 4))

        fatalities.move_to([0, 0, 0])

        with self.voiceover(
                text="""In 2020, 1200 pedestrians died in car collisions in America, 
                or three and a half people per day.
                """
        ):
            self.play(
                FadeIn(fatalities, shift=DOWN, lag_ratio=0.04),
                run_time=2.5
            )

        with self.voiceover(
            text="""It’s clear we need to make our streets safer for pedestrians to be able to use them effectively, 
            especially when considering the future importance of walkable urban environments. 
            Walking and transit-oriented design are not only better for the environment due to their lower emissions, 
            but also allows those in society who can’t drive, like children, the elderly, 
            and those with certain disabilities, to retain or gain independence."""
        ):
            pass

        with self.voiceover(
                text="""There are two main factors I want to talk about when it comes to 
                increasing pedestrian safety. One is the frequency of car-pedestrian collisions. 
                This is something we’ll want to decrease. 
                Another, slightly more complex, is the speed of the cars on the road."""
        ):
            self.play(
                FadeOut(fatalities, shift=DOWN, lag_ratio=0.04),
                run_time=2.5
            )

    def play_pedestrian_graph_scene(self):

        #(No speech)
        self.make_title(r"The Mathematics of Collisions", 2)
        #(No speech)

        with self.voiceover(
            text="While it may be obvious to us that faster cars are more dangerous, it’s good to quantify their impact a bit more precisely."
        ):
            pass

        #"One study found a ... the probability of death."
        self.display_prob_func()
        #"The driver may be ... at some given distance"

        #"We can visualize the collision with a position vs time graph"
        self.pos_vs_time()

        self.wait(2.5)

    def display_prob_func(self):
        line_color = Color()
        line_color.set_hex("#D8570D")
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

        plot: ParametricFunction = axes.plot(prob_func, color=TEAL)

        labels = axes.get_axis_labels(x_label=Tex("$v$"), y_label=Tex("$P(v)$"))

        with self.voiceover(text="One study found a relationship between car impact velocity and pedestrian fatality,") as tracker:
            self.play(
                Write(prob_func_tex,run_time=tracker.duration / 2),
                Create(axes, run_time=(tracker.duration / 2), lag_ratio=0),
                Create(plot),
                Write(labels, run_time=1)
            )

        with self.voiceover(
                text="""relating them with the logistical equation shown here, 
                where v is the impact velocity of the collision in kilometers per hour, 
                and P of v is the probability of the pedestrian dying.""",
                subcaption="""relating them with the logistical equation shown here, 
                where v is the impact velocity of the collision in km/hr, 
                and P(v) is the probability of the pedestrian dying."""
        ):
            pass

        inp = ValueTracker(20)
        self.add(inp)
        point = Dot(point=axes.c2p(inp.get_value(), prob_func(inp.get_value())), color=line_color)
        point.add_updater(lambda this: this.move_to(axes.c2p(inp.get_value(), prob_func(inp.get_value()))))

        vert_line = axes.get_vertical_line(axes.c2p(inp.get_value(), prob_func(inp.get_value())), color=line_color)
        vert_line.add_updater(
            lambda this: this.set_points(
                axes.get_vertical_line(
                    axes.c2p(inp.get_value(), prob_func(inp.get_value()))
                ).get_all_points()
            )
        )

        horz_line = axes.get_horizontal_line(axes.c2p(inp.get_value(), prob_func(inp.get_value())), color=line_color)
        horz_line.add_updater(
            lambda this: this.set_points(
                axes.get_horizontal_line(
                    axes.c2p(inp.get_value(), prob_func(inp.get_value()))
                ).get_all_points()
            )
        )

        self.play(
            Create(point)
        )
        self.add(horz_line, vert_line)

        with self.voiceover(
            text="""We can see that the severity of car collisions <bookmark mark='A'/> increases with impact speed, 
            however I also want to emphasize the difference between the impact speed 
            (the speed at which the car hits the pedestrian) and the cruising speed of the car.""",
            subcaption="""We can see that the severity of car collisions increases with impact speed, 
			however I also want to emphasize the difference between the impact speed 
			(the speed at which the car hits the pedestrian) and the cruising speed of the car."""
        ):
            self.wait_until_bookmark("A")

            self.play(inp.animate.set_value(140), rate_func=rate_functions.ease_in_out_sine, run_time=4)

        self.play(
            Unwrite(prob_func_tex, run_time=1),
            Uncreate(axes, run_time=2),
            Uncreate(plot),
            Unwrite(labels, run_time=1),
            Uncreate(point, run_time=2),
            Uncreate(vert_line, run_time=2),
            Uncreate(horz_line, run_time=2)
        )

    def pos_vs_time(self):
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
            x_range=[0, 5, 20],
            y_range=[0, 5, 20],
            x_length=5,
            y_length=5
        )

        labels = axes.get_axis_labels(x_label=Tex("$t$"), y_label=Tex("$x$"))

        car_plot = get_car_plot(axes, velocity.get_value())
        car_plot.add_updater(
            lambda this: this.set_points(
                get_car_plot(axes, velocity.get_value()).get_all_points()
            )
        )

        pedestrian_plot = axes.plot(lambda t: dist, color=ped_color)

        with self.voiceover(
                text="""We can visualize the collision with a position vs time graph, 
                where the horizontal axis is the time t, and the vertical axis is the position x along the road."""
        ):
            self.play(
                Create(axes),
                Create(car_plot),
                Create(pedestrian_plot),
                Write(labels),
                run_time=3
            )

        with self.voiceover(
            text="""The pink curve is the pedestrian and the yellow curve is a car 
            on a collision course with the pedestrian. The slope of a line represents the speed of the object, 
            so the pedestrian’s line is horizontal because they don’t move along the road all that much."""
        ):
            pass

        #"If these two curves happen to intersect..."
        with self.voiceover(
                text="""If these two curves happen to intersect, 
                the car and the pedestrian have the same position and a collision happens."""
        ):
            self.play(
                velocity.animate.set_value(1.2),
                run_time=0.7
            )

        # Line to demonstrate where the acceleration starts
        line = axes.get_vertical_line(axes.c2p(reaction, velocity.get_value() * reaction), color=TEAL)
        line.add_updater(
            lambda this: this.replace(
                axes.get_vertical_line(
                    axes.c2p(reaction, velocity.get_value() * reaction),
                    color=TEAL
                ),
                stretch=True
            )
        )

        temp_line = Line(start=axes.coords_to_point(0, 0), end=axes.coords_to_point(reaction))

        brace = Brace(temp_line)
        brace_text = Tex("Reaction Time", font_size=24).next_to(brace, DOWN * 1/2)

        with self.voiceover(
                text="""Because human brains are slow and take time to react to events, 
                there will be a little bit of time <bookmark mark='A'/>after seeing a pedestrian on the road 
                where the driver won’t react, called the <bookmark mark='B'/>reaction time.""",
                subcaption="""Because human brains are slow and take time to react to events, 
                there will be a little bit of time after seeing a pedestrian on the road 
                where the driver won’t react, called the reaction time."""
        ):
            self.wait_until_bookmark("A")
            self.play(
                Create(line)
            )
            self.wait_until_bookmark("B")
            self.play(
                Write(brace),
                Write(brace_text)
            )

        #"We can see now that changing..."
        with self.voiceover(
            text="""We can see now that changing <bookmark mark='A'/>the cruising speed of the car 
            (the slope of the line at t = 0) changes the impact speed 
            (the slope of the line at the collision) by a lot.""",
            subcaption="""We can see now that changing the cruising speed of the car 
            (the slope of the line at t = 0) changes the impact speed 
            (the slope of the line at the collision) by a lot."""
        ):
            self.wait_until_bookmark("A")
            self.play(
                velocity.animate.set_value(1.26),
                rate_func=wiggle,
                run_time=3
            )

        with self.voiceover(
                text="""Low enough cruising speeds allow the car to come to a full stop and avoid a collision, 
                <bookmark mark='A'/>but as the cruising speed rises, the impact speed rises a lot faster until 
                the driver can’t react to the collision anymore and doesn't hit the brakes before colliding.""",
                subcaption="""Low enough cruising speeds allow the car to come to a full stop and avoid a collision, 
                but as the cruising speed rises, the impact speed rises a lot faster until 
                the driver can’t react to the collision anymore and doesn't hit the brakes before colliding."""
        ):
            self.play(
                velocity.animate.set_value(0.4),
                run_time=1.2
            )

            self.wait_until_bookmark("A")
            self.play(
                velocity.animate.set_value(1.3),
                run_time=3
            )

        self.play(
            Uncreate(axes),
            Uncreate(car_plot),
            Uncreate(pedestrian_plot),
            Unwrite(labels),
            Uncreate(line),
            Unwrite(brace),
            Unwrite(brace_text)
        )

    def play_roadside_tree_scene(self):
        self.make_title(r"Designing Streets for Safety", 1.6)

        with self.voiceover(
            text="""We are now more aware of what goes into
            making car collisions dangerous, but how do we design
            streets to mitigate this risk?"""
        ):
            pass

        self.show_road_with_trees()

        self.show_traffic_lanes()

    def show_road_with_trees(self):

        column_left = self.create_tree_column(-2.5)
        column_right = self.create_tree_column(2.5)

        road_left = Line(start=[-1.2, -5, 0], end=[-1.2, 5, 0], color=WHITE)
        road_right = Line(start=[1.2, -5, 0], end=[1.2, 5, 0], color=WHITE)
        road_divide = DashedLine(start=[0, -5, 0], end=[0, 5, 0], color=YELLOW, dash_length=0.5)

        with self.voiceover(text="""One way is with trees on the side of the road."""):
            self.play(
                Create(column_left, lag_ratio=0.15),
                Create(column_right, lag_ratio=0.15),
                Write(road_left),
                Write(road_divide),
                Write(road_right)
            )

        with self.voiceover(
            text="""One study found that having trees <bookmark mark='A'/>closer to 
            the side of the road slowed drivers down by up to 10%.""",
            subcaption="""One study found that having trees closer to 
            the side of the road slowed drivers down by up to 10%."""
        ):
            self.wait_until_bookmark("A")
            self.play(
                column_left.animate.shift(RIGHT * 0.6),
                column_right.animate.shift(LEFT * 0.6)
            )

        with self.voiceover(
            text = """They also found that having the trees closer leads to 
            drivers driving further from the edge of the road. 
            The authors theorized this to be due to the drivers’ risk assessment, 
            however I also believe the trees’ apparent speed plays a factor. """
        ):
            pass

        self.play(
            Uncreate(column_left, lag_ratio=0.15),
            Uncreate(column_right, lag_ratio=0.15),
            Unwrite(road_left),
            Unwrite(road_divide),
            Unwrite(road_right)
        )

        # Lens shape for the eye's outline
        # Sclera is the white part of the eye
        sclera = Intersection(
            Circle(0.8).shift(UP / 2),
            Circle(0.8).shift(DOWN / 2)
        ).shift(LEFT * 2)

        pupil = Circle(
            radius=0.26,
            stroke_color="#1AB1E0"
        ).shift(LEFT * 2)

        eye = VGroup(sclera, pupil)
        tree = self.create_tree().shift(2 * RIGHT).scale(2)

        tree_eye_line = Line(start=eye.get_center(), end=tree.get_center(), stroke_width=2, color="#E97010")
        tree_eye_line.add_updater(
            lambda this: this.set_points(Line(start=eye.get_center(), end=tree.get_center()).get_all_points())
        )

        with self.voiceover(
            text="""We can’t perceive the absolute distance we travel, only the <bookmark mark='A'/>change in angle 
            of things in our field of view. This change decreases with <bookmark mark='B'/>distance to an observer, 
            so the further the trees are from the road, the less they move across one’s field of vision,
            and the lower the perceived speed. """,
            subcaption="""We can’t perceive the absolute distance we travel, only the change in angle 
            of things in our field of view. This change decreases with distance to an observer, 
            so the further the trees are from the road, the less they move across one’s field of vision,
            and the lower the perceived speed. """
        ):
            self.play(
                Write(eye),
                Create(tree, lag_ratio=0.1)
            )

            self.add(tree_eye_line)

            self.wait_until_bookmark("A")
            self.play(
                tree.animate.shift(UP * 2),
                rate_func=wiggle,
                run_time=2
            )

            self.wait_until_bookmark("B")
            self.play(
                tree.animate.shift(RIGHT * 3),
                eye.animate.shift(LEFT * 3),
                run_time=1.5
            )

            self.play(
                tree.animate.shift(UP * 2),
                rate_func=wiggle,
                run_time=2
            )

        with self.voiceover(text="Either way, roadside trees seem to be something favorable for our streets."):
            pass

        self.play(
            Unwrite(eye),
            Uncreate(tree, lag_ratio=0.1),
            Unwrite(tree_eye_line)
        )

    def show_traffic_lanes(self):
        with self.voiceover(text="Another way to increase safety is to decrease traffic lane size, to a point anyways."):
            pass
        lane_width = ValueTracker(3)

        def create_road(width: ValueTracker) -> VGroup:
            road = VGroup()
            center = Line(start=[0, -5, 0], end=[0, 5, 0], color=YELLOW)
            left = Line(start=[-width.get_value(), -5, 0], end=[-width.get_value(), 5, 0])
            left.add_updater(
                lambda this: this.set_points(
                    Line(start=[-width.get_value(), -5, 0], end=[-width.get_value(), 5, 0]).get_all_points())
            )
            right = Line(start=[width.get_value(), -5, 0], end=[width.get_value(), 5, 0])
            right.add_updater(
                lambda this: this.set_points(
                    Line(start=[width.get_value(), -5, 0], end=[width.get_value(), 5, 0]).get_all_points())
            )
            road.add(center)
            road.add(left)
            road.add(right)

            return road

        road = create_road(lane_width)
        lane_width_tracker = Variable(var=lane_width.get_value(), label="Lane Width", num_decimal_places=1).to_corner(corner=LEFT+UP)
        lane_width_tracker.add_updater(lambda this: this.tracker.set_value(lane_width.get_value()))
        self.add(road)
        self.play(
            Write(lane_width_tracker)
        )

        with self.voiceover(
                text="""Two studies both found some evidence that, for lanes wider than 3-3.6 meters, 
                the <bookmark mark='A'/>wider the lane, the less safe it was for pedestrians. 
                One study cited increasing collision frequency as the cause.""",
                subcaption="""Two studies both found some evidence that, for lanes wider than 3-3.6 meters, 
                the wider the lane, the less safe it was for pedestrians. 
                One study cited increasing collision frequency as the cause."""
        ):
            self.wait_until_bookmark("A")
            self.play(
                lane_width.animate.set_value(4),
                run_time=1
            )

        with self.voiceover(
            text="""I’m also inclined to believe that perceived speed is a factor here too, 
            since a wider lane has lane dividers that move more slowly across a driver’s field of vision, 
            by the principles mentioned with the trees."""
        ):
            pass

        self.play(
            Unwrite(road),
            Unwrite(lane_width_tracker)
        )

    def play_site_visit_scene(self):
        self.make_title(r"Designs in the Real World", 1.6)
        with self.voiceover("It’s good to confirm predictions or results we make with a real world example."):
            pass
        self.introduce_locations()
        self.show_satellite_images()
        pass

    def introduce_locations(self):
        ucm_image = ImageMobject(filename_or_array="images/UC Merced.jpeg", scale_to_resolution=720).shift(LEFT * 4)
        bak_image = ImageMobject(filename_or_array="images/Bakersfield.jpeg", scale_to_resolution=720).shift(RIGHT * 4)

        with self.voiceover(
            text="""For this, I chose two locations to compare, being my college, <bookmark mark='A'/>UC Merced, 
            a pedestrian heavy place with little motor vehicle traffic, and some suburban streets 
            in my hometown of <bookmark mark='B'/>Bakersfield, which is much more car-centric.""",
            subcaption="""For this, I chose two locations to compare, being my college, UC Merced, 
            a pedestrian heavy place with little motor vehicle traffic, and some suburban streets 
            in my hometown of Bakersfield, which is much more car-centric."""
        ):
            self.wait_until_bookmark("A")
            self.play(
                FadeIn(ucm_image, shift=DOWN)
            )

            self.wait_until_bookmark("B")
            self.play(
                FadeIn(bak_image, shift=DOWN)
            )


        self.play(
            FadeOut(bak_image, shift=DOWN),
            FadeOut(ucm_image, shift=DOWN)
        )

        scholars_lane = ImageMobject(filename_or_array="images/Scholars Lane.JPG", scale_to_resolution=4320).shift(LEFT * 4)
        bak_street = ImageMobject(filename_or_array="images/Bakersfield Street.JPG", scale_to_resolution=4320).shift(RIGHT * 4)

        with self.voiceover(
                text="""Visiting UC Merced’s Scholars’ Lane, a paved street spanning the length of the university, 
                I saw <bookmark mark='A'/>rows of trees lining the edges of the streets, as well as thinner lanes. As a bonus, 
                the trees lie between the sidewalk and the paved road, which acts like a buffer zone between 
                cars and pedestrians.""",
                subcaption="""Visiting UC Merced’s Scholars’ Lane, a paved street spanning the length of the university, 
                I saw rows of trees lining the edges of the streets, as well as thinner lanes. As a bonus, 
                the trees lie between the sidewalk and the paved road, which acts like a buffer zone between 
                cars and pedestrians."""
        ):
            self.wait_until_bookmark("A")
            self.play(
                FadeIn(scholars_lane, shift=DOWN)
            )

        with self.voiceover(
            text="""Looking at a residential street in Bakersfield, we can see <bookmark mark='A'/>much wider lanes, 
            and while roadside trees are present they are much further away from the road’s center 
            by virtue of the road itself simply being wider.""",
            subcaption="""Looking at a residential street in Bakersfield, we can see much wider lanes, 
            and while roadside trees are present they are much further away from the road’s center 
            by virtue of the road itself simply being wider."""
        ):
            self.wait_until_bookmark("A")
            self.play(
                FadeIn(bak_street, shift=DOWN)
            )

        self.play(
            FadeOut(bak_street, shift=DOWN),
            FadeOut(scholars_lane, shift=DOWN)
        )

    def show_satellite_images(self):
        ucm_image = ImageMobject(filename_or_array="images/Scholars Lane Satellite.png", scale_to_resolution=1080).shift(LEFT * 4)
        ucm_text = Tex("4.2 m").next_to(ucm_image, direction=DOWN)
        ucm = Group(ucm_image, ucm_text)

        bak_image = ImageMobject(filename_or_array="images/Bakersfield Satellite.png", scale_to_resolution=1080).shift(RIGHT * 4)
        bak_text = Tex("8.5 m").next_to(bak_image, direction=DOWN)
        bak = Group(bak_image, bak_text)

        with self.voiceover(
            text="""Actually measuring the road’s width using satellite imaging yields a width of <bookmark mark='A'/>4.2 meters
            for Scholars’ Lane, and <bookmark mark='B'/>8.5 meters for Bakersfield’s residential roads. While both are higher than 
            the 3-3.6 meters recommended by the studies mentioned earlier, Scholar’s Lane still has a much closer 
            width to the recommended than Bakersfield’s streets.""",
            subcaption="""Actually measuring the road’s width using satellite imaging yields a width of 4.2 m
            for Scholars’ Lane, and 8.5 m for Bakersfield’s residential roads. While both are higher than 
            the 3-3.6 m recommended by the studies mentioned earlier, Scholar’s Lane still has a much closer 
            width to the recommended than Bakersfield’s streets."""
        ):
            self.wait_until_bookmark("A")
            self.play(
                FadeIn(ucm, shift=DOWN, lag_ratio=0.2)
            )

            self.wait_until_bookmark("B")
            self.play(
                FadeIn(bak, shift=DOWN, lag_ratio=0.2)
            )

        self.play(
            FadeOut(ucm, shift=DOWN, lag_ratio=0.2),
            FadeOut(bak, shift=DOWN, lag_ratio=0.2)
        )

    def play_conclusion_scene(self):
        self.make_title(r"Conclusion", 1.6)
        road_left = Line(start=[-1.2, -5, 0], end=[-1.2, 5, 0], color=WHITE)
        road_right = Line(start=[1.2, -5, 0], end=[1.2, 5, 0], color=WHITE)
        road_divide = DashedLine(start=[0, -5, 0], end=[0, 5, 0], color=YELLOW, dash_length=0.5)

        column_left = self.create_tree_column(-2.5)
        column_right = self.create_tree_column(2.5)

        with self.voiceover(
            text="""So, we can now conclude that <bookmark mark='A'/>lane width and <bookmark mark='B'/>roadside trees 
            are important factors for improving pedestrian safety, by having considered both some studies 
            into how these affect safety, and actual sites that exhibit these characteristics. 
            These findings can be incorporated into building new streets, or remodeling old ones, to 
            improve pedestrian safety and hopefully take a step towards a better, more walkable future.""",
            subcaption="""So, we can now conclude that lane width and roadside trees 
            are important factors for improving pedestrian safety, by having considered both some studies 
            into how these affect safety, and actual sites that exhibit these characteristics. 
            These findings can be incorporated into building new streets, or remodeling old ones, to 
            improve pedestrian safety and hopefully take a step towards a better, more walkable future."""
        ):
            self.wait_until_bookmark("A")
            self.play(
                Write(road_left),
                Write(road_right),
                Write(road_divide)
            )

            self.wait_until_bookmark("B")
            self.play(
                Create(column_left),
                Create(column_right)
            )

        self.wait()

        self.play(
            Unwrite(road_left),
            Unwrite(road_right),
            Unwrite(road_divide),
            Uncreate(column_left),
            Uncreate(column_right)
        )

        self.wait()

    def show_credits(self):
        line1 = Tex("By Leonardo Gil Rojo").shift(UP)
        line2 = Tex("Made using the Manim animation library").shift(DOWN)

        self.play(
            Write(line1)
        )

        self.wait(4)

        self.play(
            Write(line2)
        )

        self.wait(5)

    def create_tree_column(self, position: float) -> VGroup:
        column = VGroup()
        tree = self.create_tree()

        tree.move_to(point_or_mobject=[position, -5, 0])
        column.add(tree)

        # Copies the tree shape to make a whole column
        for i in range(10):
            column.add(tree.copy().shift(i * UP))

        return column

    def create_tree(self) -> VGroup:
        tree = VGroup()
        shrub_1 = Ellipse(0.45, 0.195, fill_color="#57A275", stroke_opacity=0, fill_opacity=1)

        tree.add(shrub_1)

        # Rotating the ellipse discretely produces a shrub-like shape
        for i in range(7):
            tree.add(shrub_1.copy().rotate(i * PI / 4))

        return tree
