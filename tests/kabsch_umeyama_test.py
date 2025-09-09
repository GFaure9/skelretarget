import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as Rot

from skelretarget.utils import batch_kabsch_umeyama


def main(output_folder: str):
    S_target = np.array([
        [0, 0, 0],
        [-0.5, 1, 0],
        [0.5, 1, 0],
        [0.2, 0, 0.2]
    ])

    sca = 3.5
    rot = Rot.from_euler('zyx', [90, 45, 30], degrees=True).as_matrix()
    trans = np.array([[5., 0.6, 1.5]])
    S_source = (sca * (rot @ S_target.T) + trans.T).T

    batch_source = np.tile(S_source, reps=(100, 1, 1))
    batch_target = np.tile(S_target, reps=(100, 1, 1))
    s, R, t = batch_kabsch_umeyama(batch_source, batch_target)
    S_source_transformed = (s[0] * (R[0] @ S_source.T) + t[0]).T

    print("S_source: ", S_source)
    print("S_target: ", S_target)
    print("S_source_transformed: ", S_source_transformed)

    # -- Plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Unpack coordinates
    xs_source, ys_source, zs_source = zip(*S_source)
    xs_target, ys_target, zs_target = zip(*S_target)
    xs_source_transformed, ys_source_transformed, zs_source_transformed = zip(*S_source_transformed)
    # Plot points
    ax.scatter(xs_source, ys_source, zs_source, s=20, c='blue', alpha=0.5)
    ax.scatter(xs_target, ys_target, zs_target, s=20, c='magenta', alpha=0.5)
    ax.scatter(xs_source_transformed, ys_source_transformed, zs_source_transformed, s=20, c='green', alpha=0.5)
    # Label points
    for i, (x, y, z) in enumerate(S_source, start=1):
        ax.text(x, y, z, f'{i}', fontsize=12, ha='center', va='bottom', color='blue')
    for i, (x, y, z) in enumerate(S_target, start=1):
        ax.text(x, y, z, f'{i}', fontsize=12, ha='center', va='bottom', color='magenta')
    for i, (x, y, z) in enumerate(S_source_transformed, start=1):
        ax.text(x, y, z, f'{i}', fontsize=12, ha='center', va='bottom', color='green')
    # Show axes clearly
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.view_init(elev=100, azim=-90)
    # plt.show()
    plt.savefig(f"{output_folder}/kabsch_umeyama_test.png")
    plt.close()


if __name__ == "__main__":
    OUTPUT_FOLDER = "./outputs"
    main(OUTPUT_FOLDER)
