import pandas as pd
import json
from pathlib import Path

csv_path = Path("data/processed/stats/transition_matrix.csv")
json_path = Path("data/processed/stats/transition_matrix.json")

# Read CSV (Long format: from_class, to_class, area, pct)
df = pd.read_csv(csv_path)

# Pivot to create a matrix (Row: from_class, Col: to_class, Value: area_sq_km)
pivot_df = df.pivot(index='from_class', columns='to_class', values='area_sq_km')

# Convert to dictionary {row: {col: value}}
matrix_dict = pivot_df.to_dict(orient='index')

with open(json_path, 'w') as f:
    json.dump(matrix_dict, f, indent=4)

print(f"Pivoted and converted {csv_path} to {json_path}")
