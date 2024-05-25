import json
import pandas as pd
from pathlib import Path

result_files = [f for f in Path("./results/").rglob("*.json")]

results = []

for file in result_files:
    with open(file, "r") as f:
        data = json.load(f)

        for result in data["results"]:
            if "python" in result["command"]:
                strategy = result["command"].split(".")[1].split()[0]
                lang = "Python"
            else:
                strategy = result["command"].split("/")[-1].split()[0]
                lang = "Rust"

            mean = result["mean"]
            stddev = result["stddev"]
            median = result["median"]
            min_time = result["min"]
            max_time = result["max"]
            df = results.append(
                {
                    "Strategy": strategy,
                    "Language": lang,
                    "Mean": mean,
                    "StdDev": stddev,
                    "Median": median,
                    "Min": min_time,
                    "Max": max_time,
                }
            )

df = pd.DataFrame(results)
df.sort_values(by="Mean", inplace=True)

df = df.round(2)

# Convert DataFrame to Markdown (requires tabulate)
print(df.to_markdown(index=False))
