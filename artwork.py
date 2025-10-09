import turtle
import random
import math
import colorsys
import time

# ----------------------------
# Configuration
# ----------------------------
WIDTH, HEIGHT = 1000, 700
NUM_PARTICLES = 220       # number of particles
MAX_SPEED = 2.2
PARTICLE_SIZE = (2, 6)    # min, max dot size
TRAIL_ALPHA = 0.08        # not directly supported; simulated via background repaint
FPS = 60
COLOR_CYCLE_SPEED = 0.12  # how fast hues change
WAVE_ELEMENTS = 8

# ----------------------------
# Utilities
# ----------------------------
def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h % 1.0, max(0, min(s, 1)), max(0, min(v, 1)))
    return int(r * 255), int(g * 255), int(b * 255)

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def clamp(x, a, b):
    return max(a, min(b, x))

# ----------------------------
# Turtle setup
# ----------------------------
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("Turtle Particle Art")
screen.colormode(255)
screen.tracer(0, 0)  # manual updates for smooth animation
screen.bgcolor((8, 6, 20))  # dark base

# Create dedicated turtles for layers
bg_turtle = turtle.Turtle(visible=False)
bg_turtle.penup()
bg_turtle.hideturtle()

shape_turtle = turtle.Turtle(visible=False)
shape_turtle.hideturtle()
shape_turtle.penup()

particle_turtle = turtle.Turtle(visible=False)
particle_turtle.hideturtle()
particle_turtle.penup()

overlay_turtle = turtle.Turtle(visible=False)
overlay_turtle.hideturtle()
overlay_turtle.penup()

