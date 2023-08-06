from pathlib import Path

# from tkinter import NO
import nibabel as nib
import numpy as np

base_path = Path("/media/storage/github/mohsen2/bowel/results/TS_CT_Full/1/1-1.nii")

arr = [organ for organ in base_path.glob("*.nii.gz")]


first_mask = nib.load(arr[0])
first_mask_data = first_mask.get_fdata()


res = np.empty(first_mask_data.shape, dtype=np.bool_)
for i in arr:
    mask = nib.load(i)
    mask_data = mask.get_fdata()
    mask_data = mask_data.astype(np.bool_)
    res = res | mask_data


np.save("allMasks.npy", res)
print(res.shape)
