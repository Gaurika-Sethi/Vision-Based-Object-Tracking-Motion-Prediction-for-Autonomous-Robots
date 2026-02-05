import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def mean_error(csv_path):
    df = pd.read_csv(csv_path, header=None)
    df.columns = ["frame", "mx", "my", "px", "py"]
    error = np.sqrt((df["mx"] - df["px"])**2 + (df["my"] - df["py"])**2)
    return error.mean()

low_err = mean_error("results/noise_study/low_R/trajectory_log.csv")
mid_err = mean_error("results/noise_study/mid_R/trajectory_log.csv")
high_err = mean_error("results/noise_study/high_R/trajectory_log.csv")

labels = ["Low R", "Mid R", "High R"]
values = [low_err, mid_err, high_err]

plt.figure(figsize=(6,4))
plt.bar(labels, values, color="gray")
plt.ylabel("Mean Prediction Error (pixels)")
plt.xlabel("Measurement Noise Configuration")
plt.tight_layout()
plt.savefig("measurement_noise_barplot.pdf", bbox_inches="tight")