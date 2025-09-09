import os
import numpy as np

from skelretarget.utils import load_csv_skels, compute_bbox_stats, make_box_plot
from skelretarget import MP178SkelRetarget


def main(list_skels: list[np.ndarray], output_folder: str, prefix: str = ""):
    retargeter = MP178SkelRetarget()

    # computing results (stats) for each retargeting method
    results_dic = {}
    for mtd, kwargs in METHODS.items():
        RETARGET_SKELS = [retargeter.run(skels, mtd, **kwargs) for skels in LIST_SKELS]
        results_dic[mtd] = compute_bbox_stats(RETARGET_SKELS)

    # plotting results (and saving it)
    make_box_plot(
        dfs=[df for df in results_dic.values()],
        dfs_names=[name.replace("_", "\n").capitalize() for name in results_dic.keys()],
        save_fpath=f"{output_folder}/{prefix}compare_retarget_methods_bbox_stats"
    )

    return results_dic

if __name__ == "__main__":

    # -- Parameters
    # SOURCE_FOLDER = "./data/skel_data_MediaPiRGB__train__pelvis_centered_shoulder_normalized"
    SOURCE_FOLDER = "./data/skel_data_MediapiRGB__test__tricky__raw"
    SKELS_FILES = [os.path.join(SOURCE_FOLDER, f) for f in os.listdir(SOURCE_FOLDER) if f.endswith(".csv")]
    LIST_SKELS = [load_csv_skels(fpath) for fpath in SKELS_FILES]

    OUTPUT_FOLDER = "./outputs"

    METHODS = {
        "none": {},
        "bones_orientations": {
            "face_normalize_method": "bounding_box",
            "face_centering_method": "pelvis_face_centroid",
        },
        "similarity_transform": {
            "find_transform_method": "kabsch_umeyama",
        }
    }

    # --- Run main
    # results = main(LIST_SKELS, OUTPUT_FOLDER, "mp178_train_")
    results = main(LIST_SKELS, OUTPUT_FOLDER, "mp178_test_tricky_")

