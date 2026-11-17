# Download the BEAD Final Proposal files from BroadbandExpanded into data/raw.

from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_ROOT / "data" / "raw" / "bead_aggregator"

# Function that creates current day's folder
def make_run_folder():
    run_date = date.today().isoformat()
    run_folder = RAW_DIR / run_date
    run_folder.mkdir(parents=True, exist_ok=True)
    return run_folder


if __name__ == "__main__":
    folder = make_run_folder()
    print(f"Run folder ready: {folder}")

