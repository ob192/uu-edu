import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Polygon
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# ... (тут весь код класів Transform2D, Transform3D, Diamond2D, Parallelepiped3D)

def main_menu():
    logger.info("\n" + "="*70)
    logger.info("🎯 ЛАБОРАТОРНА РОБОТА: 2D/3D ТРАНСФОРМАЦІЇ")
    logger.info("="*70)
    logger.info("\nОберіть рівень для створення GIF анімації:")
    logger.info("  1️⃣  - Рівень I: 2D Ромб (переміщення + обертання + масштабування)")
    logger.info("  2️⃣  - Рівень II: 3D Паралелепіпед (обертання)")
    logger.info("  3️⃣  - Рівень III: Комбінована анімація (2D + 3D)")
    logger.info("  🎬 - Створити ВСІ ТРИ анімації")
    logger.info("  ❌ - Вийти")
    logger.info("="*70)

    choice = input("\n👉 Ваш вибір: ").strip()

    if choice == '1':
        logger.info("\n🎬 Створення Рівня I...")
        # save_animation() # Виклик функції з першого повідомлення
    elif choice == '2':
        logger.info("\n🎬 Створення Рівня II...")
        # save_3d_animation() # Виклик функції з другого повідомлення
    elif choice == '3':
        logger.info("\n🎬 Створення Рівня III...")
        # Код збереження рівня III
    elif choice.lower() in ['all', 'всі', '🎬']:
        logger.info("\n🎬 Створення всіх трьох анімацій...")
        # Виклик усіх функцій
    else:
        logger.info("\n👋 До побачення!")

if __name__ == "__main__":
    main_menu()