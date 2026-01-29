import polars as pl
import os
import shutil

# Config
INPUT_FILE = "data/final.parquet"
OUTPUT_DIR = "data/fraud_data_chunks"
ROWS_PER_CHUNK = 1_000_000  # Adjust based on row size, targeting <50MB per file

def split_parquet():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    # Clean output dir
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    print(f"Reading {INPUT_FILE}...")
    df = pl.read_parquet(INPUT_FILE)
    total_rows = df.height
    print(f"Total rows: {total_rows:,}")

    # Split and save
    chunk_idx = 0
    for i in range(0, total_rows, ROWS_PER_CHUNK):
        chunk = df.slice(i, ROWS_PER_CHUNK)
        chunk_path = f"{OUTPUT_DIR}/part_{chunk_idx:03d}.parquet"
        chunk.write_parquet(chunk_path)
        print(f"Saved {chunk_path} ({chunk.height:,} rows)")
        chunk_idx += 1
    
    print("\n✅ Splitting complete! Push the 'data/fraud_data_chunks' folder to GitHub.")

if __name__ == "__main__":
    split_parquet()
