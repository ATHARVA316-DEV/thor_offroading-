from PIL import Image, ImageDraw, ImageFont
import os
import math
import sys

# ================= CONFIG =================
WIDTH, HEIGHT = 200, 200
BASE_DIR = "dgus_assets"
SPEED_MAX = 80  # Define SPEED_MAX globally at the top

folders = [
    "speed", "rpm",
    "temp_motor", "temp_controller", "temp_battery",
    "soc", "battery_vi", "motor_vi",
    "charging", "indicators", "warnings"
]

for f in folders:
    os.makedirs(os.path.join(BASE_DIR, f), exist_ok=True)

# Ensure console encoding supports UTF-8 (prevents emoji print errors on Windows)
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

# ================= COLORS =================
BG = (0, 0, 0)
BLACK = (0, 0, 0)  # Added BLACK color definition
WHITE = (255, 255, 255)
GREEN = (0, 220, 120)
YELLOW = (255, 200, 0)
ORANGE = (255, 140, 0)
RED = (220, 50, 50)
GRAY = (120, 120, 120)
BLUE = (0, 150, 255)
CYAN = (0, 200, 200)

# ================= FONT =================
try:
    font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
    font_med = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
    font_small = ImageFont.truetype("DejaVuSans-Bold.ttf", 24)
except:
    font_big = font_med = font_small = ImageFont.load_default()

# ================= HELPER FUNCTIONS =================
def get_temp_color(temp, max_temp=80):
    """Dynamic color based on temperature"""
    ratio = temp / max_temp
    if ratio < 0.5:
        return GREEN
    elif ratio < 0.75:
        return YELLOW
    else:
        return RED

def draw_arc_gauge(draw, bounds, start_angle, end_angle, color, width=12):
    """Draw smooth arc"""
    draw.arc(bounds, start_angle, end_angle, fill=color, width=width)

