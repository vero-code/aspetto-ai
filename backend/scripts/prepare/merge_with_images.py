# backend/scripts/prepare/merge_with_images.py

import pandas as pd

VECTORS_CSV = "data/styles_with_vectors.csv"
IMAGES_CSV = "data/images.csv"
OUTPUT_CSV = "data/styles_final.csv"

def main():
    styles_df = pd.read_csv(VECTORS_CSV)
    images_df = pd.read_csv(IMAGES_CSV)

    images_df["id"] = images_df["filename"].str.replace(".jpg", "", regex=False).astype(int)
    merged_df = pd.merge(styles_df, images_df, on="id")

    merged_df.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Merged and saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
