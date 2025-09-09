from typing import Callable

import os
from pathlib import Path
import numpy as np

from skelretarget.utils import load_csv_skels, make_video_simple, DEFAULT_LIMS
from skelretarget import MP178SkelRetarget


def invert_y(skels: np.ndarray) -> np.ndarray:
    new_skels = skels.copy()
    new_skels[:, :, 1] *= -1
    return new_skels


def main(
        methods: dict,
        skels_files: list[str],
        prepro_transf: Callable,
        output_folder: str
):
    # instantiate 'retargeter'
    retargeter = MP178SkelRetarget()

    # retrieve bones (connections) data - for future plots
    bones = retargeter.skel_def["CONNECTIONS"]

    for mtd, kwargs in methods.items():
        print(f"   | Retargeting method: {mtd}")
        print("   |     Arguments:")
        for k, v in kwargs.items():
            print(f"   |        - {k}: {v}")
        print("   |     Number of files: ", len(skels_files))

        # create subfolder to store results if it does not exist
        mtd_output_folder = f"{output_folder}/{mtd}"
        os.makedirs(mtd_output_folder, exist_ok=True)

        for fpath in skels_files:
            # 1/ load original skeletal poses
            skels_original = load_csv_skels(fpath)

            # 2/ transform as needed skeletal poses
            skels_original = prepro_transf(skels_original)

            # 3/ compute retargeted version skeletal poses
            skels_retarget = retargeter.run(skels_original, method=mtd, **kwargs)

            # 4/ create a video of original VS retargeted poses
            make_video_simple(
                skels_original,
                skels_retarget,
                bones,
                retargeter.face_ids,
                # DEFAULT_LIMS,
                None,
                f"{mtd_output_folder}/retarget_mp178_MTD{mtd}_{Path(fpath).stem}.mp4", 25,
            )


if __name__ == "__main__":

    # -- Parameters
    METHODS = {
        "bones_orientations": {
            "face_normalize_method": "bounding_box", # "bounding_box", "temples", "right_eye_corner_top_head", "eyes_corners"
            "face_centering_method": "pelvis_face_centroid",  # "pelvis_face_centroid", "pelvis_top_head"
        },
        "similarity_transform": {
            "find_transform_method": "kabsch_umeyama",
        }
    }

    # SOURCE_FOLDER = "./data/skel_data_MediaPiRGB__train__pelvis_centered_shoulder_normalized"
    SOURCE_FOLDER = "./data/skel_data_MediapiRGB__test__tricky__raw"
    OUTPUT_FOLDER = "./outputs"
    SKELS_FILES = [os.path.join(SOURCE_FOLDER, f) for f in os.listdir(SOURCE_FOLDER) if f.endswith(".csv")]
    SKELS_FILES.sort()

    # --- Run main
    main(METHODS, SKELS_FILES, invert_y, OUTPUT_FOLDER)
