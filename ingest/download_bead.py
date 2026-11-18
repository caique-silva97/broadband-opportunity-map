"""Download the BEAD Final Proposal files from BroadbandExpanded into data/raw."""

from datetime import date
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_ROOT / "data" / "raw" / "bead_aggregator"

RELEASE = "20260827"
BASE_URL = "https://broadbandportal.netlify.app/files/data/bead"
TABLES = ["SUBGRANTEE", "PROJECT", "LOCATION", "NO_BEAD", "CAI"]

CHUNK_SIZE = 1024 * 1024 #1MB
TIMEOUT = (10, 120) # seconds: (connection, read)

# Function that creates current day's folder
def make_run_folder() -> Path:
    run_date = date.today().isoformat()
    run_folder = RAW_DIR / run_date
    run_folder.mkdir(parents=True, exist_ok=True)
    return run_folder


def file_url(table: str) -> str:
    return f"{BASE_URL}/{table}_{RELEASE}.parquet"


def download_file(url: str, destination: Path) -> int:
    bytes_written = 0
    with requests.get(url, stream=True, timeout=TIMEOUT) as response:
        response.raise_for_status()
        with open(destination, "wb") as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
                bytes_written += len(chunk)
    return bytes_written


if __name__ == "__main__":
    run_folder = make_run_folder()
    for table in [TABLES]:  # test with one file first; switch to TABLES once it works
        url = file_url(table)
        destination = run_folder / f"{table}_{RELEASE}.parquet"
        print(f"Downloading {url}")
        size = download_file(url, destination)
        print(f"  saved {size / 1_000_000:.1f} MB -> {destination.name}")

