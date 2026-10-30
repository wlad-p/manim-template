"""
End screen: "Thank you so much for watching…" — 9.3 s static layout with two
video slots for YouTube's end-screen elements, the logo, and a small
like / subscribe animation.

Render:
    manim -pql endscreen.py EndScreen     # quick preview (480p15)
    manim -pqh endscreen.py EndScreen     # final (1080p60)

The dashed boxes are where to place YouTube's end-screen elements:
two video elements (16:9) and the round subscribe element.
Put the narration at ./sounds/endscreen.mp3 to have it added automatically.
"""

from pathlib import Path

from manim import *

HERE = Path(__file__).resolve().parent
SOUND = HERE / "sounds" / "endscreen.mp3"

# ---------------------------------------------------------------- style ----
BG = "#123b2a"
TEXT_C = "#E8ECF2"
MUTED = "#8A94A6"
IP_C = "#ff503aff"
V6_C = "#46DC6E"
YT_RED = "#FF0033"
SUBBED_C = "#4A5263"

PANEL_FILL = "#1A4A36"
PANEL_STROKE = "#2A5E47"

FONT = "Comfortaa"
MONO = "Comfortaa"

config.background_color = BG

DURATION = 9.3

# No label file for this one: beats are estimated from the line
# "Thank you so much for watching, guys! If you enjoyed the video, hit the like
#  button and subscribe. Also check out my other videos on my channel.
#  See you in the next one."  Adjust once you have the recording.
MARKERS = {
    "like": 3.4,        # "…hit the like button"
    "subscribe": 4.9,   # "…and subscribe."
    "videos": 6.2,      # "Also check out my other videos on my channel."
    "end": DURATION,
}

# Layout (Manim units; the frame is 14.22 x 8)
VIDEO_W = 5.4                       # 16:9 slots
VIDEO_H = VIDEO_W * 9 / 16
VIDEO_Y = 0.1
VIDEO_X = 3.15
SUB_R = 0.62                        # round subscribe element
BOTTOM_Y = -2.95


# -------------------------------------------------------------- helpers ----
def txt(s, size=24, color=TEXT_C, font=FONT, **kw):
    return Text(s, font=font, font_size=size, color=color, **kw)


def block(w, h, color, r=0.06):
    return RoundedRectangle(
        corner_radius=r, width=w, height=h,
        fill_color=color, fill_opacity=1, stroke_width=0,
    )


def video_slot(label):
    box = RoundedRectangle(corner_radius=0.12, width=VIDEO_W, height=VIDEO_H, stroke_width=0,
                           fill_color=PANEL_FILL, fill_opacity=0.8)
    dash = DashedVMobject(box.copy().set_stroke(PANEL_STROKE, 3).set_fill(opacity=0), num_dashes=60)
    tri = Triangle(fill_color=PANEL_STROKE, fill_opacity=1, stroke_width=0).rotate(-PI / 2).scale(0.35)
    lbl = txt(label, 20, MUTED).next_to(tri, DOWN, buff=0.3)
    return VGroup(box, dash, VGroup(tri, lbl).move_to(box))


def thumb_up(height=0.9, color=TEXT_C):
    cuff = RoundedRectangle(corner_radius=0.06, width=0.22, height=0.6)
    palm = RoundedRectangle(corner_radius=0.14, width=0.55, height=0.62).next_to(cuff, RIGHT, buff=0.06)
    thumb = RoundedRectangle(corner_radius=0.1, width=0.2, height=0.5).rotate(-0.45)
    thumb.move_to(palm.get_corner(UL) + RIGHT * 0.2 + UP * 0.12)
    icon = VGroup(cuff, palm, thumb).set_stroke(color, 5).set_fill(color, 0)
    return icon.scale_to_fit_height(height)


def bell(height=0.55, color=TEXT_C):
    dome = Arc(radius=0.3, start_angle=0, angle=PI)
    sides = VMobject().set_points_as_corners([[-0.3, 0, 0], [-0.38, -0.32, 0], [0.38, -0.32, 0], [0.3, 0, 0]])
    clapper = Dot([0, -0.42, 0], radius=0.07)
    knob = Dot([0, 0.33, 0], radius=0.05)
    g = VGroup(dome, sides).set_stroke(color, 5)
    return VGroup(g, clapper.set_color(color), knob.set_color(color)).scale_to_fit_height(height)


def sub_button(label, fill, text_color=TEXT_C):
    t = txt(label, 22, text_color, weight=BOLD)
    box = block(t.width + 0.6, t.height + 0.4, fill, 0.3)
    return VGroup(box, t.move_to(box))