# ================= SPEED GAUGE (0-80 km/h) =================
print("Generating speed gauge...")
for v in range(SPEED_MAX + 1):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(img)
    
    # Background circle
    d.ellipse((10, 10, 190, 190), outline=GRAY, width=3)
    
    # Dynamic color based on speed
    if v < 40:
        color = GREEN
    elif v < 60:
        color = YELLOW
    else:
        color = RED
    
    # Arc progress
    angle = int(270 * v / SPEED_MAX)
    draw_arc_gauge(d, (20, 20, 180, 180), 135, 135 + angle, color)
    
    # Speed markers (every 20 km/h)
    for marker in [0, 20, 40, 60, SPEED_MAX]:
        marker_angle = 135 + (270 * marker / SPEED_MAX)
        rad = math.radians(marker_angle)
        x1 = 100 + 75 * math.cos(rad)
        y1 = 100 + 75 * math.sin(rad)
        x2 = 100 + 85 * math.cos(rad)
        y2 = 100 + 85 * math.sin(rad)
        d.line([(x1, y1), (x2, y2)], fill=WHITE, width=2)
    
    # Center value
    text = str(v)
    bbox = d.textbbox((0, 0), text, font=font_big)
    text_w = bbox[2] - bbox[0]
    d.text((100 - text_w//2, 65), text, fill=WHITE, font=font_big)
    
    # Unit label
    unit_bbox = d.textbbox((0, 0), "km/h", font=font_small)
    unit_w = unit_bbox[2] - unit_bbox[0]
    d.text((100 - unit_w//2, 125), "km/h", fill=GRAY, font=font_small)
    
    img.save(f"{BASE_DIR}/speed/{v:03}.png")

# ================= RPM GAUGE (0-8000, 17 frames) =================
print("Generating RPM gauge...")
for i in range(17):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(img)
    rpm_val = i * 500
    
    # Background circle
    d.ellipse((10, 10, 190, 190), outline=GRAY, width=3)
    
    # Color based on RPM range
    if rpm_val < 4000:
        color = GREEN
    elif rpm_val < 6000:
        color = YELLOW
    else:
        color = RED
    
    # Arc progress
    angle = int(270 * i / 16)
    draw_arc_gauge(d, (20, 20, 180, 180), 135, 135 + angle, color)
    
    # RPM markers
    for marker in range(0, 9):
        marker_angle = 135 + (270 * marker / 16)
        rad = math.radians(marker_angle)
        x1 = 100 + 75 * math.cos(rad)
        y1 = 100 + 75 * math.sin(rad)
        x2 = 100 + 85 * math.cos(rad)
        y2 = 100 + 85 * math.sin(rad)
        d.line([(x1, y1), (x2, y2)], fill=WHITE, width=2)
    
    # RPM value
    text = str(rpm_val)
    bbox = d.textbbox((0, 0), text, font=font_big)
    text_w = bbox[2] - bbox[0]
    d.text((100 - text_w//2, 65), text, fill=WHITE, font=font_big)
    
    # Unit label
    d.text((75, 125), "RPM", fill=GRAY, font=font_small)
    
    img.save(f"{BASE_DIR}/rpm/{i:02}.png")

# ================= TEMPERATURE BARS =================
print("Generating temperature bars...")
def temp_bar_enhanced(folder, label):
    for t in range(101):
        img = Image.new("RGB", (80, 220), BG)
        d = ImageDraw.Draw(img)
        
        # Outer frame
        d.rectangle((15, 15, 65, 205), outline=WHITE, width=3)
        
        # Temperature fill
        base_y = 201
        fill_h = int((t/100) * 175)
        color = get_temp_color(t, 100)
        top_y = base_y - fill_h
        if fill_h > 0:
            d.rectangle((19, top_y, 61, base_y), fill=color)

        # Tick marks every 25%
        for tick in [0.25, 0.5, 0.75]:
            y = base_y - int(tick * 175)
            d.line([(15, y), (22, y)], fill=GRAY, width=2)
            d.line([(58, y), (65, y)], fill=GRAY, width=2)
        
        # Temperature value at bottom
        temp_text = f"{t}"
        bbox = d.textbbox((0, 0), temp_text, font=font_small)
        text_w = bbox[2] - bbox[0]
        d.text((40 - text_w//2, 208), temp_text, fill=WHITE, font=font_small)
        
        img.save(f"{BASE_DIR}/{folder}/{t:03}.png")

temp_bar_enhanced("temp_motor", "Motor")
temp_bar_enhanced("temp_controller", "Ctrl")
temp_bar_enhanced("temp_battery", "Batt")

# ================= STATE OF CHARGE =================
print("Generating SOC bar...")
for s in range(101):
    img = Image.new("RGB", (240, 80), BG)
    d = ImageDraw.Draw(img)
    
    # Battery outline
    d.rectangle((10, 20, 220, 60), outline=WHITE, width=4)
    d.rectangle((220, 30, 230, 50), fill=WHITE)
    
    # Fill color based on charge level
    if s > 60:
        fill_color = GREEN
    elif s > 20:
        fill_color = YELLOW
    else:
        fill_color = RED
    
    # Fill bar
    fill_width = int((s/100) * 200)
    if fill_width > 0:
        d.rectangle((15, 25, 15 + fill_width, 55), fill=fill_color)
    
    # Percentage text
    text = f"{s}%"
    bbox = d.textbbox((0, 0), text, font=font_med)
    text_w = bbox[2] - bbox[0]
    text_color = BLACK if s > 30 else WHITE
    d.text((120 - text_w//2, 28), text, fill=text_color, font=font_med)
    
    img.save(f"{BASE_DIR}/soc/{s:03}.png")

# ================= VOLTAGE/CURRENT BARS =================
print("Generating V/I bars...")
def vi_bar_enhanced(folder, label, max_val, unit):
    for v in range(max_val + 1):
        img = Image.new("RGB", (240, 70), BG)
        d = ImageDraw.Draw(img)
        
        # Bar background
        d.rectangle((10, 30, 230, 60), outline=WHITE, width=3)
        
        # Fill
        fill_width = int((v/max_val) * 210)
        if fill_width > 0:
            d.rectangle((13, 33, 13 + fill_width, 57), fill=BLUE)
        
        # Value text
        text = f"{v}{unit}"
        d.text((15, 5), text, fill=WHITE, font=font_small)
        
        img.save(f"{BASE_DIR}/{folder}/{v:03}.png")

vi_bar_enhanced("battery_vi", "Battery", 100, "V")
vi_bar_enhanced("motor_vi", "Motor", 150, "A")

# ================= CHARGING ICONS =================
print("Generating charging icons...")
def charging_icon_animated(charging=True):
    frames = []
    for frame in range(4):
        img = Image.new("RGB", (100, 100), BG)
        d = ImageDraw.Draw(img)
        
        if charging:
            bolt = [(50, 10), (30, 50), (45, 50), (35, 90), (70, 45), (55, 45)]
            d.polygon(bolt, fill=GREEN if frame % 2 == 0 else (0, 180, 100))
            d.ellipse((10 + frame*2, 10 + frame*2, 90 - frame*2, 90 - frame*2), 
                     outline=GREEN, width=2)
        else:
            bolt = [(50, 10), (30, 50), (45, 50), (35, 90), (70, 45), (55, 45)]
            d.polygon(bolt, fill=RED)
        
        frames.append(img)
    return frames

charging_frames = charging_icon_animated(True)
for i, frame in enumerate(charging_frames):
    frame.save(f"{BASE_DIR}/charging/charging_{i}.png")

discharging_frames = charging_icon_animated(False)
discharging_frames[0].save(f"{BASE_DIR}/charging/discharging.png")

# ================= TURN INDICATORS =================
print("Generating turn indicators...")
def indicator_animated(direction, frames=3):
    images = []
    for frame in range(frames):
        img = Image.new("RGB", (140, 100), BG)
        d = ImageDraw.Draw(img)
        
        brightness = int(255 * (0.3 + 0.7 * (frame / (frames-1))))
        col = (0, brightness, int(brightness * 0.6))
        
        if direction == "left":
            pts = [(100, 15), (30, 50), (100, 85), (100, 65), (130, 65), (130, 35), (100, 35)]
        else:
            pts = [(40, 15), (110, 50), (40, 85), (40, 65), (10, 65), (10, 35), (40, 35)]
        
        d.polygon(pts, fill=col, outline=WHITE, width=2)
        images.append(img)
    return images

left_frames = indicator_animated("left")
for i, frame in enumerate(left_frames):
    frame.save(f"{BASE_DIR}/indicators/left_{i}.png")

right_frames = indicator_animated("right")
for i, frame in enumerate(right_frames):
    frame.save(f"{BASE_DIR}/indicators/right_{i}.png")

# Off states
left_off = Image.new("RGB", (140, 100), BG)
d = ImageDraw.Draw(left_off)
pts = [(100, 15), (30, 50), (100, 85), (100, 65), (130, 65), (130, 35), (100, 35)]
d.polygon(pts, fill=GRAY, outline=WHITE, width=2)
left_off.save(f"{BASE_DIR}/indicators/left_off.png")

right_off = Image.new("RGB", (140, 100), BG)
d = ImageDraw.Draw(right_off)
pts = [(40, 15), (110, 50), (40, 85), (40, 65), (10, 65), (10, 35), (40, 35)]
d.polygon(pts, fill=GRAY, outline=WHITE, width=2)
right_off.save(f"{BASE_DIR}/indicators/right_off.png")

# ================= WARNING ICONS =================
print("Generating warning icons...")
warnings = {
    "battery_low": (RED, "!"),
    "overheat": (RED, "H"),
    "motor_fault": (ORANGE, "M"),
    "brake": (RED, "B"),
    "abs": (YELLOW, "ABS")
}

for name, (color, symbol) in warnings.items():
    img = Image.new("RGBA", (100, 100), BG + (255,))
    d = ImageDraw.Draw(img)

    if name in ["battery_low", "overheat"]:
        pts = [(50, 10), (90, 90), (10, 90)]
        fill_col = (color[0], color[1], color[2], 120)
        d.polygon(pts, fill=fill_col)
        d.line(pts + [pts[0]], fill=color, width=4)
    else:
        fill_col = (color[0], color[1], color[2], 120)
        d.ellipse((10, 10, 90, 90), fill=fill_col, outline=color, width=4)

    bbox = d.textbbox((0, 0), symbol, font=font_big)
    text_w = bbox[2] - bbox[0]
    d.text((50 - text_w//2, 35), symbol, fill=color, font=font_big)
    img.save(f"{BASE_DIR}/warnings/{name}.png")

print(f"\nALL DGUS ASSETS GENERATED SUCCESSFULLY")
print(f"Output directory: {BASE_DIR}/")
print(f"Total folders: {len(folders)}")
print("\nGenerated assets:")
print(f"  - Speed: {SPEED_MAX + 1} frames (0-{SPEED_MAX} km/h)")
print(f"  - RPM: 17 frames (0-8000 RPM)")
print(f"  - Temperatures: 101 frames each (0-100 C)")
print(f"  - SOC: 101 frames (0-100%)")
print(f"  - Battery V/I: 101 frames")
print(f"  - Motor V/I: 151 frames")
print(f"  - Charging: 4 animated frames + 1 static")
print(f"  - Indicators: 3 animated frames each + off states")
print(f"  - Warnings: {len(warnings)} icons")