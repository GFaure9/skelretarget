import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
from tqdm import tqdm


DEFAULT_LIMS = (
    # lim1 [source]
    (-1.5, 1.5),
    (0, 2.),
    (-0.1, 0.1),

    # lim2 [retargeted]
    (-1.5, 1.5),
    (0, 2.),
    (-0.1, 0.1),
)

def make_video_simple(
        seq1, seq2, bones,
        no_link_ids: list[int],
        lims: list[tuple] = None,
        out_file="test_mp128.mp4", fps=25
):
    T = min(len(seq1), len(seq2))
    fig = plt.figure(figsize=(8, 4))
    ax1 = fig.add_subplot(121, projection="3d")
    ax2 = fig.add_subplot(122, projection="3d")

    # Compute fixed boxes for each sequence
    def get_limits(seq, margin=0.1):
        pts = seq.reshape(-1, 3)
        mins, maxs = pts.min(0), pts.max(0)
        span = (maxs - mins) * margin
        return (mins[0]-span[0], maxs[0]+span[0]), \
               (mins[1]-span[1], maxs[1]+span[1]), \
               (mins[2]-span[2], maxs[2]+span[2])

    if lims is None:
        xlim1, ylim1, zlim1 = get_limits(seq1)
        xlim2, ylim2, zlim2 = get_limits(seq2)
    else:
        xlim1, ylim1, zlim1 = lims[:3]
        xlim2, ylim2, zlim2 = lims[3:]

    def draw(ax, frame, xlim, ylim, zlim, color):
        ax.cla()
        pts = frame
        for i, j, _ in bones:
            if i not in no_link_ids:
                ax.plot(*pts[[i, j]].T, c="k", lw=0.5)
        ax.scatter(*pts.T, c=color, s=0.5)

        # Set fixed box
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_zlim(*zlim)

        # Camera: XY in front, Z going inside
        ax.view_init(elev=100, azim=-90)
        # ax.invert_yaxis()

        # Show axis labels and ticks
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

    writer = FFMpegWriter(fps=fps)
    with writer.saving(fig, out_file, dpi=300):
        for t in tqdm(range(T)):
            draw(ax1, seq1[t], xlim1, ylim1, zlim1, "blue")
            draw(ax2, seq2[t], xlim2, ylim2, zlim2, "magenta")
            writer.grab_frame()
    plt.close(fig)
