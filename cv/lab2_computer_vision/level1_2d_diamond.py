import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

matplotlib.use('Agg')

class Transform2D:
    @staticmethod
    def translation_matrix(dx, dy):
        return np.array([[1, 0, dx], [0, 1, dy], [0, 0, 1]])

    @staticmethod
    def rotation_matrix(angle):
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        return np.array([[cos_a, -sin_a, 0], [sin_a, cos_a, 0], [0, 0, 1]])

    @staticmethod
    def scaling_matrix(sx, sy):
        return np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])

    @staticmethod
    def apply_transform(points, matrix):
        return (matrix @ points.T).T

class Diamond2D:
    def __init__(self, center=(0, 0), width=2, height=3):
        cx, cy = center
        self.original_points = np.array([
            [cx, cy + height/2, 1],
            [cx + width/2, cy, 1],
            [cx, cy - height/2, 1],
            [cx - width/2, cy, 1],
        ])
        self.points = self.original_points.copy()

    def reset(self):
        self.points = self.original_points.copy()

    def get_center(self):
        center_2d = np.mean(self.points[:, :2], axis=0)
        return np.array([center_2d[0], center_2d[1], 1])

def save_animation():
    logger.info("\n🎬 Створення GIF анімації для IntelliJ IDEA...")
    logger.info("⏳ Це займе ~30 секунд...\n")

    fig, ax = plt.subplots(figsize=(10, 10))
    diamond = Diamond2D(center=(0, 0), width=3, height=4)

    translation_speed = 0.15
    rotation_speed = 0.08

    def update(frame):
        ax.clear()
        ax.set_xlim(-15, 15)
        ax.set_ylim(-15, 15)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.set_title(f'2D Трансформації - Кадр {frame}/200', fontsize=13, fontweight='bold')

        diamond.reset()

        angle_translation = frame * translation_speed
        radius = 8
        tx = radius * np.cos(angle_translation)
        ty = radius * np.sin(angle_translation)
        T = Transform2D.translation_matrix(tx, ty)
        diamond.points = Transform2D.apply_transform(diamond.points, T)

        current_center = diamond.get_center()
        angle_rotation = frame * rotation_speed
        T_to_origin = Transform2D.translation_matrix(-current_center[0], -current_center[1])
        R = Transform2D.rotation_matrix(angle_rotation)
        T_back = Transform2D.translation_matrix(current_center[0], current_center[1])
        transform = T_back @ R @ T_to_origin
        diamond.points = Transform2D.apply_transform(diamond.points, transform)

        scale_factor = 1 + 0.3 * np.sin(frame * 0.1)
        current_center = diamond.get_center()
        T_to_origin = Transform2D.translation_matrix(-current_center[0], -current_center[1])
        S = Transform2D.scaling_matrix(scale_factor, scale_factor)
        T_back = Transform2D.translation_matrix(current_center[0], current_center[1])
        transform = T_back @ S @ T_to_origin
        diamond.points = Transform2D.apply_transform(diamond.points, transform)

        closed_points = np.vstack([diamond.points[:, :2], diamond.points[0, :2]])
        ax.fill(closed_points[:, 0], closed_points[:, 1],
                color='lightblue', edgecolor='darkblue', linewidth=2, alpha=0.7, label='Ромб')

        final_center = diamond.get_center()
        ax.plot(final_center[0], final_center[1], 'ro', markersize=8, label='Центр')

        circle_angles = np.linspace(0, 2*np.pi, 100)
        circle_x = radius * np.cos(circle_angles)
        circle_y = radius * np.sin(circle_angles)
        ax.plot(circle_x, circle_y, 'g--', alpha=0.3, linewidth=1, label='Траєкторія')

        ax.legend(loc='upper right')

        if frame % 20 == 0:
            logger.info(f"📹 Створено кадр {frame}/200 ({frame/200*100:.0f}%)")

    anim = FuncAnimation(fig, update, frames=200, interval=50, repeat=True)

    logger.info("\n💾 Збереження у 'diamond_animation.gif'...")

    writer = PillowWriter(fps=20)
    anim.save('diamond_animation.gif', writer=writer, dpi=100)

    logger.info("\n✅ ГОТОВО!")
    logger.info("📁 Файл збережено: diamond_animation.gif")
    logger.info("🎬 Відкрийте GIF у будь-якому переглядачі зображень\n")

    plt.close()

if __name__ == "__main__":
    logger.info("="*70)
    logger.info("🎯 РІВЕНЬ I: Збереження анімації у GIF (для IntelliJ IDEA)")
    logger.info("="*70)

    save_animation()