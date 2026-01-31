import rasterio
import numpy as np
import pandas as pd
from config import PROCESSED_DIR


CLASS_NAMES = {
    1: "Forest",
    2: "Water",
    3: "Agriculture",
    4: "Barren",
    5: "Built-up"
}

PIXEL_AREA_KM2 = 0.0009  # 30m x 30m


def compute_transition_stats():
    pred_dir = PROCESSED_DIR / "predictions"
    change_dir = PROCESSED_DIR / "change"
    out_dir = PROCESSED_DIR / "stats"
    out_dir.mkdir(parents=True, exist_ok=True)

    lulc_2018 = pred_dir / "lulc_2018.tif"
    lulc_2023 = pred_dir / "lulc_2023.tif"
    out_csv = out_dir / "transition_matrix.csv"

    with rasterio.open(lulc_2018) as src18, rasterio.open(lulc_2023) as src23:
        a = src18.read(1)
        b = src23.read(1)

    valid = (a > 0) & (b > 0)

    records = []

    for i in range(1, 6):
        for j in range(1, 6):
            count = np.sum((a == i) & (b == j) & valid)
            area_km2 = count * PIXEL_AREA_KM2
            records.append({
                "from_class": CLASS_NAMES[i],
                "to_class": CLASS_NAMES[j],
                "area_sq_km": round(area_km2, 3)
            })

    df = pd.DataFrame(records)

    # Add percentage column
    total_area = df["area_sq_km"].sum()
    df["percentage"] = round((df["area_sq_km"] / total_area) * 100, 2)

    df.to_csv(out_csv, index=False)
    print("Transition matrix saved:", out_csv)


if __name__ == "__main__":
    compute_transition_stats()
