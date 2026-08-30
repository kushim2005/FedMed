"""
Member 2 - ML Engineer
Task: PyTorch Dataset class + DataLoaders
Day 3-4: Wraps MONAI transforms into a usable DataLoader
"""

from typing import Optional, Tuple
from torch.utils.data import DataLoader
from monai.data import Dataset, CacheDataset

from data.preprocess import get_data_dicts, get_train_transforms, get_val_transforms


class BraTSDataset:
    """
    BraTS 2021 Dataset wrapper using MONAI CacheDataset for faster loading.

    Args:
        data_dir: Path to BraTS 2021 data directory
        split: 'train' or 'val'
        hospital_id: Which hospital partition (1, 2, or 3). None = all data.
        cache_rate: Fraction of data to cache in memory (0.0 to 1.0)
    """

    def __init__(
        self,
        data_dir: str,
        split: str = "train",
        hospital_id: Optional[int] = None,
        cache_rate: float = 0.5,
        num_workers: int = 4,
    ):
        self.split = split
        self.hospital_id = hospital_id

        data_dicts = get_data_dicts(
            data_dir=data_dir,
            split=split,
            hospital_id=hospital_id,
        )

        transforms = get_train_transforms() if split == "train" else get_val_transforms()

        # CacheDataset caches transformed samples in RAM for speed
        self.dataset = CacheDataset(
            data=data_dicts,
            transform=transforms,
            cache_rate=cache_rate,
            num_workers=num_workers,
        )

        print(f"[Dataset] Hospital {hospital_id or 'ALL'} | {split} | {len(data_dicts)} samples")

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        return self.dataset[idx]


def get_dataloaders(
    data_dir: str,
    batch_size: int = 1,
    num_workers: int = 4,
    hospital_id: Optional[int] = None,
    cache_rate: float = 0.5,
) -> Tuple[DataLoader, DataLoader]:
    """
    Returns train and validation DataLoaders.

    Args:
        data_dir: BraTS 2021 data directory
        batch_size: Samples per batch (typically 1 for 3D volumes)
        num_workers: Parallel data loading workers
        hospital_id: Hospital partition (1/2/3) or None for all
        cache_rate: Fraction of data to cache in RAM

    Returns:
        (train_loader, val_loader)
    """
    train_dataset = BraTSDataset(
        data_dir=data_dir,
        split="train",
        hospital_id=hospital_id,
        cache_rate=cache_rate,
        num_workers=num_workers,
    )

    val_dataset = BraTSDataset(
        data_dir=data_dir,
        split="val",
        hospital_id=hospital_id,
        cache_rate=0.0,  # Don't cache val set
        num_workers=num_workers,
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=1,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
    )

    return train_loader, val_loader
