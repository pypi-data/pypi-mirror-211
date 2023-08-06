from pathlib import Path

import nibabel as nib
import numpy as np

import medviz as viz

# result = np.load("result.npy")

# result = ~result
unique, counts = np.unique(result, return_counts=True)
values = dict(zip(unique, counts))
print(values)

unique, counts = np.unique(~result, return_counts=True)
values = dict(zip(unique, counts))
print(values)


ct_image = nib.load("dataset/1-1.nii")
ct_data = ct_image.get_fdata()

np.save("ct_data.npy", ct_data)

# exit()
ct_data = np.load("ct_data.npy")
ct_data = np.flip(np.rot90(ct_data, axes=(1, 0)), axis=1)

result = np.flip(np.rot90(result, axes=(1, 0)), axis=1)


viz.layered_plot_data3D(
    image_data=ct_data,
    masks_data=[~result],
    mask_colors=["red"],
    title="Layered Plot",
)

viz.layered_plot_data3D(
    image_data=ct_data,
    masks_data=[result],
    mask_colors=["red"],
    title="Layered Plot",
)


exit()
p = Path("/media/storage/github/mohsen2/bowel/results/TS_CT_Full/1/1-1.nii")

# arr = [organ.stem.split(".")[0] for organ in p.glob("*.nii.gz")]


def mask_path_to_data(mask_path):
    mask_data = nib.load(mask_path)

    mask_data = mask_data.get_fdata()
    mask_data = mask_data.astype(np.bool_)
    # mask_data = np.flip(np.rot90(mask_data, axes=(1, 0)), axis=1)
    # mask_data = np.ma.masked_where(mask_data == False, mask_data)
    return mask_data


result = np.zeros((512, 512, 158), dtype=bool)


for pth in p.glob("*.nii.gz"):
    mask_data = mask_path_to_data(pth)
    result = result | mask_data


np.save("result.npy", result)
# result = np.ma.masked_where(result == False, result)
print(np.unique(result))
# print(result)
