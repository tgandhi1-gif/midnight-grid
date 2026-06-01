"""The Midnight Grid - isolate a hidden 2 a.m. load in smart meter data."""
import os
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(11)
hours = np.arange(24)
H = 400

base = 2.0 + 1.2 * np.exp(-((hours - 19) ** 2) / 8) + 0.6 * np.exp(-((hours - 8) ** 2) / 6)
night_group = rng.random(H) < 0.18

load = np.zeros((H, 24))
for h in range(H):
    curve = base.copy()
    if night_group[h]:
        curve = curve + 1.5 * np.exp(-((hours - 2) ** 2) / 2)
    load[h] = curve + rng.normal(0, 0.05, 24)

avg = load.mean(0)
overnight_share = load[:, 0:5].sum() / load.sum()

print(f"Households with a 2 a.m. signature: {int(night_group.sum())} of {H}")
print(f"Overnight (0 to 5h) share of total load: {overnight_share * 100:.1f}%")

os.makedirs("outputs", exist_ok=True)
plt.figure(figsize=(9, 5))
plt.plot(hours, base, "--", color="#999999", label="expected")
plt.plot(hours, avg, color="#ff6a3d", lw=2.5, label="observed average")
plt.axvspan(0, 5, color="#ffab40", alpha=0.15, label="overnight window")
plt.xlabel("hour of day")
plt.ylabel("load (kW)")
plt.legend()
plt.title("The midnight grid: a hidden 2 a.m. load")
plt.tight_layout()
plt.savefig("outputs/midnight_grid.png", dpi=120)
print("Saved outputs/midnight_grid.png")