def cursor(size=0.5):
    pts = [(0, 0), (0, -0.62), (0.15, -0.48), (0.27, -0.74), (0.37, -0.69), (0.25, -0.44), (0.45, -0.44)]
    return Polygon(*[[x, y, 0] for x, y in pts], fill_color=TEXT_C, fill_opacity=1,
                   stroke_color=BG, stroke_width=2).scale_to_fit_height(size)


def click(self, cur, target, run_time=0.6):
    """Move the cursor's tip to target, then press."""
    tip_offset = cur.get_corner(UL) - cur.get_center()
    self.play(cur.animate.move_to(target - tip_offset), run_time=run_time)
    self.play(cur.animate.scale(0.8, about_point=cur.get_corner(UL)), run_time=0.1)
    self.play(cur.animate.scale(1.25, about_point=cur.get_corner(UL)), run_time=0.1)


# ---------------------------------------------------------------- scene ----
class EndScreen(Scene):
    def construct(self):
        self.late = []
        self.camera.background_image = str(HERE / "images" / "bg-gradient.png")
        self.camera.init_background()
        
        if SOUND.exists():
            self.add_sound(str(SOUND))

        # --- static layout ------------------------------------------------
        logo = SVGMobject(str(HERE / "images" / "kinda-no-bg.svg")).scale_to_fit_height(0.85).move_to(3*UP)
        thanks = txt("Thanks for watching!", 40, TEXT_C, weight=BOLD).move_to(ORIGIN)

        like = thumb_up(0.75).move_to([-3.6, BOTTOM_Y, 0])
        like_lbl = txt("Like", 22, TEXT_C, weight=BOLD).next_to(like, RIGHT, buff=0.25)
        like_grp = VGroup(like, like_lbl)

        subscribe = sub_button("SUBSCRIBE", YT_RED).move_to([3.2, BOTTOM_Y, 0])
        ring = bell(0.5).next_to(subscribe, RIGHT, buff=0.35)

        # 0.00  "Thank you so much for watching, guys!"
        self.play(FadeIn(thanks, shift=DOWN * 0.2), FadeIn(logo, shift = DOWN * 0.2), FadeIn(like_grp), FadeIn(subscribe), FadeIn(ring), run_time=0.8)

        cur = cursor(0.5).move_to([0.5, -1.6, 0])

        # 3.40  "…hit the like button"
        self.at(MARKERS["like"] - 0.9, "like")
        self.play(FadeIn(cur), run_time=0.2)
        click(self, cur, like.get_center() + RIGHT * 0.05)
        plus = txt("+1", 24, YT_RED, weight=BOLD).next_to(like, UP, buff=0.1)
        self.play(like.animate.set_fill(TEXT_C, 1), like_lbl.animate.set_color(TEXT_C),
                  Flash(like, color=TEXT_C, line_length=0.18, flash_radius=0.6),
                  FadeIn(plus, shift=UP * 0.2), run_time=0.4)
        self.play(FadeOut(plus, shift=UP * 0.2), run_time=0.3)

        # 4.90  "…and subscribe."
        self.at(MARKERS["subscribe"] - 0.7, "subscribe")
        click(self, cur, subscribe.get_center(), run_time=0.5)
        subbed = sub_button("SUBSCRIBED", SUBBED_C, TEXT_C).move_to(subscribe)
        self.play(FadeTransform(subscribe, subbed), run_time=0.3)
        click(self, cur, ring.get_center(), run_time=0.35)
        self.play(Wiggle(ring, scale_value=1.15, rotation_angle=0.08 * TAU), run_time=0.45)

        # 6.20  "Also check out my other videos on my channel."
        self.at(MARKERS["videos"], "videos")
        self.play(FadeOut(cur), run_time=0.2)

        # "See you in the next one." — hold the layout to the end
        self.at(MARKERS["end"], "end")

        if self.late:
            print("\n[sync] Beats that started late (animations ran past the marker):")
            for key, d in self.late:
                print(f"   {key:<16} +{d:.2f}s")
        else:
            print("\n[sync] All beats on time.")

    # --- timing ---------------------------------------------------------
    def now(self):
        return self.renderer.time

    def at(self, t, key=""):
        """Wait until absolute time t (seconds from the start of the scene)."""
        gap = t - self.now()
        if gap > 0.01:
            self.wait(gap)
        elif gap < -0.05:
            self.late.append((key or f"{t:.2f}s", -gap))
