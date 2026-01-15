"""
DGUS Dashboard Asset Generator
Generates UI assets for DGUS display systems with improved structure and error handling.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import NamedTuple

from PIL import Image, ImageDraw, ImageFont

# Fix Unicode output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    """Central configuration for asset generation."""
    
    # Canvas
    CANVAS_WIDTH = 1024
    CANVAS_HEIGHT = 600
    
    # Paths
    OUTPUT_DIR = Path("dgus_assets")
    FONT_NAME = "DejaVuSans-Bold.ttf"
    
    # Font sizes
    FONT_SIZE_BIG = 36
    FONT_SIZE_MED = 26
    
    # Folders
    FOLDERS = [
        "background", "labels", "indicators",
        "warning", "bars", "charging"
    ]


# ============================================================================
# COLOR DEFINITIONS
# ============================================================================

class Color(NamedTuple):
    """RGB or RGBA color tuple."""
    r: int
    g: int
    b: int
    a: int = 255
    
    def as_rgb(self) -> tuple[int, int, int]:
        """Return as RGB tuple."""
        return (self.r, self.g, self.b)
    
    def as_rgba(self) -> tuple[int, int, int, int]:
        """Return as RGBA tuple."""
        return (self.r, self.g, self.b, self.a)


class Palette:
    """Color palette for dashboard assets."""
    
    BG = Color(235, 237, 240)
    DARK = Color(40, 60, 80)
    WHITE = Color(255, 255, 255)
    GREEN = Color(0, 220, 120)
    YELLOW = Color(255, 200, 0)
    RED = Color(220, 50, 50)
    BLUE = Color(0, 150, 255)
    GRAY = Color(150, 150, 150)
    DARK_BG = Color(60, 90, 120)
    TRANSPARENT = Color(0, 0, 0, 0)


# ============================================================================
# ENUMS
# ============================================================================

class Direction(Enum):
    """Arrow direction."""
    LEFT = "left"
    RIGHT = "right"


class State(Enum):
    """Component state."""
    ON = True
    OFF = False


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class LabelSpec:
    """Label specification."""
    text: str
    filename: str


@dataclass
class ArrowSpec:
    """Arrow indicator specification."""
    name: str
    direction: Direction
    state: State


# ============================================================================
# ASSET GENERATOR CLASS
# ============================================================================

class AssetGenerator:
    """Generates all dashboard assets."""
    
    def __init__(self, config: Config = Config()):
        """Initialize generator with configuration."""
        self.config = config
        self.font_big: ImageFont.FreeTypeFont | ImageFont.ImageFont
        self.font_med: ImageFont.FreeTypeFont | ImageFont.ImageFont
        
        self._setup()
    
    def _setup(self) -> None:
        """Setup output directories and load fonts."""
        self._create_directories()
        self._load_fonts()
    
    def _create_directories(self) -> None:
        """Create output directory structure."""
        for folder in self.config.FOLDERS:
            (self.config.OUTPUT_DIR / folder).mkdir(parents=True, exist_ok=True)
        print(f"[OK] Created {len(self.config.FOLDERS)} output directories")
    
    def _load_fonts(self) -> None:
        """Load TrueType fonts with fallback."""
        try:
            self.font_big = ImageFont.truetype(
                self.config.FONT_NAME, 
                self.config.FONT_SIZE_BIG
            )
            self.font_med = ImageFont.truetype(
                self.config.FONT_NAME, 
                self.config.FONT_SIZE_MED
            )
            print(f"[OK] Loaded font: {self.config.FONT_NAME}")
        except (OSError, IOError):
            print(f"[WARNING] Font '{self.config.FONT_NAME}' not found, using default")
            self.font_big = self.font_med = ImageFont.load_default()
    
    # ========================================================================
    # BACKGROUND
    # ========================================================================
    
    def create_background(self) -> None:
        """Generate main dashboard background."""
        img = Image.new(
            "RGB", 
            (self.config.CANVAS_WIDTH, self.config.CANVAS_HEIGHT), 
            Palette.BG.as_rgb()
        )
        draw = ImageDraw.Draw(img)
        
        # Panel containers
        panels = [
            ((40, 100, 300, 380), 20, Palette.DARK, 3),
            ((360, 80, 660, 380), 150, Palette.BLUE, 5),
            ((740, 100, 980, 260), 20, Palette.DARK, 3),
        ]
        
        for coords, radius, color, width in panels:
            draw.rounded_rectangle(
                coords, 
                radius, 
                outline=color.as_rgb(), 
                width=width
            )
        
        # Bottom panels with fill
        bottom_panels = [
            ((60, 430, 440, 560), 20, Palette.DARK_BG),
            ((580, 430, 960, 560), 20, Palette.DARK_BG),
        ]
        
        for coords, radius, fill_color in bottom_panels:
            draw.rounded_rectangle(
                coords, 
                radius, 
                fill=fill_color.as_rgb()
            )
        
        output_path = self.config.OUTPUT_DIR / "background" / "dashboard_bg.png"
        img.save(output_path)
        print("✓ Background generated")
    
    # ========================================================================
    # LABELS
    # ========================================================================
    
    def create_labels(self) -> None:
        """Generate all text labels."""
        labels = [
            LabelSpec("SPEED (km/h)", "speed.png"),
            LabelSpec("RPM", "rpm.png"),
            LabelSpec("TEMP - MOTOR", "temp_motor.png"),
            LabelSpec("TEMP - CONTROLLER", "temp_controller.png"),
            LabelSpec("TEMP - BATTERY", "temp_battery.png"),
            LabelSpec("BATTERY (V / I)", "battery.png"),
            LabelSpec("MOTOR (V / I)", "motor.png"),
        ]
        
        for spec in labels:
            self._create_label(spec)
        
        print(f"✓ Generated {len(labels)} labels")
    
    def _create_label(self, spec: LabelSpec) -> None:
        """Create individual label image."""
        img = Image.new("RGBA", (260, 50), Palette.TRANSPARENT.as_rgba())
        draw = ImageDraw.Draw(img)
        draw.text((10, 5), spec.text, fill=Palette.DARK.as_rgb(), font=self.font_med)
        
        output_path = self.config.OUTPUT_DIR / "labels" / spec.filename
        img.save(output_path)
    
    # ========================================================================
    # INDICATORS
    # ========================================================================
    
    def create_indicators(self) -> None:
        """Generate arrow indicators."""
        arrows = [
            ArrowSpec("left_off", Direction.LEFT, State.OFF),
            ArrowSpec("left_on", Direction.LEFT, State.ON),
            ArrowSpec("right_off", Direction.RIGHT, State.OFF),
            ArrowSpec("right_on", Direction.RIGHT, State.ON),
        ]
        
        for spec in arrows:
            img = self._create_arrow(spec.direction, spec.state)
            output_path = self.config.OUTPUT_DIR / "indicators" / f"{spec.name}.png"
            img.save(output_path)
        
        print(f"✓ Generated {len(arrows)} arrow indicators")
    
    def _create_arrow(self, direction: Direction, state: State) -> Image.Image:
        """Create arrow indicator icon."""
        img = Image.new("RGBA", (120, 80), Palette.TRANSPARENT.as_rgba())
        draw = ImageDraw.Draw(img)
        
        color = Palette.GREEN if state == State.ON else Palette.GRAY
        
        points = (
            [(80, 10), (20, 40), (80, 70), (80, 55), (110, 55), (110, 25), (80, 25)]
            if direction == Direction.LEFT else
            [(40, 10), (100, 40), (40, 70), (40, 55), (10, 55), (10, 25), (40, 25)]
        )
        
        draw.polygon(points, fill=color.as_rgb())
        return img
    
    # ========================================================================
    # WARNINGS
    # ========================================================================
    
    def create_warnings(self) -> None:
        """Generate warning icons."""
        for state in [State.OFF, State.ON]:
            img = self._create_warning(state)
            filename = f"warning_{'on' if state == State.ON else 'off'}.png"
            output_path = self.config.OUTPUT_DIR / "warning" / filename
            img.save(output_path)
        
        print("✓ Generated warning icons")
    
    def _create_warning(self, state: State) -> Image.Image:
        """Create warning triangle icon."""
        img = Image.new("RGBA", (100, 90), Palette.TRANSPARENT.as_rgba())
        draw = ImageDraw.Draw(img)
        
        color = Palette.RED if state == State.ON else Palette.GRAY
        points = [(50, 5), (5, 85), (95, 85)]
        draw.polygon(points, fill=color.as_rgb())
        
        return img
    
    # ========================================================================
    # BARS
    # ========================================================================
    
    def create_bars(self) -> None:
        """Generate all bar indicators."""
        self._create_temp_bars()
        self._create_soc_bars()
        print("✓ Generated bar indicators")
    
    def _create_temp_bars(self) -> None:
        """Create temperature bar indicators."""
        for filled in [False, True]:
            img = Image.new("RGBA", (50, 200), Palette.TRANSPARENT.as_rgba())
            draw = ImageDraw.Draw(img)
            draw.rectangle((0, 0, 50, 200), outline=Palette.DARK.as_rgb(), width=3)
            
            if filled:
                draw.rectangle((3, 90, 47, 197), fill=Palette.YELLOW.as_rgb())
            
            filename = f"temp_bar_{'fill' if filled else 'empty'}.png"
            output_path = self.config.OUTPUT_DIR / "bars" / filename
            img.save(output_path)
    
    def _create_soc_bars(self) -> None:
        """Create state-of-charge bar indicators."""
        for filled in [False, True]:
            img = Image.new("RGBA", (200, 40), Palette.TRANSPARENT.as_rgba())
            draw = ImageDraw.Draw(img)
            draw.rectangle((0, 0, 200, 40), outline=Palette.DARK.as_rgb(), width=3)
            
            if filled:
                draw.rectangle((3, 3, 160, 37), fill=Palette.GREEN.as_rgb())
            
            filename = f"soc_bar_{'fill' if filled else 'empty'}.png"
            output_path = self.config.OUTPUT_DIR / "bars" / filename
            img.save(output_path)
    
    # ========================================================================
    # CHARGING
    # ========================================================================
    
    def create_charging_icons(self) -> None:
        """Generate charging/discharging icons."""
        for is_charging in [True, False]:
            img = self._create_charging_icon(is_charging)
            filename = f"{'charging' if is_charging else 'discharging'}.png"
            output_path = self.config.OUTPUT_DIR / "charging" / filename
            img.save(output_path)
        
        print("✓ Generated charging icons")
    
    def _create_charging_icon(self, charging: bool) -> Image.Image:
        """Create charging bolt icon."""
        img = Image.new("RGBA", (80, 80), Palette.TRANSPARENT.as_rgba())
        draw = ImageDraw.Draw(img)
        
        color = Palette.GREEN if charging else Palette.RED
        points = [(40, 5), (20, 45), (35, 45), (25, 75), (60, 30), (45, 30)]
        draw.polygon(points, fill=color.as_rgb())
        
        return img
    
    # ========================================================================
    # MAIN GENERATION
    # ========================================================================
    
    def generate_all(self) -> bool:
        """Generate all assets. Returns True on success."""
        try:
            self.create_background()
            self.create_labels()
            self.create_indicators()
            self.create_warnings()
            self.create_bars()
            self.create_charging_icons()
            
            self._print_summary()
            return True
            
        except Exception as e:
            print(f"\n❌ Error during generation: {e}", file=sys.stderr)
            return False
    
    def _print_summary(self) -> None:
        """Print generation summary."""
        print("\n" + "=" * 70)
        print("✅ ALL DGUS DASHBOARD ASSETS GENERATED SUCCESSFULLY!")
        print("=" * 70)
        print(f"📁 Output: {self.config.OUTPUT_DIR.absolute()}")
        print(f"📦 Folders: {len(self.config.FOLDERS)}")
        print("🎨 Assets generated:")
        print("   • Background (1)")
        print("   • Labels (7)")
        print("   • Indicators (4)")
        print("   • Warning icons (2)")
        print("   • Temperature bars (2)")
        print("   • SOC bars (2)")
        print("   • Charging icons (2)")
        print("=" * 70)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main() -> int:
    """Main entry point."""
    try:
        generator = AssetGenerator()
        success = generator.generate_all()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n⚠ Generation cancelled by user")
        return 130
    except Exception as e:
        print(f"\n❌ Fatal error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())