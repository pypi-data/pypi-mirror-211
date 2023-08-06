import math

import matplotlib.pyplot as plt
import numpy as np

from ...plots import plot_image, save_image
from ...utils import image_path_to_data_ax, save_path_file


def images_path(
    paths,
    rows=None,
    columns=None,
    titles=[],
    cmap="gray",
    origin="upper",
    save_path=None,
):
    images_data = [image_path_to_data_ax(path) for path in paths]

    images_array(
        images_data=images_data,
        rows=rows,
        columns=columns,
        titles=titles,
        cmap=cmap,
        origin=origin,
        save_path=save_path,
    )


def images_array(
    images_data,
    rows=None,
    columns=None,
    titles=[],
    cmap="gray",
    origin="upper",
    save_path=None,
):
    print("Loading images...")

    try:
        assert len(images_data[0].shape) == 2
    except AssertionError:
        raise ValueError("Images must be 2D")

    num_images = len(images_data)  # Number of images
    rows = math.ceil(math.sqrt(num_images))  # Number of rows in the grid
    columns = math.ceil(num_images / rows)  # Number of columns in the grid

    _, axs = plt.subplots(rows, columns)
    if num_images == 1:
        axs = np.array([axs])

    for i, ax in enumerate(axs.flat):
        if i < num_images:
            title = titles[i] if titles else f"Image {i}"
            plot_image(ax, images_data[i], cmap=cmap, title=title, origin=origin)
            ax.axis("off")
        else:
            ax.axis("off")

    plt.tight_layout()

    if save_path:
        save_path = save_path_file(save_path, suffix=".png")
        save_image(plt, save_path)
    else:
        plt.show()

    plt.close()
