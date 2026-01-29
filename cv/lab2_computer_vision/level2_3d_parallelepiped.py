import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

matplotlib.use('Agg')

class Transform3D:
    @staticmethod
    def rotation_x(angle):
        c, s = np.cos(angle), np.sin(angle)
        return np.array([
            [1, 0, 0, 0],
            [0, c, -s, 0],
            [0, s, c, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def rotation_y(angle):
        c, s = np.cos(angle), np.sin(angle)
        return np.array([
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def rotation_z(angle):
        c, s = np.cos(angle), np.sin(angle)
        return np.array([
            [c, -s, 0, 0],
            [s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def apply_transform(points, matrix):
        return (matrix @ points.T).T

class Parallelepiped3D:
    def __init__(self, center=(0, 0, 0), width=2, height=3, depth=1.5):
        cx, cy, cz = center
        w, h, d = width/2, height/2, depth/2

        self.original_vertices = np.array([
            [cx-w, cy-h, cz-d, 1],
            [cx+w, cy-h, cz-d, 1],
            [cx+w, cy+h, cz-d, 1],
            [cx-w, cy+h, cz-d, 1],
            [cx-w, cy-h, cz+d, 1],
            [cx+w, cy-h, cz+d, 1],
            [cx+w, cy+h, cz+d, 1],
            [cx-w, cy+h, cz+d, 1],
        ])

        self.vertices = self.original_vertices.copy()

        self.faces = [
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [0, 1, 5, 4],
            [2, 3, 7, 6],
            [0, 3, 7, 4],
            [1, 2, 6, 5],
        ]

        self.face_colors = [
            '#FF6B6B',
            '#4ECDC4',
            '#45B7D1',
            '#FFA07A',
            '#98D8C8',
            '#F7DC6F',
        ]

    def reset(self):
        self.vertices = self.original_vertices.copy()

    def get_faces_vertices(self):
        faces_vertices = []
        for face in self.faces:
            face_verts = self.vertices[face][:, :3]
            faces_vertices.append(face_verts)
        return faces_vertices

def save_3d_animation():
    logger.info("\n" + "="*70)
    logger.info("🎬 СТВОРЕННЯ 3D АНІМАЦІЇ ПАРАЛЕЛЕПІПЕДА")
    logger.info("="*70)
    logger.info("⏳ Це займе ~40 секунд...\n")

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    parallelepiped = Parallelepiped3D(
        center=(0, 0, 0),
        width=3,
        height=4,
        depth=2
    )

    rotation_speed = 0.05
    total_frames = 200

    def update(frame):
        ax.clear()

        limit = 5
        ax.set_xlim([-limit, limit])
        ax.set_ylim([-limit, limit])
        ax.set_zlim([-limit, limit])
        ax.set_xlabel('X', fontsize=12, fontweight='bold')
        ax.set_ylabel('Y', fontsize=12, fontweight='bold')
        ax.set_zlabel('Z', fontsize=12, fontweight='bold')

        angle_deg = np.degrees(frame * rotation_speed)
        ax.set_title(
            f'3D Аксонометрична проекція: Обертання паралелепіпеда\n'
            f'Кадр {frame}/{total_frames} | Кут: {angle_deg:.1f}°',
            fontsize=13,
            fontweight='bold',
            pad=20
        )

        parallelepiped.reset()

        angle = frame * rotation_speed
        Rx = Transform3D.rotation_x(angle)
        Ry = Transform3D.rotation_y(angle * 0.7)
        Rz = Transform3D.rotation_z(angle * 0.5)

        R_combined = Rz @ Ry @ Rx

        parallelepiped.vertices = Transform3D.apply_transform(
            parallelepiped.vertices, R_combined
        )

        faces_vertices = parallelepiped.get_faces_vertices()

        poly_collection = Poly3DCollection(
            faces_vertices,
            facecolors=parallelepiped.face_colors,
            edgecolors='black',
            linewidths=2,
            alpha=0.85
        )

        ax.add_collection3d(poly_collection)

        ax.grid(True, alpha=0.3)
        ax.view_init(elev=20, azim=30)

        if frame % 20 == 0:
            logger.info(f"📹 Створено кадр {frame}/{total_frames} ({frame/total_frames*100:.0f}%)")

    anim = FuncAnimation(
        fig,
        update,
        frames=total_frames,
        interval=50,
        repeat=True
    )

    logger.info("\n💾 Збереження у 'parallelepiped_animation.gif'...")

    writer = PillowWriter(fps=20)
    anim.save('parallelepiped_animation.gif', writer=writer, dpi=100)

    logger.info("\n✅ ГОТОВО!")
    logger.info("📁 Файл збережено: parallelepiped_animation.gif")
    logger.info("🎬 Відкрийте GIF у будь-якому переглядачі зображень\n")

    plt.close()

if __name__ == "__main__":
    logger.info("\n" + "="*70)
    logger.info("🎯 РІВЕНЬ II: 3D ТРАНСФОРМАЦІЇ ПАРАЛЕЛЕПІПЕДА (GIF)")
    logger.info("="*70)

    save_3d_animation()