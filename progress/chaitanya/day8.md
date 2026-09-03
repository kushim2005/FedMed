# Chaitanya Day 8 - Review Week 1 model, plan Week 2 training improvements

## Tasks Completed
* Reviewed Week 1 checkpoint: val Dice=0.61, loss plateau after epoch 8
* Identified underfitting in WT class; noted LR decay and clipping as fixes
* Drafted Week 2 training improvement plan in docs/week2_pipeline.md

## Files Modified/Created
* `train/federated_train.py` - added review comments and TODO markers
* `docs/week2_pipeline.md` - initial Week 2 plan skeleton

## Notes & Challenges
* Dice=0.61 is below target (0.70); suspect LR too high and no scheduler

## Tomorrow's Plan
* Add CosineAnnealingLR scheduler to local training loop
