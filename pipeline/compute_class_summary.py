import rasterio
import numpy as np
import json
from config import PROCESSED_DIR


CLASS_NAMES = {
    1: "Forest",
    2: "Water",
    3: "Agriculture",
    4: "Barren",
    5: "Built-up"
}

PIXEL_AREA_KM2 = 0.0009


def compute_class_summary():
    pred_dir = PROCESSED_DIR / "predictions"
    out_dir = PROCESSED_DIR / "stats"
    out_dir.mkdir(parents=True, exist_ok=True)

    lulc_2018 = pred_dir / "lulc_2018.tif"
    lulc_2023 = pred_dir / "lulc_2023.tif"
    out_json = out_dir / "summary_stats.json"

    with rasterio.open(lulc_2018) as src18, rasterio.open(lulc_2023) as src23:
        a = src18.read(1)
        b = src23.read(1)

    summary = {}

    for cls, name in CLASS_NAMES.items():
        area_2018 = np.sum(a == cls) * PIXEL_AREA_KM2
        area_2023 = np.sum(b == cls) * PIXEL_AREA_KM2

        net_change = area_2023 - area_2018
        pct_change = (
            (net_change / area_2018) * 100
            if area_2018 > 0 else None
        )

        summary[name] = {
            "area_2018_sq_km": round(area_2018, 3),
            "area_2023_sq_km": round(area_2023, 3),
            "net_change_sq_km": round(net_change, 3),
            "percent_change": round(pct_change, 2) if pct_change is not None else None
        }

    with open(out_json, "w") as f:
        json.dump(summary, f, indent=2)

    print("Class summary saved:", out_json)


if __name__ == "__main__":
    compute_class_summary()
