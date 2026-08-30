"""
Member 1 - ML Lead
Task: 3D U-Net Architecture for Brain Tumor Segmentation
Day 1-2: Model definition using PyTorch + MONAI
"""

import torch
import torch.nn as nn
from monai.networks.nets import UNet
from monai.networks.layers import Norm


class FedMed3DUNet(nn.Module):
    """
    3D U-Net for brain tumor segmentation (BraTS 2021).

    Input:  (B, 4, 240, 240, 155)  - 4 MRI modalities: T1, T1ce, T2, FLAIR
    Output: (B, 4, 240, 240, 155)  - 4 classes: Background, NCR, ED, ET
    """

    def __init__(
        self,
        in_channels: int = 4,
        out_channels: int = 4,
        spatial_dims: int = 3,
        init_filters: int = 32,
    ):
        super(FedMed3DUNet, self).__init__()

        self.in_channels = in_channels
        self.out_channels = out_channels

        # MONAI UNet with instance normalization (better than BN for small batches)
        self.unet = UNet(
            spatial_dims=spatial_dims,
            in_channels=in_channels,
            out_channels=out_channels,
            channels=(init_filters, init_filters * 2, init_filters * 4,
                      init_filters * 8, init_filters * 16),
            strides=(2, 2, 2, 2),
            num_res_units=2,
            norm=Norm.INSTANCE,
            dropout=0.1,
        )

        self.softmax = nn.Softmax(dim=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass.
        Args:
            x: Input tensor (B, 4, H, W, D)
        Returns:
            Segmentation logits (B, 4, H, W, D)
        """
        logits = self.unet(x)
        return logits

    def predict(self, x: torch.Tensor) -> torch.Tensor:
        """Returns probability maps (softmax applied)."""
        return self.softmax(self.forward(x))

    def get_num_parameters(self) -> int:
        """Returns total number of trainable parameters."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


def build_model(device: str = "cuda") -> FedMed3DUNet:
    """
    Factory function to build and initialize the 3D U-Net model.
    Args:
        device: 'cuda' or 'cpu'
    Returns:
        Initialized FedMed3DUNet model on the specified device
    """
    model = FedMed3DUNet(
        in_channels=4,
        out_channels=4,
        spatial_dims=3,
        init_filters=32,
    )
    model = model.to(device)
    print(f"[FedMed] 3D U-Net initialized | Parameters: {model.get_num_parameters():,}")
    print(f"[FedMed] Running on device: {device}")
    return model


if __name__ == "__main__":
    # Quick sanity check
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = build_model(device)

    # Test forward pass with dummy input
    dummy_input = torch.randn(1, 4, 128, 128, 64).to(device)
    output = model(dummy_input)
    print(f"[FedMed] Input shape:  {dummy_input.shape}")
    print(f"[FedMed] Output shape: {output.shape}")
    assert output.shape == dummy_input.shape, "Output shape mismatch!"
    print("[FedMed] ✅ Model sanity check passed.")
