import numpy as np
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def run_3d_reconstruction(image_path1, image_path2):
    # 1. LOAD DATA
    img1 = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image_path2, cv2.IMREAD_GRAYSCALE)

    if img1 is None or img2 is None:
        print(f"Error: Could not load images from {image_path1} or {image_path2}")
        return

    # 2. SETUP: Intrinsic Camera Matrix K
    h, w = img1.shape
    focal_length = w
    K = np.array([[focal_length, 0, w/2],
                  [0, focal_length, h/2],
                  [0, 0, 1]], dtype=np.float32)

    # 3. FEATURE DETECTION (SIFT)
    sift = cv2.SIFT_create(nfeatures=5000)
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    # 4. FEATURE MATCHING
    flann = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=50))
    matches = flann.knnMatch(des1, des2, k=2)

    # Lowe's Ratio Test
    good_matches = []
    pts1, pts2 = [], []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)
            pts1.append(kp1[m.queryIdx].pt)
            pts2.append(kp2[m.trainIdx].pt)

    pts1 = np.float32(pts1)
    pts2 = np.float32(pts2)

    if len(pts1) < 8:
        print("Error: Not enough points matched.")
        return

    # 5. GEOMETRY
    E, mask = cv2.findEssentialMat(pts1, pts2, K, method=cv2.RANSAC, prob=0.999, threshold=1.0)
    _, R, t, mask = cv2.recoverPose(E, pts1, pts2, K)

    # 6. TRIANGULATION
    P1 = K @ np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])
    P2 = K @ np.hstack((R, t))
    points_4d_hom = cv2.triangulatePoints(P1, P2, pts1.T, pts2.T)
    points_3d = (points_4d_hom[:3] / points_4d_hom[3]).T

    # 7. SAVE & VISUALIZE
    # A. Save 2D Matches Image
    match_img = cv2.drawMatches(img1, kp1, img2, kp2, good_matches[:100], None,
                                flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    cv2.imwrite('reconstruction_matches.jpg', match_img)
    print("Saved: reconstruction_matches.jpg")

    # B. Save 3D Points to CSV
    np.savetxt("reconstructed_points.csv", points_3d, delimiter=",", header="X,Y,Z", comments='')
    print("Saved: reconstructed_points.csv")

    # C. Visualize 3D
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Filter for display (remove outliers)
    z_mask = (points_3d[:, 2] > 0) & (points_3d[:, 2] < 50)
    filtered_points = points_3d[z_mask]

    if len(filtered_points) > 0:
        ax.scatter(filtered_points[:, 0], filtered_points[:, 2], -filtered_points[:, 1],
                   c=filtered_points[:, 2], cmap='viridis', s=2)
        plt.title(f"3D Cloud - {len(filtered_points)} points")
        plt.savefig('3d_plot.png')
        print("Saved: 3d_plot.png")
        plt.show()

if __name__ == "__main__":
    run_3d_reconstruction('cam_l.jpg', 'cam_r.jpg')