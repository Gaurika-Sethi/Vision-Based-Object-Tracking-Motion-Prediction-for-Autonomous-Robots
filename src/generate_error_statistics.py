import pandas as pd
import numpy as np

def compute_error_stats(csv_path):
    # Read CSV (no header in your logs)
    df = pd.read_csv(csv_path, header=None)
    df.columns = ["frame", "mx", "my", "px", "py"]

    # Euclidean prediction error
    error = np.sqrt((df["mx"] - df["px"])**2 + (df["my"] - df["py"])**2)

    # Descriptive statistics
    stats = {
        "count": error.count(),
        "mean": error.mean(),
        "std": error.std(),
        "min": error.min(),
        "25%": error.quantile(0.25),
        "50%": error.quantile(0.50),
        "75%": error.quantile(0.75),
        "max": error.max()
    }
    return stats

# Paths
paths = {
    "Low R": "results/noise_study/low_R/trajectory_log.csv",
    "Mid R": "results/noise_study/mid_R/trajectory_log.csv",
    "High R": "results/noise_study/high_R/trajectory_log.csv"
}

# Compute table
table = pd.DataFrame({
    label: compute_error_stats(path)
    for label, path in paths.items()
})

# Save table
output_path = "results/noise_study/error_statistics_table.csv"
table.to_csv(output_path)

print("Table generated successfully!")
print(table)