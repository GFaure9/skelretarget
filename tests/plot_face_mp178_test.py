from skelretarget.utils import plot_mp178_face, load_csv_skels


if __name__ == "__main__":
    t = 5
    source_skel = "./data/skel_data_MediaPiRGB__train__pelvis_centered_shoulder_normalized/skels1.csv"
    skel178_one_pose = load_csv_skels(source_skel)[t]
    plot_mp178_face(skel178_one_pose, "./outputs")
