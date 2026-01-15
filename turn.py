import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Background color (RGB 3,6,21)
BG = (3/255, 6/255, 21/255)

def draw_turn(direction="left", glow=False, filename="turn.png"):
    fig, ax = plt.subplots(figsize=(4, 2))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    # Arrow points
    if direction == "left":
        arrow = np.array([
            [0.15, 0.5],
            [0.45, 0.85],
            [0.45, 0.65],
            [0.85, 0.65],
            [0.85, 0.35],
            [0.45, 0.35],
            [0.45, 0.15],
        ])
    else:
        arrow = np.array([
            [0.85, 0.5],
            [0.55, 0.85],
            [0.55, 0.65],
            [0.15, 0.65],
            [0.15, 0.35],
            [0.55, 0.35],
            [0.55, 0.15],
        ])

    # Glow layers
    if glow:
        for lw, alpha in [(18, 0.12), (12, 0.25), (6, 0.45)]:
            ax.add_patch(
                patches.Polygon(
                    arrow,
                    closed=True,
                    edgecolor="#00FF66",
                    facecolor="none",
                    linewidth=lw,
                    alpha=alpha
                )
            )

    # Main arrow body (3D effect)
    arrow_body = patches.Polygon(
        arrow,
        closed=True,
        facecolor="#00FF66" if glow else "#1f6f4a",
        edgecolor="#00FF99",
        linewidth=2
    )
    ax.add_patch(arrow_body)

    # Highlight (fake 3D shine)
    highlight = patches.Polygon(
        arrow * [1, 0.92] + [0, 0.04],
        closed=True,
        facecolor="white",
        alpha=0.08
    )
    ax.add_patch(highlight)

    # THOR text
    ax.text(
        0.5, 0.5, "THOR",
        color="black" if glow else "#0a2a1e",
        fontsize=22,
        fontweight="bold",
        ha="center",
        va="center"
    )

    ax.set_aspect("equal")
    ax.axis("off")
    plt.xlim(0, 1)
    plt.ylim(0, 1)

    plt.savefig(filename, dpi=300, bbox_inches="tight", facecolor=BG)
    plt.close()

# Generate images
draw_turn("left",  glow=True,  filename="left_on.png")
draw_turn("left",  glow=False, filename="left_off.png")
draw_turn("right", glow=True,  filename="right_on.png")
draw_turn("right", glow=False, filename="right_off.png")