# ----------------------------
# Background gradient painter
# ----------------------------
def paint_background(hue_offset):
    """Simulate a vertical gradient using thin horizontal fills."""
    # We'll paint only a few thin stripes to avoid slowing down too much.
    stripes = 60
    w, h = WIDTH, HEIGHT
    start_y = -h // 2
    step = h / stripes
    bg_turtle.clear()
    for i in range(stripes):
        t = i / max(1, stripes - 1)
        # hue shifts top to bottom and add animated offset
        hue = (hue_offset * 0.12 + 0.55 * t) % 1.0
        sat = 0.55 + 0.25 * math.sin(hue_offset * 0.5 + t * 4.0)
        val = 0.05 + 0.45 * (1 - (t*0.9))
        color = rgb_to_hex(hsv_to_rgb(hue, sat, val))
        bg_turtle.goto(-w//2, start_y + i*step)
        bg_turtle.color(color)
        bg_turtle.begin_fill()
        bg_turtle.setheading(0)
        bg_turtle.pendown()
        # draw thin rectangle
        bg_turtle.forward(w)
        bg_turtle.left(90)
        bg_turtle.forward(step + 1)
        bg_turtle.left(90)
        bg_turtle.forward(w)
        bg_turtle.left(90)
        bg_turtle.forward(step + 1)
        bg_turtle.left(90)
        bg_turtle.penup()
        bg_turtle.end_fill()

# ----------------------------
# Decorative shapes (rotating mandala-like)
# ----------------------------
def draw_mandala(cx, cy, radius, layers, hue_offset):
    shape_turtle.clear()
    for L in range(layers):
        r = radius * (0.18 + 0.9 * (L / layers))
        parts = 6 + L*2
        for i in range(parts):
            ang = (i / parts) * 360 + hue_offset * (6 + L)
            x = cx + math.cos(math.radians(ang)) * r
            y = cy + math.sin(math.radians(ang)) * r
            hue = (hue_offset * 0.07 + 0.07 * L + i / parts) % 1.0
            color = rgb_to_hex(hsv_to_rgb(hue, 0.85, 1.0 - 0.12*L))
            shape_turtle.goto(x, y)
            shape_turtle.dot(8 + int(6 * math.sin(hue_offset * 0.2 + L)), color)

# ----------------------------
# Particles
# ----------------------------
class Particle:
    def __init__(self, w, h, hue_base):
        self.w = w; self.h = h
        self.reset(hue_base)

    def reset(self, hue_base=None):
        # spawn around center with some randomness
        self.x = random.uniform(-self.w*0.45, self.w*0.45)
        self.y = random.uniform(-self.h*0.45, self.h*0.45)
        angle = random.uniform(0, math.tau)
        speed = random.uniform(0.2, MAX_SPEED)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.size = random.uniform(*PARTICLE_SIZE)
        self.life = random.uniform(4.0, 12.0)
        self.age = random.uniform(0, self.life)
        self.hue_offset = random.uniform(0, 1)
        # initial alpha for fade effect simulated by size & brightness
        self.hue_base = hue_base if hue_base is not None else random.random()

    def update(self, dt, hue_global, attractors):
        # Move
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Small wandering force
        wobble = 0.06
        ang = math.sin((self.x + self.y) * 0.01 + hue_global * 2.3)
        self.vx += wobble * math.cos(ang) * dt
        self.vy += wobble * math.sin(ang) * dt

        # Attractors affect velocity
        for ax, ay, power in attractors:
            dx = ax - self.x
            dy = ay - self.y
            d2 = dx*dx + dy*dy + 1e-6
            force = power / d2
            self.vx += dx * force * dt
            self.vy += dy * force * dt

        # Lifespan
        self.age += dt
        if self.age >= self.life:
            self.reset(hue_global)

        # Wrap-around edges with soft bounce
        margin = 20
        if self.x < -self.w/2 - margin: self.x = self.w/2 + margin
        if self.x > self.w/2 + margin:  self.x = -self.w/2 - margin
        if self.y < -self.h/2 - margin: self.y = self.h/2 + margin
        if self.y > self.h/2 + margin:  self.y = -self.h/2 - margin

    def draw(self, pen, hue_global):
        # brightness fades with life
        life_ratio = clamp(1 - (self.age / self.life), 0.0, 1.0)
        hue = (self.hue_base + hue_global*COLOR_CYCLE_SPEED*0.3) % 1.0
        sat = 0.75 + 0.2 * life_ratio
        val = 0.5 + 0.5 * life_ratio
        color = rgb_to_hex(hsv_to_rgb(hue, sat, val))
        # size pulsates slightly
        dot_size = self.size * (0.8 + 0.6 * life_ratio)
        pen.goto(self.x, self.y)
        pen.dot(max(1, int(dot_size)), color)

# ----------------------------
# Build particles
# ----------------------------
particles = [Particle(WIDTH, HEIGHT, random.random()) for _ in range(NUM_PARTICLES)]

# ----------------------------
# Animation loop
# ----------------------------
last_time = time.time()
hue_global = 0.0
frame_count = 0

def animation_step():
    global last_time, hue_global, frame_count
    now = time.time()
    dt = clamp(now - last_time, 0.0, 1/15) * 60.0  # normalize dt to ~60FPS scale
    last_time = now
    frame_count += 1
    hue_global += COLOR_CYCLE_SPEED * (dt * 0.016)

    # Paint background slowly (we repaint partly to emulate trailing)
    paint_background(hue_global * 0.5)

    # Add soft central attractors (moving with time)
    cx, cy = 0, 0
    attractors = []
    # moving orbiting attractor points to create flow
    for i in range(3):
        ang = frame_count * 0.7 * (0.9 + 0.2 * i) + i * 2.3
        r = 120 + 100 * i
        ax = cx + math.cos(ang * 0.02) * r * math.cos(ang * 0.01 + i)
        ay = cy + math.sin(ang * 0.02) * r * math.sin(ang * 0.011 + i*0.4)
        attractors.append((ax, ay, 9000 / (50 * (i+1))))

    # update and draw shapes
    draw_mandala(0, 0, min(WIDTH, HEIGHT) * 0.26, 6, hue_global * 0.8)

    # draw a few wavy ribbons using overlay_turtle for motion blur-like effect
    overlay_turtle.clear()
    overlay_turtle.width(2)
    for w in range(WAVE_ELEMENTS):
        pts = []
        tsi = frame_count * 0.03 + w * 0.6
        for i in range(22):
            t = i / 21.0
            x = -WIDTH/2 + t*WIDTH
            y = math.sin(t * 8.0 + tsi) * (40 + 20 * math.sin(tsi*0.6 + w))
            y += math.sin(t*5.0 + tsi*1.3 + w) * 30
            pts.append((x, y - 60 + 30 * math.cos(tsi*0.2 + w)))
        hue = (hue_global*0.08 + w*0.07) % 1.0
        overlay_turtle.goto(pts[0])
        overlay_turtle.pendown()
        overlay_turtle.color(rgb_to_hex(hsv_to_rgb(hue, 0.85, 0.9)))
        overlay_turtle.setheading(0)
        for (x, y) in pts:
            overlay_turtle.goto(x, y)
        overlay_turtle.penup()

    # Particle drawing (clear particle_turtle each frame)
    particle_turtle.clear()
    for p in particles:
        p.update(dt * 0.8, hue_global, attractors)
        p.draw(particle_turtle, hue_global)

    # Foreground sparkles
    shape_turtle.width(1)
    if frame_count % 3 == 0:
        for _ in range(6):
            x = random.uniform(-WIDTH*0.33, WIDTH*0.33)
            y = random.uniform(-HEIGHT*0.33, HEIGHT*0.33)
            hue = (hue_global*0.15 + random.random()*0.2) % 1.0
            shape_turtle.goto(x, y)
            shape_turtle.dot(random.choice([2,3,4]), rgb_to_hex(hsv_to_rgb(hue, 0.9, 1.0)))

    screen.update()
    # Schedule next frame
    screen.ontimer(animation_step, int(1000 / FPS))

# kick off animation
animation_step()

# keep window open until closed
turtle.done()