from fastapi import APIRouter
import json
from pathlib import Path

router = APIRouter()

DATA_DIR = Path("data/processed/stats")

@router.get("/summary")
def summary():
    with open(DATA_DIR / "summary_stats.json") as f:
        return json.load(f)

@router.get("/transition-matrix")
def transition_matrix():
    with open(DATA_DIR / "transition_matrix.json") as f:
        return json.load(f)
