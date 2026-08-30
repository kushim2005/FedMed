"""
Member 2 - ML Engineer
Task: MONAI Data Preprocessing Pipeline
Day 1-3: Data loading, augmentation, and transforms for BraTS 2021
"""

import os
from pathlib import Path
from typing import List, Dict, Optional

from monai.transforms import (
    Compose,
    LoadImaged,
    EnsureChannelFirstd,
    ConvertToMultiChannelBasedOnBratsClassesd,
    CropForegroundd,
    RandSpatialCropd,
    RandFlipd,
    NormalizeIntensityd,
    RandScaleIntensityd,
    RandShiftIntensityd,
    Orientationd,
    Spacingd,
    ToTensord,
)


# BraTS 2021 modality keys
MODALITY_KEYS = ["t1", "t1ce", "t2", "flair"]
ALL_KEYS = MODALITY_KEYS + ["label"]


def get_train_transforms() -> Compose:
    """
    Full augmentation pipeline for training.
    Applied locally at each hospital node.
    """
    return Compose([
        # Step 1: Load all 4 modalities + segmentation label
        LoadImaged(keys=ALL_KEYS),
        EnsureChannelFirstd(keys=ALL_KEYS),

        # Step 2: Convert BraTS label classes (0,1,2,4) → (0,1,2,3)
        ConvertToMultiChannelBasedOnBratsClassesd(keys="label"),

        # Step 3: Reorient to standard anatomical orientation
        Orientationd(keys=ALL_KEYS, axcodes="RAS"),

        # Step 4: Resample to 1mm isotropic voxel spacing
        Spacingd(
            keys=ALL_KEYS,
            pixdim=(1.0, 1.0, 1.0),
            mode=("bilinear", "bilinear", "bilinear", "bilinear", "nearest"),
        ),

        # Step 5: Crop out background (zero regions)
        CropForegroundd(keys=ALL_KEYS, source_key="t1"),

        # Step 6: Random 3D patch crop - 128x128x64
        RandSpatialCropd(
            keys=ALL_KEYS,
            roi_size=(128, 128, 64),
            random_size=False,
        ),

        # Step 7: Random flipping for augmentation
        RandFlipd(keys=ALL_KEYS, prob=0.5, spatial_axis=0),
        RandFlipd(keys=ALL_KEYS, prob=0.5, spatial_axis=1),
        RandFlipd(keys=ALL_KEYS, prob=0.5, spatial_axis=2),

        # Step 8: Intensity normalization (Z-score per modality)
        NormalizeIntensityd(
            keys=MODALITY_KEYS,
            nonzero=True,    # Only normalize non-zero brain voxels
            channel_wise=True,
        ),

        # Step 9: Random intensity augmentation
        RandScaleIntensityd(keys=MODALITY_KEYS, factors=0.1, prob=0.5),
        RandShiftIntensityd(keys=MODALITY_KEYS, offsets=0.1, prob=0.5),

        # Step 10: Convert to PyTorch tensors
        ToTensord(keys=ALL_KEYS),
    ])


def get_val_transforms() -> Compose:
    """
    Minimal transforms for validation (no augmentation).
    """
    return Compose([
        LoadImaged(keys=ALL_KEYS),
        EnsureChannelFirstd(keys=ALL_KEYS),
        ConvertToMultiChannelBasedOnBratsClassesd(keys="label"),
        Orientationd(keys=ALL_KEYS, axcodes="RAS"),
        Spacingd(
            keys=ALL_KEYS,
            pixdim=(1.0, 1.0, 1.0),
            mode=("bilinear", "bilinear", "bilinear", "bilinear", "nearest"),
        ),
        NormalizeIntensityd(keys=MODALITY_KEYS, nonzero=True, channel_wise=True),
        ToTensord(keys=ALL_KEYS),
    ])


def get_data_dicts(data_dir: str, split: str = "train",
                   hospital_id: Optional[int] = None,
                   num_hospitals: int = 3) -> List[Dict[str, str]]:
    """
    Scan BraTS directory and build file dictionaries.

    Args:
        data_dir: Path to BraTS 2021 training data
        split: 'train' or 'val'
        hospital_id: If set (1/2/3), returns this hospital's partition only
        num_hospitals: Total number of hospital partitions

    Returns:
        List of dicts with paths for each modality and label
    """
    data_dir = Path(data_dir)
    if not data_dir.exists():
        raise FileNotFoundError(
            f"BraTS data not found at {data_dir}. "
            "Please download BraTS 2021 from https://www.synapse.org"
        )

    # Find all patient folders
    patient_dirs = sorted([d for d in data_dir.iterdir() if d.is_dir()])

    # Split 80/20 for train/val
    split_idx = int(len(patient_dirs) * 0.8)
    if split == "train":
        patients = patient_dirs[:split_idx]
    else:
        patients = patient_dirs[split_idx:]

    # Partition data among hospitals (simulate non-IID split)
    if hospital_id is not None:
        partition_size = len(patients) // num_hospitals
        start = (hospital_id - 1) * partition_size
        end = start + partition_size if hospital_id < num_hospitals else len(patients)
        patients = patients[start:end]

    # Build file dictionaries
    data_dicts = []
    for patient_dir in patients:
        pid = patient_dir.name
        data_dicts.append({
            "t1":    str(patient_dir / f"{pid}_t1.nii.gz"),
            "t1ce":  str(patient_dir / f"{pid}_t1ce.nii.gz"),
            "t2":    str(patient_dir / f"{pid}_t2.nii.gz"),
            "flair": str(patient_dir / f"{pid}_flair.nii.gz"),
            "label": str(patient_dir / f"{pid}_seg.nii.gz"),
        })

    return data_dicts
