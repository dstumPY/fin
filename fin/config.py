"""Project configuration."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# PATH
ROOT_FOLDER = Path(os.getenv("ROOT_FOLDER", default="/home/root/app"))
DATA_FOLDER = ROOT_FOLDER / "data"
ANALYSIS_FOLDER = DATA_FOLDER / "analysis"
DATA_PY4FI_2ND = DATA_FOLDER / "py4fi2nd/source"
DATA_API = DATA_FOLDER / "api"
