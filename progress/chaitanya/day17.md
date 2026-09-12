# Chaitanya Day 17 - Profile GPU memory: 3D UNet on 128³ patch uses 7.2 GB VRAM

## Tasks Completed
* Used `torch.cuda.memory_summary()` and `nvitop` to profile training memory
* 3D UNet (32 init features) with batch=2, patch 128³: peak 7.2 GB VRAM
* Documented memory breakdown (activations ~4.1 GB, params ~0.9 GB, gradients ~2.2 GB)

## Files Modified/Created
* `results/gpu_memory_profile.txt` - raw nvitop + torch.cuda output saved
* `docs/week2_pipeline.md` - added memory profiling section

## Notes & Challenges
* 7.2 GB leaves only ~0.8 GB headroom on 8 GB cards; need gradient accumulation

## Tomorrow's Plan
* Implement gradient accumulation (steps=4) to reduce effective batch memory
