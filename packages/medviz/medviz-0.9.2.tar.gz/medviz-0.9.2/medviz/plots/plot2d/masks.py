import math

import matplotlib.pyplot as plt
import numpy as np

from ...plots import generate_mask_colors, plot_contour, save_image
from ...utils import mask_path_to_data_ax, save_path_file


def masks_path(
    paths,
    rows=None,
    columns=None,
    mask_colors=None,
    titles=[],
    origin="upper",
    save_path=None,
):
    masks_data = [mask_path_to_data_ax(path) for path in paths]  # just for nifti files

    masks_array(
        masks_data=masks_data,
        rows=rows,
        columns=columns,
        titles=titles,
        origin=origin,
        mask_colors=mask_colors,
        save_path=save_path,
    )


def masks_array(
    masks_data,
    rows=None,
    columns=None,
    titles=[],
    mask_colors=None,
    origin="upper",
    save_path=None,
):
    print("Loading images...")

    try:
        assert len(masks_data[0].shape) == 2
    except AssertionError:
        raise ValueError("Masks must be 2D")

    num_masks = len(masks_data)  # Number of images
    rows = math.ceil(math.sqrt(num_masks))  # Number of rows in the grid
    columns = math.ceil(num_masks / rows)  # Number of columns in the grid

    mask_colors = generate_mask_colors(num_masks, mask_colors)

    _, axs = plt.subplots(rows, columns)
    if num_masks == 1:
        axs = np.array([axs])

    for i, ax in enumerate(axs.flat):
        if i < num_masks:
            title = titles[i] if titles else f"Mask {i}"

            plot_contour(
                ax,
                masks_data[i],
                color=mask_colors[i],
                title=title,
                origin=origin,
                levels=[0.5],
            )
            # ax.axis("off")
        else:
            ax.axis("off")

    plt.tight_layout()

    if save_path:
        save_path = save_path_file(save_path, suffix=".png")
        save_image(plt, save_path)
    else:
        plt.show()

    plt.close()
