# TrendPulse Task 3 - digging into the clean csv from task 2
# loading it, checking out some numpy stats, adding 2 new columns
# (engagement + is_popular), then saving the result for task 4

import pandas as pd
import numpy as np

INPUT_PATH = "data/trends_clean.csv"
OUTPUT_PATH = "data/trends_analysed.csv"


def main():
    # --- step 1: load and explore ---
    df = pd.read_csv(INPUT_PATH)

    print(f"Loaded data: {df.shape}")
    print("\nFirst 5 rows:")
    print(df.head())

    avg_score = df["score"].mean()
    avg_comments = df["num_comments"].mean()
    print(f"\nAverage score   : {avg_score:.0f}")
    print(f"Average comments: {avg_comments:.0f}")

    # --- step 2: numpy stats ---
    # pulling the score column out as a numpy array so i can use
    # np.mean / np.median / np.std directly instead of the pandas versions
    scores = df["score"].to_numpy()

    mean_score = np.mean(scores)
    median_score = np.median(scores)
    std_score = np.std(scores)
    max_score = np.max(scores)
    min_score = np.min(scores)

    print("\n--- NumPy Stats ---")
    print(f"Mean score   : {mean_score:.0f}")
    print(f"Median score : {median_score:.0f}")
    print(f"Std deviation: {std_score:.0f}")
    print(f"Max score    : {max_score}")
    print(f"Min score    : {min_score}")

    # which category shows up the most - value_counts already sorts
    # descending so the first one is the winner
    category_counts = df["category"].value_counts()
    top_category = category_counts.index[0]
    top_category_count = category_counts.iloc[0]
    print(f"Most stories in: {top_category} ({top_category_count} stories)")

    # story with the most comments - idxmax gives me the row index of
    # the max value, then i can just look up that row
    most_commented_idx = df["num_comments"].idxmax()
    most_commented_row = df.loc[most_commented_idx]
    print(f'Most commented story: "{most_commented_row["title"]}" — {most_commented_row["num_comments"]} comments')

    # --- step 3: add new columns ---
    # engagement = comments per upvote, roughly. +1 on score so i never
    # divide by zero if a story somehow has 0 score
    df["engagement"] = df["num_comments"] / (df["score"] + 1)

    # is_popular = above the average score line
    df["is_popular"] = df["score"] > avg_score

    # --- step 4: save ---
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
    