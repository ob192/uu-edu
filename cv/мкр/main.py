import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import os

# --- МАТЕМАТИЧНИЙ МОДУЛЬ (Senior R&D) ---

def project_axonometric(points):
    """Аксонометрична проекція 3D -> 2D."""
    alpha = np.radians(30)
    x, y, z = points[:,0], points[:,1], points[:,2]
    px = (x - z) * np.cos(alpha)
    py = y + (x + z) * np.sin(alpha)
    return np.stack((px, py), axis=1)

def get_cube():
    """Синтез моделі паралелепіпеда."""
    # Вершини (x, y, z)
    nodes = np.array([
        [0, 0, 0], [2, 0, 0], [2, 1.5, 0], [0, 1.5, 0], # Задня (0-3)
        [0, 0, 2], [2, 0, 2], [2, 1.5, 2], [0, 1.5, 2]  # Передня (4-7)
    ])
    # Грані: F0(Back), F1(Front), F2(Bottom), F3(Top), F4(Left), F5(Right)
    faces = [
        [0, 3, 2, 1], # F0: Задня
        [4, 5, 6, 7], # F1: Передня
        [0, 1, 5, 4], # F2: Нижня
        [3, 2, 6, 7], # F3: Верхня
        [0, 4, 7, 3], # F4: Ліва
        [1, 2, 6, 5]  # F5: Права
    ]
    return nodes, faces

def run_pipeline():
    nodes, faces = get_cube()
    # Камера налаштована на бачення F0, F3, F4
    view_vector = np.array([1, -1, 1])

    steps = ["step1_wireframe", "step2_analysis", "step3_final"]
    titles = ["1. Каркасна модель", "2. Аналіз видимості (F0, F3, F4)", "3. Фінальний рендеринг"]

    for i, step in enumerate(steps):
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_aspect('equal')
        ax.set_title(titles[i], fontsize=14, fontweight='bold')

        for idx, f_indices in enumerate(faces):
            pts_3d = nodes[f_indices]
            pts_2d = project_axonometric(pts_3d)

            # Математика нормалей
            v1, v2 = pts_3d[1] - pts_3d[0], pts_3d[2] - pts_3d[0]
            normal = np.cross(v1, v2)
            is_visible = np.dot(normal, view_vector) < 0

            if step == "step1_wireframe":
                ax.add_patch(Polygon(pts_2d, fill=False, edgecolor='gray', ls='--'))

            elif step == "step2_analysis":
                color = 'green' if is_visible else 'red'
                ax.add_patch(Polygon(pts_2d, color=color, alpha=0.3))
                center = np.mean(pts_2d, axis=0)
                ax.text(center[0], center[1], f"F{idx}\n{'Visible' if is_visible else 'Hidden'}",
                        ha='center', fontsize=9)

            elif step == "step3_final" and is_visible:
                ax.add_patch(Polygon(pts_2d, facecolor='lightcyan', edgecolor='navy', lw=2.5))

        # Оформлення
        ax.grid(True, linestyle=':', alpha=0.6)
        all_2d = project_axonometric(nodes)
        ax.set_xlim(all_2d[:,0].min()-0.5, all_2d[:,0].max()+0.5)
        ax.set_ylim(all_2d[:,1].min()-0.5, all_2d[:,1].max()+0.5)

        plt.savefig(f"{step}.png", dpi=300)
        print(f"Збережено: {step}.png")
        plt.close()

if __name__ == "__main__":
    run_pipeline()