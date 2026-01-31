import pandas as pd
import matplotlib.pyplot as plt

def load_traj(csv_path):
    df = pd.read_csv(csv_path, header=None)
    df.columns = ["frame", "mx", "my", "px", "py"]
    return df["px"], df["py"]

px_l, py_l = load_traj("results/noise_study/low_R/trajectory_log.csv")
px_m, py_m = load_traj("results/noise_study/mid_R/trajectory_log.csv")
px_h, py_h = load_traj("results/noise_study/high_R/trajectory_log.csv")

plt.figure(figsize=(6,6))
plt.plot(px_l, py_l, label="Low R")
plt.plot(px_m, py_m, label="Mid R")
plt.plot(px_h, py_h, label="High R")

plt.gca().invert_yaxis()
plt.xlabel("X position (pixels)")
plt.ylabel("Y position (pixels)")
plt.title("Predicted Trajectory Comparison Across Noise Levels")
plt.legend()
plt.tight_layout()
plt.savefig("results/noise_study/trajectory_comparison.png")
plt.show()
