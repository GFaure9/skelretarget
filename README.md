![Logo](./logo.png)

# SkelRetarget

*A Python toolbox to normalize and retarget skeletal motion sequences.*

---

`skelretarget` provides methods that:
1) take as input a sequence (or batch) of skeletal poses which may vary in scale, bone lengths 
or coordinate system, but sharing the same skeletal structure,
2) produce skeletal poses that preserves relative positions of joints within the skeletal reference 
while ensuring that all poses are expressed on a canonical / normalized skeleton or, at minimum, aligned to a common,
centered coordinate system.

## Usage example

```python
from skelretarget.utils import load_csv_skels, make_video_simple
from skelretarget import MP178SkelRetarget

skels = load_csv_skels('path/to/your/skels.csv')  # shape=(B, 178, 3) | assuming a Mediapipe-like 178 joints skeletal structure
retargeter = MP178SkelRetarget()
retargeted_skels = retargeter.run(
    method="bones_orientations",
    face_normalize_method="bounding_box", 
    face_centering_method="pelvis_face_centroid",
)
make_video_simple(
    skels, retargeted_skels, 
    bones=retargeter.skel_def["CONNECTIONS"],
    no_link_ids=retargeter.face_ids,
    out_file="path/to/your/output/video.mp4",
    fps=25,
)
```
