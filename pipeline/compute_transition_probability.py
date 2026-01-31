import rasterio
import numpy as np
from config import PROCESSED_DIR


def compute_transition_probability():
    pred_dir = PROCESSED_DIR / "predictions"
    out_dir = PROCESSED_DIR / "change"
    out_dir.mkdir(parents=True, exist_ok=True)

    conf_2018 = pred_dir / "confidence_2018.tif"
    conf_2023 = pred_dir / "confidence_2023.tif"
    out_path = out_dir / "transition_probability.tif"

    with rasterio.open(conf_2018) as src18, rasterio.open(conf_2023) as src23:
        p18 = src18.read(1).astype(np.float32)
        p23 = src23.read(1).astype(np.float32)

        meta = src18.meta.copy()
        meta.update(dtype="float32", count=1, nodata=0.0)

        prob = np.zeros_like(p18, dtype=np.float32)
        valid = (p18 > 0) & (p23 > 0)
        prob[valid] = p18[valid] * p23[valid]

        with rasterio.open(out_path, "w", **meta) as dst:
            dst.write(prob, 1)

    print("Transition probability map saved:", out_path)


if __name__ == "__main__":
    compute_transition_probability()
