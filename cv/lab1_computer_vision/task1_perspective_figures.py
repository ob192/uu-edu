import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_perspective_figures():
    """
    Task 1: Draw concentric circles and triangle in one window
    Variant 5,6: Circles with lines + Triangle with hatching
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_aspect('equal')
    ax.set_xlim(-2, 8)
    ax.set_ylim(-2, 6)
    ax.grid(True, alpha=0.3)
    ax.set_title('Task 1: Perspective Figures - Concentric Circles and Triangle',
                 fontsize=14, fontweight='bold')

    # === Figure 1: Concentric Circles with radial lines ===
    circle_center = (2, 3)
    radii = [0.5, 1.0, 1.5, 2.0]
    colors = ['blue', 'green', 'red', 'purple']
    linewidths = [1, 1.5, 2, 2.5]

    # Draw circles
    for radius, color, lw in zip(radii, colors, linewidths):
        circle = plt.Circle(circle_center, radius,
                            fill=False,
                            edgecolor=color,
                            linewidth=lw,
                            label=f'Circle r={radius}')
        ax.add_patch(circle)

    # Add radial lines connecting circles
    angles = np.linspace(0, 2*np.pi, 8, endpoint=False)
    for angle in angles:
        x_end = circle_center[0] + radii[-1] * np.cos(angle)
        y_end = circle_center[1] + radii[-1] * np.sin(angle)
        ax.plot([circle_center[0], x_end],
                [circle_center[1], y_end],
                'k--', linewidth=0.8, alpha=0.5)

    # === Figure 2: Triangle with hatching ===
    triangle_vertices = np.array([
        [6, 1],      # bottom left
        [7.5, 4.5],  # top
        [5, 4]       # top left
    ])

    # Create triangle with hatching
    triangle = patches.Polygon(triangle_vertices,
                               closed=True,
                               edgecolor='darkred',
                               facecolor='lightcoral',
                               linewidth=2.5,
                               hatch='///',
                               alpha=0.6,
                               label='Triangle with hatching')
    ax.add_patch(triangle)

    # Connect circles and triangle with line
    ax.plot([circle_center[0] + radii[-1], triangle_vertices[0, 0]],
            [circle_center[1], triangle_vertices[0, 1]],
            'orange', linewidth=2, linestyle=':',
            label='Connection line')

    ax.legend(loc='upper left', fontsize=9)
    ax.set_xlabel('X coordinate', fontsize=11)
    ax.set_ylabel('Y coordinate', fontsize=11)

    plt.tight_layout()
    plt.savefig('task1_perspective_figures.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    draw_perspective_figures()