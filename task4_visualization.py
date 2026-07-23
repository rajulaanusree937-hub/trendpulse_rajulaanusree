# TrendPulse Task 4 - turning the analysed csv into charts
# 3 separate charts (top stories, categories, score vs comments)
# plus a combined dashboard figure at the end

import pandas as pd
import matplotlib.pyplot as plt
import os

INPUT_PATH = "data/trends_analysed.csv"
OUTPUT_FOLDER = "outputs"


def shorten_title(title, max_len=50):
    # long titles make the bar chart labels unreadable, so cutting
    # anything over 50 chars and adding "..." to show it was trimmed
    if len(title) > max_len:
        return title[:max_len].rstrip() + "..."
    return title


def make_chart1_top_stories(df):
    # top 10 by score, horizontal bars so the titles are readable
    top10 = df.sort_values("score", ascending=False).head(10)
    # reversing so the highest score ends up at the top of the chart
    # (matplotlib draws bar charts bottom-up by default)
    top10 = top10.iloc[::-1]

    labels = [shorten_title(t) for t in top10["title"]]

    plt.figure(figsize=(10, 6))
    plt.barh(labels, top10["score"], color="steelblue")
    plt.xlabel("Score")
    plt.ylabel("Story Title")
    plt.title("Top 10 Stories by Score")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "chart1_top_stories.png"))
    plt.show()


def make_chart2_categories(df):
    # how many stories landed in each category
    counts = df["category"].value_counts()

    # giving each bar its own colour instead of one flat colour
    colors = ["steelblue", "orange", "green", "crimson", "purple"]

    plt.figure(figsize=(8, 6))
    plt.bar(counts.index, counts.values, color=colors[:len(counts)])
    plt.xlabel("Category")
    plt.ylabel("Number of Stories")
    plt.title("Stories per Category")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "chart2_categories.png"))
    plt.show()


def make_chart3_scatter(df):
    # splitting into popular vs not so i can plot them in 2 different
    # colours and add a proper legend
    popular = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]

    plt.figure(figsize=(8, 6))
    plt.scatter(popular["score"], popular["num_comments"], color="crimson", label="Popular")
    plt.scatter(not_popular["score"], not_popular["num_comments"], color="steelblue", label="Not Popular")
    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.title("Score vs Comments")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "chart3_scatter.png"))
    plt.show()


def make_dashboard(df):
    # same 3 charts again but laid out side by side in one figure
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # --- panel 1: top 10 stories ---
    top10 = df.sort_values("score", ascending=False).head(10).iloc[::-1]
    labels = [shorten_title(t, 30) for t in top10["title"]]  # shorter here, less room
    axes[0].barh(labels, top10["score"], color="steelblue")
    axes[0].set_xlabel("Score")
    axes[0].set_title("Top 10 Stories")

    # --- panel 2: categories ---
    counts = df["category"].value_counts()
    colors = ["steelblue", "orange", "green", "crimson", "purple"]
    axes[1].bar(counts.index, counts.values, color=colors[:len(counts)])
    axes[1].set_xlabel("Category")
    axes[1].set_ylabel("Number of Stories")
    axes[1].set_title("Stories per Category")
    axes[1].tick_params(axis="x", rotation=45)

    # --- panel 3: scatter ---
    popular = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]
    axes[2].scatter(popular["score"], popular["num_comments"], color="crimson", label="Popular")
    axes[2].scatter(not_popular["score"], not_popular["num_comments"], color="steelblue", label="Not Popular")
    axes[2].set_xlabel("Score")
    axes[2].set_ylabel("Number of Comments")
    axes[2].set_title("Score vs Comments")
    axes[2].legend()

    fig.suptitle("TrendPulse Dashboard", fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "dashboard.png"))
    plt.show()


def main():
    df = pd.read_csv(INPUT_PATH)

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    make_chart1_top_stories(df)
    make_chart2_categories(df)
    make_chart3_scatter(df)
    make_dashboard(df)

    print("All charts saved to the outputs/ folder:")
    print("  outputs/chart1_top_stories.png")
    print("  outputs/chart2_categories.png")
    print("  outputs/chart3_scatter.png")
    print("  outputs/dashboard.png")


if __name__ == "__main__":
    main()