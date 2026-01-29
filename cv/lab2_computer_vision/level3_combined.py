import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Polygon
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import random

class Transform2D:
    """Клас для 2D трансформацій"""

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

class Transform3D:
    """Клас для 3D трансформацій"""

    @staticmethod
    def rotation_x(angle):
        c, s = np.cos(angle), np.sin(angle)
        return np.array([[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]])

    @staticmethod
    def rotation_y(angle):
        c, s = np.cos(angle), np.sin(angle)
        return np.array([[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]])

    @staticmethod
    def rotation_z(angle):
        c, s = np.cos(angle), np.sin(angle)
        return np.array([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    @staticmethod
    def apply_transform(points, matrix):
        return (matrix @ points.T).T

class Diamond2D:
    """Ромб для 2D"""

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

class Parallelepiped3D:
    """Паралелепіпед для 3D"""

    def __init__(self, center=(0, 0, 0), width=2, height=3, depth=1.5):
        cx, cy, cz = center
        w, h, d = width/2, height/2, depth/2

        self.original_vertices = np.array([
            [cx-w, cy-h, cz-d, 1], [cx+w, cy-h, cz-d, 1],
            [cx+w, cy+h, cz-d, 1], [cx-w, cy+h, cz-d, 1],
            [cx-w, cy-h, cz+d, 1], [cx+w, cy-h, cz+d, 1],
            [cx+w, cy+h, cz+d, 1], [cx-w, cy+h, cz+d, 1],
        ])

        self.vertices = self.original_vertices.copy()

        self.faces = [
            [0, 1, 2, 3], [4, 5, 6, 7],
            [0, 1, 5, 4], [2, 3, 7, 6],
            [0, 3, 7, 4], [1, 2, 6, 5],
        ]

        self.face_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']

    def reset(self):
        self.vertices = self.original_vertices.copy()

    def get_faces_vertices(self):
        faces_vertices = []
        for face in self.faces:
            face_verts = self.vertices[face][:, :3]
            faces_vertices.append(face_verts)
        return faces_vertices

class CombinedAnimationGIF:
    """Комбінована анімація для збереження в GIF"""

    def __init__(self):
        # ВАЖЛИВО: Спочатку визначаємо список кольорів
        self.colors = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A',
            '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2',
            '#F8B739', '#52BE80'
        ]

        # Тепер створюємо фігуру
        self.fig = plt.figure(figsize=(16, 8))

        # 2D підграфік
        self.ax2d = self.fig.add_subplot(121)
        self.ax2d.set_xlim(-15, 15)
        self.ax2d.set_ylim(-15, 15)
        self.ax2d.set_aspect('equal')

        # 3D підграфік
        self.ax3d = self.fig.add_subplot(122, projection='3d')
        self.ax3d.set_xlim(-5, 5)
        self.ax3d.set_ylim(-5, 5)
        self.ax3d.set_zlim(-5, 5)

        # Об'єкти
        self.diamond_2d = Diamond2D(center=(0, 0), width=3, height=4)
        self.parallelepiped_3d = Parallelepiped3D(center=(0, 0, 0), width=3, height=4, depth=2)

        # Параметри 2D анімації
        self.appearance_phase = 0
        self.target_position = (0, 0)
        self.current_color = self.get_random_color()  # Тепер це працює!
        self.alpha_value = 0.0
        self.fade_in = True

        # Параметри 3D
        self.rotation_speed_3d = 0.05

    def get_random_color(self):
        """Отримання випадкового кольору"""
        return random.choice(self.colors)

    def get_random_position(self):
        """Отримання випадкової позиції"""
        x = random.uniform(-10, 10)
        y = random.uniform(-10, 10)
        return (x, y)

    def update_2d(self, frame):
        """Оновлення 2D частини"""
        self.ax2d.clear()
        self.ax2d.set_xlim(-15, 15)
        self.ax2d.set_ylim(-15, 15)
        self.ax2d.set_aspect('equal')
        self.ax2d.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        self.ax2d.set_xlabel('X', fontsize=11, fontweight='bold')
        self.ax2d.set_ylabel('Y', fontsize=11, fontweight='bold')
        self.ax2d.set_title(
            f'2D: Ромб з динамічною появою\nAlpha: {self.alpha_value:.2f}',
            fontsize=12, fontweight='bold', pad=10
        )

        # Логіка появи/зникнення
        if self.fade_in:
            self.alpha_value += 0.05
            if self.alpha_value >= 1.0:
                self.alpha_value = 1.0
                self.fade_in = False
                self.appearance_phase = 0
        else:
            self.appearance_phase += 1
            if self.appearance_phase > 40:  # Тривалість показу
                self.alpha_value -= 0.05
                if self.alpha_value <= 0.0:
                    self.alpha_value = 0.0
                    self.fade_in = True
                    # Нова позиція та колір
                    self.target_position = self.get_random_position()
                    self.current_color = self.get_random_color()

        # Трансформації
        self.diamond_2d.reset()

        # Переміщення
        tx, ty = self.target_position
        T = Transform2D.translation_matrix(tx, ty)
        self.diamond_2d.points = Transform2D.apply_transform(self.diamond_2d.points, T)

        # Обертання
        angle = frame * 0.02
        center = self.diamond_2d.get_center()

        T_to_origin = Transform2D.translation_matrix(-center[0], -center[1])
        R = Transform2D.rotation_matrix(angle)
        T_back = Transform2D.translation_matrix(center[0], center[1])

        transform = T_back @ R @ T_to_origin
        self.diamond_2d.points = Transform2D.apply_transform(self.diamond_2d.points, transform)

        # Відображення
        if self.alpha_value > 0:
            closed_points = np.vstack([
                self.diamond_2d.points[:, :2],
                self.diamond_2d.points[0, :2]
            ])

            self.ax2d.fill(
                closed_points[:, 0], closed_points[:, 1],
                color=self.current_color,
                edgecolor='black',
                linewidth=2,
                alpha=self.alpha_value
            )

            # Центр
            final_center = self.diamond_2d.get_center()
            self.ax2d.plot(
                final_center[0], final_center[1],
                'ko', markersize=6,
                markerfacecolor='red',
                alpha=self.alpha_value,
                zorder=5
            )

            # Інформація
            info_text = (
                f'Позиція: ({tx:.1f}, {ty:.1f})\n'
                f'Кут: {np.degrees(angle):.0f}°\n'
                f'Колір: {self.current_color}'
            )

            self.ax2d.text(
                0.02, 0.98, info_text,
                transform=self.ax2d.transAxes,
                fontsize=9,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7)
            )

    def update_3d(self, frame):
        """Оновлення 3D частини"""
        self.ax3d.clear()
        self.ax3d.set_xlim(-5, 5)
        self.ax3d.set_ylim(-5, 5)
        self.ax3d.set_zlim(-5, 5)
        self.ax3d.set_xlabel('X', fontsize=11, fontweight='bold')
        self.ax3d.set_ylabel('Y', fontsize=11, fontweight='bold')
        self.ax3d.set_zlabel('Z', fontsize=11, fontweight='bold')

        angle_deg = np.degrees(frame * self.rotation_speed_3d)
        self.ax3d.set_title(
            f'3D: Паралелепіпед (обертання)\nКут: {angle_deg:.1f}°',
            fontsize=12, fontweight='bold', pad=10
        )

        # Обертання
        self.parallelepiped_3d.reset()

        angle = frame * self.rotation_speed_3d
        Rx = Transform3D.rotation_x(angle)
        Ry = Transform3D.rotation_y(angle * 0.7)
        Rz = Transform3D.rotation_z(angle * 0.5)

        R_combined = Rz @ Ry @ Rx

        self.parallelepiped_3d.vertices = Transform3D.apply_transform(
            self.parallelepiped_3d.vertices, R_combined
        )

        # Відображення
        faces_vertices = self.parallelepiped_3d.get_faces_vertices()

        poly_collection = Poly3DCollection(
            faces_vertices,
            facecolors=self.parallelepiped_3d.face_colors,
            edgecolors='black',
            linewidths=1.5,
            alpha=0.85
        )

        self.ax3d.add_collection3d(poly_collection)
        self.ax3d.grid(True, alpha=0.3)
        self.ax3d.view_init(elev=20, azim=30)

    def update(self, frame):
        """Оновлення обох частин"""
        self.update_2d(frame)
        self.update_3d(frame)

        if frame % 20 == 0:
            print(f"📹 Створено кадр {frame}/300 ({frame/300*100:.0f}%)")

    def save(self, filename='combined_animation.gif', frames=300):
        """Збереження анімації"""
        print("\n" + "="*70)
        print("🎬 СТВОРЕННЯ КОМБІНОВАНОЇ АНІМАЦІЇ (2D + 3D)")
        print("="*70)
        print(f"⏳ Створення {frames} кадрів... Це займе ~60 секунд\n")

        anim = FuncAnimation(
            self.fig,
            self.update,
            frames=frames,
            interval=50,
            repeat=True
        )

        print(f"\n💾 Збереження у '{filename}'...")

        writer = PillowWriter(fps=20)
        anim.save(filename, writer=writer, dpi=100)

        print("\n✅ ГОТОВО!")
        print(f"📁 Файл збережено: {filename}")
        print("🎬 Відкрийте GIF у будь-якому переглядачі зображень")
        print("="*70 + "\n")

        plt.close()

def save_combined_animation():
    """Головна функція для збереження комбінованої анімації"""
    print("\n" + "="*70)
    print("🎯 РІВЕНЬ III: КОМБІНОВАНА АНІМАЦІЯ")
    print("="*70)

    try:
        anim = CombinedAnimationGIF()
        anim.save('combined_animation.gif', frames=300)
    except Exception as e:
        print(f"\n❌ ПОМИЛКА: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    save_combined_animation()