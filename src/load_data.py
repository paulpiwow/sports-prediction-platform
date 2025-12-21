from pathlib import Path
import pandas as pd

# Get project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Build path safely
RESULTS_PATH = BASE_DIR / "data" / "raw" / "results.csv"

df = pd.read_csv(RESULTS_PATH)

print(df.head())
print(df.info())