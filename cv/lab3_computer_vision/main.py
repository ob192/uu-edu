import numpy as np
import cv2
import math
import imageio

class PyramidResearcher:
    def __init__(self, size=400):
        self.size = size
        self.center = size // 2
        # Setup 3D Geometry: Apex + Triangular Base
        self.verts = [[0, 1.2, 0], [-1, -0.8, 1], [1, -0.8, 1], [0, -0.8, -1]]
        self.faces = [(0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 2, 3)]

    def rotate_y(self, point, angle):
        """Applies a rotation matrix around the Y-axis."""
        rad = math.radians(angle)
        x, y, z = point
        nx = x * math.cos(rad) + z * math.sin(rad)
        nz = -x * math.sin(rad) + z * math.cos(rad)
        return [nx, y, nz]

    def project(self, p):
        """Axonometric (Isometric) Projection: 3D to 2D screen coordinates."""
        x, y, z = p
        u = (x - z) * math.cos(math.radians(30))
        v = y + (x + z) * math.sin(math.radians(30))
        # Scale by 100 and offset to center
        return int(u * 100 + self.center), int(-v * 100 + self.center)

    def draw_l1_line(self, img, p1, p2, c1, c2):
        """
        Level I: Bresenham-based line drawing.
        Implements color change from raster to raster.
        """
        x1, y1 = p1; x2, y2 = p2
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        steps = max(dx, dy)
        for i in range(steps + 1):
            t = i / steps if steps > 0 else 1
            curr_x = int(x1 + (x2 - x1) * t)
            curr_y = int(y1 + (y2 - y1) * t)
            # Linear color interpolation
            curr_col = [int(c1[j] * (1 - t) + c2[j] * t) for j in range(3)]
            if 0 <= curr_x < self.size and 0 <= curr_y < self.size:
                img[curr_y, curr_x] = curr_col

    def draw_l2_fill(self, img, pts, base_color):
        """
        Level II: Face filling using Barycentric coordinates.
        Ensures color variation inside the triangle on a per-raster level.
        """
        pts = np.array(pts)
        # Bounding box for optimization
        x_min, y_min = np.max([[0, 0], pts.min(axis=0).astype(int)], axis=0)
        x_max, y_max = np.min([[self.size-1, self.size-1], pts.max(axis=0).astype(int)], axis=0)

        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                # Calculate Barycentric weights (w0, w1, w2)
                d = (pts[1][1]-pts[2][1])*(pts[0][0]-pts[2][0]) + (pts[2][0]-pts[1][0])*(pts[0][1]-pts[2][1])
                w0 = ((pts[1][1]-pts[2][1])*(x-pts[2][0]) + (pts[2][0]-pts[1][0])*(y-pts[2][1])) / (d + 1e-6)
                w1 = ((pts[2][1]-pts[0][1])*(x-pts[2][0]) + (pts[0][0]-pts[2][0])*(y-pts[2][1])) / (d + 1e-6)
                w2 = 1 - w0 - w1

                if w0 >= 0 and w1 >= 0 and w2 >= 0:
                    # Color shifts based on spatial position (raster-to-raster)
                    img[y, x] = [int(base_color[i] * (w0*0.3 + 0.7)) for i in range(3)]

    def apply_l3_filter(self, img, mode='sepia'):
        """
        Level III: Matrix-level spatial gradient processing.
        Applies a color correction filter blended by a radial mask.
        """
        h, w = img.shape[:2]
        y, x = np.ogrid[:h, :w]
        # Radial gradient mask (distance from center)
        dist = np.sqrt((x - w/2)**2 + (y - h/2)**2)
        mask = dist / dist.max()

        # Float normalization for matrix multiplication
        res = img.astype(np.float32) / 255.0
        if mode == 'sepia':
            # Industry standard sepia matrix
            sepia_matrix = np.array([
                [0.272, 0.534, 0.131],
                [0.349, 0.686, 0.168],
                [0.393, 0.769, 0.189]
            ])
            sepia_img = res @ sepia_matrix.T
            # Blend original render with sepia based on radial gradient
            res = res * (1 - mask[:,:,None]) + sepia_img * mask[:,:,None]

        return (np.clip(res * 255, 0, 255)).astype(np.uint8)

def run_experiment():
    researcher = PyramidResearcher(400)
    gif_frames = []

    print("Starting Graphics Pipeline. Press 'q' to stop.")

    # 360-degree rotation loop
    for angle in range(0, 360, 8):
        # Create blank canvases for each Level
        l1_canvas = np.zeros((400, 400, 3), dtype=np.uint8)
        l2_canvas = np.zeros((400, 400, 3), dtype=np.uint8)

        # Dynamics: Opacity/Brightness pulse (Figure appears and fades)
        pulse = (math.sin(math.radians(angle)) + 1) / 2

        # 3D Math: Rotation and Projection
        rotated = [researcher.rotate_y(v, angle) for v in researcher.verts]
        proj = [researcher.project(v) for v in rotated]

        # Render Level 2 (Faces) and Level 1 (Edges)
        for i, f in enumerate(researcher.faces):
            p_tri = [proj[f[0]], proj[f[1]], proj[f[2]]]

            # Level II: Filling with per-raster gradient
            researcher.draw_l2_fill(l2_canvas, p_tri, [int(200*pulse), 100, 50 + i*50])

            # Level I: Edges with per-raster gradient
            for j in range(3):
                p_start, p_end = proj[f[j]], proj[f[(j+1)%3]]
                researcher.draw_l1_line(l1_canvas, p_start, p_end, (0, 255, 100), (255, 100, pulse*255))
                # Add white wireframe on top of filled model for clarity
                researcher.draw_l1_line(l2_canvas, p_start, p_end, (255, 255, 255), (150, 150, 150))

        # Level III: Global matrix correction
        l3_canvas = researcher.apply_l3_filter(l2_canvas, mode='sepia')

        # Assemble Triptych Visualization
        combined = np.hstack((l1_canvas, l2_canvas, l3_canvas))

        # Annotations
        labels = ["L1: RASTER EDGES", "L2: RASTER FILL", "L3: MATRIX FILTER"]
        for idx, label in enumerate(labels):
            cv2.putText(combined, label, (10 + idx*400, 385),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Show Live Window
        cv2.imshow("CV LABS Research: Levels I, II, III", combined)

        # Save a frame for the static report
        if angle == 120:
            cv2.imwrite('pyramid_research_static.png', combined)

        gif_frames.append(cv2.cvtColor(combined, cv2.COLOR_BGR2RGB))

        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

    # Export Results
    print("Saving dynamic GIF...")
    imageio.mimsave('pyramid_research_dynamic.gif', gif_frames, fps=15)
    print("Success. Files 'pyramid_research_dynamic.gif' and 'pyramid_research_static.png' generated.")

if __name__ == "__main__":
    run_experiment()