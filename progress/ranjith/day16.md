# Ranjith Day 16 - feat(eval): add moving average smoothing to loss curves

## Tasks Completed
* Implemented `smooth(values, window=3)` using `np.convolve` in `plot_convergence()`.
* Applied smoothing to global Dice and loss curves in convergence plot.
* Added dashed red smoothed line alongside raw blue line for clarity.

## Files Modified/Created
* `eval/federated_metrics.py` — `smooth()` helper + updated `plot_convergence()`

## Notes & Challenges
* `np.convolve` with `mode="valid"` shortens the array by `window-1`; adjusted x-axis accordingly.

## Tomorrow's Plan
* Implement per-hospital local Dice tracking alongside global aggregated Dice.
