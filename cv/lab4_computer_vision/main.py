import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# Створення директорії для результатів
output_dir = 'lab4_results'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

class CVFieldLab:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise FileNotFoundError(f"Неможливо завантажити {image_path}")
        self.results = {}

    def run_pipeline(self):
        # 1. Оригінал (Корекція кольору для відображення)
        rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.results['01_original'] = rgb

        # 2. Покращення: Грейскейл + CLAHE (Локальна еквалізація)
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        self.results['02_enhanced_hist'] = enhanced

        # 3. Фільтрація: Gaussian Blur (Метод усунення шуму)
        blurred = cv2.GaussianBlur(enhanced, (5, 5), 0)
        self.results['03_filtered'] = blurred

        # 4. Векторизація: Canny Edge Detection
        edges = cv2.Canny(blurred, 30, 120)
        self.results['04_vectorized_edges'] = edges

        # 5. Ідентифікація: Контури та Геометрія
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        identified = rgb.copy()

        count = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1500: # Геометричний фільтр за площею
                epsilon = 0.03 * cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, epsilon, True)

                # Посівні площі (4-6 кутів)
                if 4 <= len(approx) <= 8:
                    cv2.drawContours(identified, [approx], -1, (0, 255, 0), 3)
                    count += 1

        self.results['05_identified_objects'] = identified
        return count

    def save_all(self):
        """Збереження кожного кроку конвеєру як окремий файл"""
        print(f"--- Збереження результатів у папку {output_dir} ---")
        for name, img in self.results.items():
            file_path = os.path.join(output_dir, f"{name}.png")
            # OpenCV використовує BGR, тому для кольорових фото робимо реверс перед записом
            if len(img.shape) == 3:
                save_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            else:
                save_img = img
            cv2.imwrite(file_path, save_img)
            print(f"Збережено: {file_path}")

    def generate_report_plot(self):
        """Фінальний колаж для звіту"""
        plt.figure(figsize=(20, 10))
        for i, (name, img) in enumerate(self.results.items()):
            plt.subplot(1, 5, i+1)
            plt.imshow(img, cmap='gray' if len(img.shape) == 2 else None)
            plt.title(name.replace('_', ' ').capitalize())
            plt.axis('off')

        report_path = os.path.join(output_dir, "final_comparison_report.png")
        plt.savefig(report_path)
        plt.show()

# --- Запуск ---
def main():
    try:
        lab = CVFieldLab('input_dzz.png')
        found = lab.run_pipeline()
        lab.save_all()
        lab.generate_report_plot()
        print(f"\nУспішно ідентифіковано {found} посівних площ.")
    except Exception as e:
        print(f"Помилка: {e}")

if __name__ == "__main__":
    main()