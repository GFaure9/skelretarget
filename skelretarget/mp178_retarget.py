import numpy as np

from .utils import batch_kabsch_umeyama
from .skeleton_defs import MP178SKEL
from .retarget import SkelRetarget


class MP178SkelRetarget(SkelRetarget):
    def __init__(self):
        mp178_skel_def = MP178SKEL
        super().__init__(skel_def=mp178_skel_def)
        self.face_ids = []
        for k, v in self.skel_def["IDS"].items():
            if "face" in k:
                self.face_ids.append(v)
        self.torso_ids = [
            self.skel_def["IDS"]["RShoulder"],
            self.skel_def["IDS"]["LShoulder"],
            self.skel_def["IDS"]["RHip"],
            self.skel_def["IDS"]["LHip"]
        ]
        self.arms_hands_ids = []
        for i in self.skel_def["IDS"].values():
            if i not in self.face_ids and i not in self.torso_ids:
                self.arms_hands_ids += [i]
        self.arms_hands_ids.sort()

    @property
    def retarget_methods(self):
        mtds = {
            "none": {},

            "bones_orientations": {

                "face_normalize_method": [
                    "temples",
                    "right_eye_corner_top_head",
                    "eyes_corners",
                    "bounding_box",
                ],

                "face_centering_method": [
                    "pelvis_top_head",
                    "pelvis_face_centroid",
                ],
            },

            "similarity_transform": {

                "find_transform_method": [
                    "kabsch_umeyama",
                ],
            },
        }
        return mtds

    def _bones_orientations_based_retarget(
            self,
            skels: np.ndarray,
            face_normalize_method: str, face_centering_method: str,
    ) -> np.ndarray:
        skels_retarg = np.zeros_like(skels)

        # -- compute retargeted shoulders and hips
        i_Rhip, i_Lhip = self.skel_def["IDS"]["RHip"], self.skel_def["IDS"]["LHip"]
        x_Rhip, x_Lhip = skels[:, [i_Rhip]], skels[:, [i_Lhip]]
        x_pelv = (x_Rhip + x_Lhip) / 2

        i_RShoulder, i_LShoulder = self.skel_def["IDS"]["RShoulder"], self.skel_def["IDS"]["LShoulder"]
        x_RShoulder, x_LShoulder = skels[:, [i_RShoulder]], skels[:, [i_LShoulder]]

        u_pelv_to_RShoulder = (x_RShoulder - x_pelv) / np.linalg.norm(x_RShoulder - x_pelv, axis=-1, keepdims=True)
        u_pelv_to_LRShoulder = (x_LShoulder - x_pelv) / np.linalg.norm(x_LShoulder - x_pelv, axis=-1, keepdims=True)

        pelvis_target = np.zeros((skels.shape[0], 1, 3))
        pelv_to_shoulder_fa = 0.6  # 0.62
        x_RShoulder_retarg = pelvis_target + u_pelv_to_RShoulder * pelv_to_shoulder_fa
        x_LShoulder_retarg = pelvis_target + u_pelv_to_LRShoulder * pelv_to_shoulder_fa

        ratio = 0.7  # 0.9
        v_RHip_to_LHip = ratio * (x_LShoulder_retarg - x_RShoulder_retarg)
        x_RHip_retarg = pelvis_target - v_RHip_to_LHip / 2
        x_LHip_retarg = pelvis_target + v_RHip_to_LHip / 2

        skels_retarg[:, self.torso_ids] = np.concat(
            [x_RShoulder_retarg, x_LShoulder_retarg, x_RHip_retarg, x_LHip_retarg],
            axis=1
        )

        # -- compute retargeted arms + hands
        for iParent, iChild, length in self.skel_def["CONNECTIONS"]:
            if iChild in self.arms_hands_ids:
                if (skels_retarg[:, [iChild]] == 0).any() and length is not None:
                    xP, xC = skels[:, [iParent]], skels[:, [iChild]]
                    u = (xC - xP) / np.linalg.norm(xC - xP, axis=-1, keepdims=True)
                    skels_retarg[:, [iChild]] = skels_retarg[:, [iParent]] + u * length

        # -- compute retargeted face
        if face_normalize_method == "temples":
            # using inter-temples distance (forehead width) to normalize
            i_RTemple, i_LTemple = 106, 167
            x_RTemple, x_LTemple = skels[:, [i_RTemple]], skels[:, [i_LTemple]]
            normalized_face = skels[:, self.face_ids] / np.linalg.norm(x_RTemple - x_LTemple, axis=-1, keepdims=True)
            normalized_face *= 0.2  # ensure consistent scale with respect to the rest of the skeleton

        elif face_normalize_method == "right_eye_corner_top_head":
            # using the distance between the top of the forehead and the right eye to normalize
            i_top_forehead, i_Reye = 52, 89
            x_top_forehead, x_Reye = skels[:, [i_top_forehead]], skels[:, [i_Reye]]
            normalized_face = skels[:, self.face_ids] / np.linalg.norm(x_top_forehead - x_Reye, axis=-1, keepdims=True)
            normalized_face *= 0.07  # ensure consistent scale with respect to the rest of the skeleton

        elif face_normalize_method == "eyes_corners":
            # using distance between eye corners to normalize
            i_Reye, i_Leye = 89, 151
            x_Reye, x_Leye = skels[:, [i_Reye]], skels[:, [i_Leye]]
            normalized_face = skels[:, self.face_ids] / np.linalg.norm(x_Reye - x_Leye, axis=-1, keepdims=True)
            normalized_face *= 0.07  # ensure consistent scale with respect to the rest of the skeleton

        elif face_normalize_method == "bounding_box":
            # using face bounding box to normalize
            face = skels[:, self.face_ids]
            min_xyz = face.min(axis=1, keepdims=True)
            max_xyz = face.max(axis=1, keepdims=True)
            bbox_sizes = max_xyz - min_xyz
            max_lengths = bbox_sizes.max(axis=-1, keepdims=True)
            normalized_face = face / max_lengths
            normalized_face *= 0.2  # ensure consistent scale with respect to the rest of the skeleton

        else:
            raise ValueError(f"face_normalize_method='{face_normalize_method}' is not a valid method.")

        if face_centering_method == "pelvis_top_head":
            # ensuring a constant distance between the pelvis and the top of the forehead
            v_pelv_to_neck = u_pelv_to_RShoulder + u_pelv_to_LRShoulder
            u_pelv_to_neck = v_pelv_to_neck / np.linalg.norm(v_pelv_to_neck, axis=-1, keepdims=True)
            top_forehead_target = pelvis_target + u_pelv_to_neck * 0.9
            i_top_forehead_face_only = 2
            normalized_face += (top_forehead_target - normalized_face[:, [i_top_forehead_face_only]])

        elif face_centering_method == "pelvis_face_centroid":
            # ensuring constant distance between the pelvis and the face centroid
            v_pelv_to_neck = u_pelv_to_RShoulder + u_pelv_to_LRShoulder
            u_pelv_to_neck = v_pelv_to_neck / np.linalg.norm(v_pelv_to_neck, axis=-1, keepdims=True)
            face_centroid_target = pelvis_target + u_pelv_to_neck * 0.75
            normalized_face += (face_centroid_target - normalized_face.mean(axis=1, keepdims=True))

        else:
            raise ValueError(f"face_centering_method='{face_centering_method}' is not a valid method.")

        # filling `skels_retarg` with the face
        skels_retarg[:, self.face_ids] = normalized_face

        global_sca = 2
        return skels_retarg * global_sca

    def _similarity_transform_based_retarget(
            self, skels: np.ndarray,
            find_transform_method: str,
            face_normalize_method: str = None,
    ) -> np.ndarray:
        # retrieving shoulders and hips joints coordinates from the `skels`
        ids = self.skel_def["IDS"]
        i_RShoulder, i_LShoulder = ids["RShoulder"], ids["LShoulder"]
        i_RHip, i_Lhip = ids["RHip"], ids["LHip"]
        source_pts = skels[:, [i_RShoulder, i_LShoulder, i_RHip, i_Lhip]]  # shape=(T, 4, 3)

        # defining target shoulder and hips (must respect order previous `skels` extraction: RS->LS->RH->LH)
        T = skels.shape[0]
        target_torso = np.array([
            [-0.5, 1, 0],  # RShoulder
            [0.5, 1, 0],  # LShoulder
            [-0.25, 0, 0],  # RHip
            [0.25, 0, 0]  # LHip
        ])
        target_pts = np.tile(target_torso, reps=(T, 1, 1))  # shape=(T, 4, 3)

        # -- find and apply similarity transformation
        if find_transform_method == "kabsch_umeyama":
            c, R, t = batch_kabsch_umeyama(source_pts, target_pts)  # (B, 1, 1) | (B, 3, 3) | (B, 3, 1)
            skels_retarg = (c * (R @ skels.transpose(0, 2, 1)) + t).transpose(0, 2, 1)

        else:
            raise ValueError(f"find_transform_method='{find_transform_method}' is not a valid method.")

        return skels_retarg

    def run(self, skels: np.ndarray, method: str = "none", **kwargs) -> np.ndarray:
        if method == "bones_orientations":
            return self._bones_orientations_based_retarget(skels, **kwargs)
        elif method == "similarity_transform":
            return  self._similarity_transform_based_retarget(skels, **kwargs)
        elif method == "none":
            return skels
        else:
            raise ValueError(
                f"Re-targeting method '{method}' is not valid. Check possible methods:\n{self.retarget_methods}"
            )