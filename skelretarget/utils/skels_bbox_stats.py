from tqdm import tqdm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def compute_bbox_stats(list_skels: list[np.ndarray]) -> pd.DataFrame:
    # `list_skels` is a list of N skels sequences of shape (T, Npts, 3) - with varying T

    stats = {
        "std_bbox_lenX": [],
        "std_bbox_lenY": [],
        "std_bbox_lenZ": [],
        "std_bbox_lenX+lenY+lenZ": [],
        "meanXYZ_std_centroid": [],
    }

    for skels in tqdm(list_skels):
        # -- find skeletal pose bounding box X, Y, Z lengths for each frame
        bboxes_lenX = skels[:, :, 0].max(axis=1) - skels[:, :, 0].min(axis=1)  # shape=(T,)
        bboxes_lenY = skels[:, :, 1].max(axis=1) - skels[:, :, 1].min(axis=1)
        bboxes_lenZ = skels[:, :, 2].max(axis=1) - skels[:, :, 2].min(axis=1)

        # -- normalize per sequence: (* - min) / (max - min)
        bboxes_lenX = (bboxes_lenX - bboxes_lenX.min()) / (bboxes_lenX.max() - bboxes_lenX.min())  # shape=(T,)
        bboxes_lenY = (bboxes_lenY - bboxes_lenY.min()) / (bboxes_lenY.max() - bboxes_lenY.min())
        bboxes_lenZ = (bboxes_lenZ - bboxes_lenZ.min()) / (bboxes_lenZ.max() - bboxes_lenZ.min())

        # -- compute standard deviation of normalized bbox lengths for each dimension
        std_bboxes_lenX = np.std(bboxes_lenX)
        std_bboxes_lenY = np.std(bboxes_lenY)
        std_bboxes_lenZ = np.std(bboxes_lenZ)

        # -- compute standard deviation of the per frame sum over X, Y, Z of normalized bbox lengths
        std_bboxes_sum_len = np.std(bboxes_lenX + bboxes_lenY + bboxes_lenZ)

        # -- compute std of normalized centroid
        centroid = skels.mean(axis=1)  # shape=(T, 3)
        c_minX, c_maxX = centroid[:, 0].min(), centroid[:, 0].max()
        c_minY, c_maxY = centroid[:, 1].min(), centroid[:, 1].max()
        c_minZ, c_maxZ = centroid[:, 2].min(), centroid[:, 2].max()
        centroid_bbox_len = np.linalg.norm(np.array([c_minX, c_minY, c_minZ]) - np.array([c_maxX, c_maxY, c_maxZ]))
        centroid /= centroid_bbox_len
        meanXYZ_std_centroids = np.mean([np.std(centroid[:, 0]), np.std(centroid[:, 1]), np.std(centroid[:, 2])])

        # -- update `stats` data dict
        stats["std_bbox_lenX"].append(std_bboxes_lenX)
        stats["std_bbox_lenY"].append(std_bboxes_lenY)
        stats["std_bbox_lenZ"].append(std_bboxes_lenZ)
        stats["std_bbox_lenX+lenY+lenZ"].append(std_bboxes_sum_len)
        stats["meanXYZ_std_centroid"].append(meanXYZ_std_centroids)

    df = pd.DataFrame.from_dict(stats)

    return df


def make_box_plot(
        dfs: list[pd.DataFrame], dfs_names: list[str],
        column_names: list[str] = None,
        save_fpath: str = None,
):
    if column_names is None:
        print("Since no `column_names` were provided, generating boxplot for all columns.")
        column_names = dfs[0].columns

    n_cols = len(column_names)
    fig, axes = plt.subplots(1, n_cols, figsize=(5 * n_cols, 5), squeeze=False)

    for idx, col in enumerate(column_names):
        data = [df[col].dropna() for df in dfs]  # collect data per column
        axes[0, idx].boxplot(data, labels=[dfs_names[i] for i in range(len(dfs))])
        axes[0, idx].set_title(f"Boxplot - ${col.replace("_", "~")}$")
        axes[0, idx].set_ylabel(col)

    plt.tight_layout()
    if save_fpath:
        plt.savefig(save_fpath, dpi=500)
        plt.close()
    else:
        plt.show()
