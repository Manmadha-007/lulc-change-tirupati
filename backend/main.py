from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from backend.api.stats import router as stats_router
from backend.api.pixel import router as pixel_router

app = FastAPI(title="Tirupati LULC Change Dashboard")
app.include_router(stats_router, prefix="/api")
app.include_router(pixel_router, prefix="/api")

BASE_DIR = Path(__file__).resolve().parent.parent

# Serve tiles
app.mount(
    "/tiles",
    StaticFiles(directory=BASE_DIR / "backend" / "static" / "tiles"),
    name="tiles"
)

# Serve React app
app.mount(
    "/",
    StaticFiles(directory=BASE_DIR / "backend" / "static" / "app", html=True),
    name="app"
)
