import matplotlib.pyplot as plt
import numpy as np


def plot_mp178_face(skel: np.ndarray, output_folder: str = "."):
    face = skel[50:]
    face[:, 1] *= -1
    plt.scatter(face[:, 0], face[:, 1])
    for i, (x, y) in enumerate(face[:, :2]):
        plt.text(x, y, str(i + 50) , fontsize=6, ha='left')
    plt.savefig(f"{output_folder}/mp178_face.png", dpi=500)
    plt.close()
