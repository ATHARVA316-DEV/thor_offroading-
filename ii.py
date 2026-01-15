import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Background color (RGB normalized)
bg_color = (3/255, 6/255, 21/255)

def draw_hazard(glow=False, filename="hazard.png"):
    fig, ax = plt.subplots(figsize=(4, 4))
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    # Glow effect (draw multiple layers)
    if glow:
        for lw, alpha in [(12, 0.15), (8, 0.25), (5, 0.4)]:
            glow_triangle = patches.Polygon(
                [[0.5, 0.95], [0.05, 0.1], [0.95, 0.1]],
                closed=True,
                edgecolor='yellow',
                facecolor='none',
                linewidth=lw,
                alpha=alpha
            )
            ax.add_patch(glow_triangle)

    # Main hazard triangle
    triangle = patches.Polygon(
        [[0.5, 0.95], [0.05, 0.1], [0.95, 0.1]],
        closed=True,
        edgecolor='yellow',
        facecolor='yellow',
        linewidth=3
    )
    ax.add_patch(triangle)

    # Exclamation mark
    ax.text(
        0.5, 0.38, '!',
        fontsize=90,
        ha='center',
        va='center',
        color='black',
        fontweight='bold'
    )

    # Formatting
    ax.set_aspect('equal')
    ax.axis('off')
    plt.xlim(0, 1)
    plt.ylim(0, 1)

    # Save image
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor=bg_color)
    plt.close()

# Generate images
draw_hazard(glow=False, filename="Hazard_OFF.png")
draw_hazard(glow=True, filename="Hazard_ON.png")
