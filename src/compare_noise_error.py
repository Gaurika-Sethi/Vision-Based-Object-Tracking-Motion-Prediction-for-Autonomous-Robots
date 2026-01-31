import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_error(csv_path):
    df = pd.read_csv(csv_path, header=None)
    df.columns = ["frame", "mx", "my", "px", "py"]
    error = np.sqrt((df["mx"] - df["px"])**2 + (df["my"] - df["py"])**2)
    return df["frame"], error

frame_l, err_l = load_error("results/noise_study/low_R/trajectory_log.csv")
frame_m, err_m = load_error("results/noise_study/mid_R/trajectory_log.csv")
frame_h, err_h = load_error("results/noise_study/high_R/trajectory_log.csv")

plt.figure(figsize=(8,4))
plt.plot(frame_l, err_l, label="Low R (High Trust in Sensor)")
plt.plot(frame_m, err_m, label="Mid R (Balanced)")
plt.plot(frame_h, err_h, label="High R (High Trust in Model)")

plt.xlabel("Frame Index")
plt.ylabel("Prediction Error (pixels)")
plt.title("Effect of Measurement Noise on Prediction Error")
plt.legend()
plt.tight_layout()
plt.savefig("results/noise_study/error_comparison.png")
plt.show()
