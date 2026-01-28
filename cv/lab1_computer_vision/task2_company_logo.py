import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon
import numpy as np

class CrossLogoGenerator:
    """
    Task 2: Company Logo - Cross Pattern with 4 Triangles
    CORRECTED: Triangles point INWARD to center (rotated 180°)
    """

    def __init__(self, company_name="TECH VISION"):
        self.company_name = company_name
        self.center = (5, 5)  # Center point
        self.triangle_height = 2.5  # Distance from center to triangle base
        self.triangle_base = 2.0    # Width of triangle base

    def create_logo_monochrome(self):
        """
        Monochrome version: Black outline, white fill, grayscale shading
        """
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_aspect('equal')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('on')
        ax.grid(False)

        # Draw border
        border = patches.Rectangle((0, 0), 10, 10,
                                   linewidth=2,
                                   edgecolor='black',
                                   facecolor='white')
        ax.add_patch(border)

        # Define 4 triangles pointing INWARD (top, right, bottom, left)
        triangles_data = [
            ('top', 0, ['#ffffff', '#e0e0e0', '#c0c0c0']),      # Top - white
            ('right', 90, ['#d0d0d0', '#b0b0b0', '#909090']),   # Right - light gray
            ('bottom', 180, ['#a0a0a0', '#808080', '#606060']), # Bottom - medium gray
            ('left', 270, ['#707070', '#505050', '#303030'])    # Left - dark gray
        ]

        for name, angle, shading_colors in triangles_data:
            triangle = self._create_triangle_inward(angle)

            # Draw triangle with shading
            tri_patch = Polygon(triangle,
                                closed=True,
                                facecolor=shading_colors[1],
                                edgecolor='black',
                                linewidth=2)
            ax.add_patch(tri_patch)

            # Add internal lines for shading effect
            self._add_shading_lines(ax, triangle, 'monochrome')

        # Draw center point
        ax.plot(self.center[0], self.center[1], 'ko', markersize=8, zorder=10)

        # Add connecting lines from center to outer vertices
        for angle in [0, 90, 180, 270]:
            triangle = self._create_triangle_inward(angle)
            # Connect center to the base vertices (outer edge)
            ax.plot([self.center[0], triangle[1][0]],
                    [self.center[1], triangle[1][1]],
                    'k-', linewidth=1, alpha=0.5)
            ax.plot([self.center[0], triangle[2][0]],
                    [self.center[1], triangle[2][1]],
                    'k-', linewidth=1, alpha=0.5)

        # Title
        ax.text(5, 0.5, self.company_name,
                fontsize=16, fontweight='bold',
                ha='center', va='center')

        ax.text(5, 9.5, 'MONOCHROME VERSION',
                fontsize=10, style='italic',
                ha='center', va='center', color='gray')

        ax.set_xticks([])
        ax.set_yticks([])

        plt.tight_layout()
        plt.savefig('task2_logo_monochrome.png', dpi=300, bbox_inches='tight')
        plt.show()

    def create_logo_color(self):
        """
        Color version: Using complementary color scheme
        Orange-Blue complementary colors with variations
        """
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_aspect('equal')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('on')
        ax.grid(False)

        # Draw border
        border = patches.Rectangle((0, 0), 10, 10,
                                   linewidth=3,
                                   edgecolor='#1a1a1a',
                                   facecolor='#f5f5f5')
        ax.add_patch(border)

        # Define 4 triangles with color scheme (pointing INWARD)
        # Using complementary colors: Blue-Orange
        triangles_data = [
            ('top', 0, '#FF6B35', '#FF8C42'),        # Orange (warm)
            ('right', 90, '#4ECDC4', '#45B7B8'),     # Cyan (cool)
            ('bottom', 180, '#FFB84D', '#FFA500'),   # Yellow-Orange (warm)
            ('left', 270, '#3D5A80', '#2E4057')      # Deep Blue (cool)
        ]

        for name, angle, fill_color, edge_color in triangles_data:
            triangle = self._create_triangle_inward(angle)

            # Draw triangle with color
            tri_patch = Polygon(triangle,
                                closed=True,
                                facecolor=fill_color,
                                edgecolor=edge_color,
                                linewidth=3,
                                alpha=0.85)
            ax.add_patch(tri_patch)

            # Add decorative shading lines
            self._add_shading_lines(ax, triangle, 'color', edge_color)

        # Draw center point with gradient effect
        center_circle = plt.Circle(self.center, 0.15,
                                   color='#1a1a1a',
                                   zorder=10)
        ax.add_patch(center_circle)

        # Outer glow
        glow_circle = plt.Circle(self.center, 0.25,
                                 color='#FFD700',
                                 alpha=0.3,
                                 zorder=9)
        ax.add_patch(glow_circle)

        # Add connecting lines with color
        line_colors = ['#FF6B35', '#4ECDC4', '#FFB84D', '#3D5A80']
        for idx, angle in enumerate([0, 90, 180, 270]):
            triangle = self._create_triangle_inward(angle)
            ax.plot([self.center[0], triangle[1][0]],
                    [self.center[1], triangle[1][1]],
                    color=line_colors[idx],
                    linewidth=1.5,
                    alpha=0.4,
                    linestyle='--')
            ax.plot([self.center[0], triangle[2][0]],
                    [self.center[1], triangle[2][1]],
                    color=line_colors[idx],
                    linewidth=1.5,
                    alpha=0.4,
                    linestyle='--')

        # Title with color
        ax.text(5, 0.5, self.company_name,
                fontsize=18, fontweight='bold',
                ha='center', va='center',
                color='#1a1a1a')

        ax.text(5, 9.5, 'COLOR VERSION',
                fontsize=11, style='italic',
                ha='center', va='center',
                color='#3D5A80')

        ax.set_xticks([])
        ax.set_yticks([])

        plt.tight_layout()
        plt.savefig('task2_logo_color.png', dpi=300, bbox_inches='tight')
        plt.show()

    def create_logo_combined(self):
        """
        Combined view: Both versions side by side
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

        # === LEFT: Monochrome ===
        self._draw_on_axis(ax1, monochrome=True)
        ax1.set_title('Monochrome Version\n(Grayscale Shading)',
                      fontsize=14, fontweight='bold', pad=15)

        # === RIGHT: Color ===
        self._draw_on_axis(ax2, monochrome=False)
        ax2.set_title('Color Version\n(Complementary: Orange-Blue)',
                      fontsize=14, fontweight='bold', pad=15)

        fig.suptitle('Task 2: Company Logo - Cross Pattern (Triangles Point Inward)',
                     fontsize=16, fontweight='bold', y=0.98)

        plt.tight_layout()
        plt.savefig('task2_logo_combined.png', dpi=300, bbox_inches='tight')
        plt.show()

    def _create_triangle_inward(self, angle_deg):
        """
        Create isosceles triangle pointing INWARD toward center

        Parameters:
        -----------
        angle_deg : float
            Rotation angle in degrees (0=from top, 90=from right, etc.)

        Returns:
        --------
        np.array : Triangle vertices [tip_at_center, base_left, base_right]
        """
        angle_rad = np.radians(angle_deg)
        cx, cy = self.center

        # Tip at center (pointing inward)
        tip_x = cx
        tip_y = cy

        # Base vertices at outer edge (perpendicular to direction)
        # Base center is at distance h from center
        base_center_x = cx + self.triangle_height * np.sin(angle_rad)
        base_center_y = cy + self.triangle_height * np.cos(angle_rad)

        # Perpendicular direction for base width
        perp_angle = angle_rad + np.pi / 2

        base_left_x = base_center_x + (self.triangle_base / 2) * np.sin(perp_angle)
        base_left_y = base_center_y + (self.triangle_base / 2) * np.cos(perp_angle)

        base_right_x = base_center_x - (self.triangle_base / 2) * np.sin(perp_angle)
        base_right_y = base_center_y - (self.triangle_base / 2) * np.cos(perp_angle)

        return np.array([
            [tip_x, tip_y],                     # Tip at center
            [base_left_x, base_left_y],         # Base left (outer)
            [base_right_x, base_right_y]        # Base right (outer)
        ])

    def _add_shading_lines(self, ax, triangle, mode='monochrome', color='black'):
        """
        Add internal shading lines to triangle
        """
        if mode == 'monochrome':
            # Add hatching lines for grayscale effect
            num_lines = 5
            tip = triangle[0]  # Center point
            base_left = triangle[1]
            base_right = triangle[2]

            for i in range(1, num_lines):
                t = i / num_lines
                p1 = tip + t * (base_left - tip)
                p2 = tip + t * (base_right - tip)
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]],
                        'k-', linewidth=0.5, alpha=0.3)
        else:
            # Add subtle gradient lines for color version
            num_lines = 3
            tip = triangle[0]
            base_left = triangle[1]
            base_right = triangle[2]

            for i in range(1, num_lines):
                t = i / num_lines
                p1 = tip + t * (base_left - tip)
                p2 = tip + t * (base_right - tip)
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]],
                        color=color, linewidth=0.8, alpha=0.2)

    def _draw_on_axis(self, ax, monochrome=True):
        """
        Helper to draw logo on specific axis
        """
        ax.set_aspect('equal')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('on')
        ax.grid(False)

        if monochrome:
            # Monochrome settings
            border_color = 'black'
            bg_color = 'white'
            triangles_data = [
                (0, '#ffffff', 'black'),
                (90, '#c0c0c0', 'black'),
                (180, '#808080', 'black'),
                (270, '#404040', 'black')
            ]
        else:
            # Color settings
            border_color = '#1a1a1a'
            bg_color = '#f5f5f5'
            triangles_data = [
                (0, '#FF6B35', '#FF8C42'),
                (90, '#4ECDC4', '#45B7B8'),
                (180, '#FFB84D', '#FFA500'),
                (270, '#3D5A80', '#2E4057')
            ]

        # Border
        border = patches.Rectangle((0, 0), 10, 10,
                                   linewidth=2,
                                   edgecolor=border_color,
                                   facecolor=bg_color)
        ax.add_patch(border)

        # Triangles
        for angle, fill_color, edge_color in triangles_data:
            triangle = self._create_triangle_inward(angle)
            tri_patch = Polygon(triangle,
                                closed=True,
                                facecolor=fill_color,
                                edgecolor=edge_color,
                                linewidth=2,
                                alpha=0.85 if not monochrome else 1.0)
            ax.add_patch(tri_patch)

            if monochrome:
                self._add_shading_lines(ax, triangle, 'monochrome')
            else:
                self._add_shading_lines(ax, triangle, 'color', edge_color)

        # Center point
        center_color = 'black' if monochrome else '#1a1a1a'
        ax.plot(self.center[0], self.center[1], 'o',
                color=center_color, markersize=8, zorder=10)

        # Text
        text_color = 'black' if monochrome else '#1a1a1a'
        ax.text(5, 0.5, self.company_name,
                fontsize=14, fontweight='bold',
                ha='center', va='center', color=text_color)

        ax.set_xticks([])
        ax.set_yticks([])


# ============= MAIN EXECUTION =============

def main():
    """
    Main function to generate all logo versions
    """
    print("="*70)
    print("TASK 2: COMPANY LOGO - CROSS PATTERN (TRIANGLES POINT INWARD)")
    print("="*70)
    print("\n📋 Technical Specifications:")
    print("   • Pattern: Cross formation with 4 isosceles triangles")
    print("   • Direction: All triangles point INWARD to center")
    print("   • Method 1: Using basic Polygon primitives")
    print("   • Method 2: Multi-sided shapes (triangles = 3-sided polygons)")
    print("   • Tip vertices: All meet at center point")
    print("   • Base vertices: At outer edges forming cross shape")
    print("\n🎨 Visual Requirements:")
    print("   ✓ Monochrome: Grayscale shading (white → black)")
    print("   ✓ Color: Complementary scheme (Orange-Blue)")
    print("   ✓ Edge outlining: Black/colored borders")
    print("   ✓ Shading method: Internal hatching lines")
    print("   ✓ Connection lines: From center to base vertices")
    print("="*70)

    # Create logo generator
    logo = CrossLogoGenerator(company_name="CV TECH")

    # Generate all versions
    print("\n[1/3] Generating monochrome version...")
    logo.create_logo_monochrome()
    print("      ✓ Saved: task2_logo_monochrome.png")

    print("\n[2/3] Generating color version...")
    logo.create_logo_color()
    print("      ✓ Saved: task2_logo_color.png")

    print("\n[3/3] Generating comparison view...")
    logo.create_logo_combined()
    print("      ✓ Saved: task2_logo_combined.png")

    print("\n" + "="*70)
    print("✅ ALL LOGO VERSIONS GENERATED SUCCESSFULLY!")
    print("="*70)

    # Technical documentation
    print("\n📐 Geometric Properties:")
    print(f"   • Center point: {logo.center}")
    print(f"   • Triangle height: {logo.triangle_height} units")
    print(f"   • Triangle base width: {logo.triangle_base} units")
    print(f"   • Number of triangles: 4")
    print(f"   • Direction: INWARD (tips meet at center)")
    print(f"   • Rotation angles: 0°, 90°, 180°, 270°")
    print("\n🔢 Mathematical Model:")
    print("   Triangle vertices (INWARD pointing):")
    print("   • Tip: (cx, cy) - at center for all triangles")
    print("   • Base center: (cx + h·sin(θ), cy + h·cos(θ))")
    print("   • Base edges: Base center ± (b/2)·(perpendicular)")
    print("   Where: h = height, b = base width, θ = rotation angle")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()