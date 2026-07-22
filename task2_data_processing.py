# TrendPulse Task 2 - cleaning up the raw json from task 1 and saving as csv
# steps: load json into a dataframe, clean it (dupes, nulls, types,
# low scores, whitespace), then save it and print a per-category summary

import pandas as pd
import glob
import os

DATA_FOLDER = "data"
MIN_SCORE = 5


def find_latest_json():
    # task 1 saves files like data/trends_20260722.json, and the date
    # changes every day, so instead of hardcoding a filename i just grab
    # whichever trends_*.json is newest in the data folder
    json_files = glob.glob(os.path.join(DATA_FOLDER, "trends_*.json"))
    if not json_files:
        return None
    # pick the most recently modified one
    return max(json_files, key=os.path.getmtime)


def main():
    json_path = find_latest_json()
    if json_path is None:
        print("no trends_*.json file found in data/ - run task 1 first")
        return

    # --- step 1: load ---
    df = pd.read_json(json_path)
    print(f"Loaded {len(df)} stories from {json_path}")

    # --- step 2: clean ---

    # duplicates - same post_id showing up more than once, just keep the first
    df = df.drop_duplicates(subset="post_id")
    print(f"After removing duplicates: {len(df)}")

    # missing values - if post_id, title or score is missing the row
    # isn't really usable, so drop those
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # data types - score and num_comments should be whole numbers, not
    # floats or strings, so force them to int after the nulls are gone.
    # post_id also turns into a float when there were nulls in the
    # column earlier, so converting that back to int too
    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].astype(int)
    df["post_id"] = df["post_id"].astype(int)

    # low quality - anything under 5 score isn't really "trending"
    df = df[df["score"] >= MIN_SCORE]
    print(f"After removing low scores: {len(df)}")

    # whitespace - titles sometimes have extra spaces at the start/end
    df["title"] = df["title"].str.strip()

    # --- step 3: save ---
    os.makedirs(DATA_FOLDER, exist_ok=True)
    output_path = os.path.join(DATA_FOLDER, "trends_clean.csv")
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} rows to {output_path}")

    # quick summary of how many stories ended up in each category
    print("\nStories per category:")
    counts = df["category"].value_counts()
    for category, count in counts.items():
        print(f"  {category:<15} {count}")


if __name__ == "__main__":
    main()