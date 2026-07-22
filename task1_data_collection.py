# TrendPulse Task 1 - fetching trending stories from HackerNews
# basic idea: grab top 500 story ids, then for each of my 5 categories
# go through the ids and pick out ones whose title matches that category's
# keywords, keep 25 max per category, dump it all into a json file

import requests
import json
import os
import time
from datetime import datetime

HEADERS = {"User-Agent": "TrendPulse/1.0"}  # HN wants this in the request
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
NEW_STORIES_URL = "https://hacker-news.firebaseio.com/v0/newstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"
MAX_PER_CATEGORY = 25

# keeping all keywords lowercase so matching is easier later
CATEGORY_KEYWORDS = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"],
}


def get_category(title):
    # go through each category's keyword list and see if any word is
    # inside the title (case doesn't matter since i lowercase both sides)
    # note: "game" is in both sports & entertainment, so sports wins
    # since it comes first in the dict - not a big deal for this task
    if not title:
        return None
    title_lower = title.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in title_lower:
                return category
    return None


def fetch_top_story_ids(limit=500):
    # gets the top 500 ids like the assignment asks
    try:
        response = requests.get(TOP_STORIES_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()[:limit]
    except requests.exceptions.RequestException as e:
        print(f"couldn't get top story ids: {e}")
        return []


def fetch_new_story_ids(limit=500):
    # topstories alone didn't give enough matches for some categories
    # (sports/worldnews came up short), so pulling newstories too gives
    # a bigger, different pool of titles to search through
    try:
        response = requests.get(NEW_STORIES_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()[:limit]
    except requests.exceptions.RequestException as e:
        print(f"couldn't get new story ids: {e}")
        return []


def fetch_story_details(story_id):
    # gets the actual story info for one id
    try:
        response = requests.get(ITEM_URL.format(story_id), headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"story {story_id} failed, skipping: {e}")
        return None


def main():
    print("getting top story ids...")
    top_ids = fetch_top_story_ids(500)
    new_ids = fetch_new_story_ids(500)
    # combining both lists, removing duplicates, so i have a bigger pool
    # to find keyword matches in (some categories weren't hitting 25
    # with just topstories alone)
    story_ids = list(dict.fromkeys(top_ids + new_ids))
    print(f"got {len(story_ids)} ids to search through")

    # one bucket per category so i can cap each at 25
    collected = {category: [] for category in CATEGORY_KEYWORDS}

    # doing categories as the outer loop since the sleep needs to happen
    # once per category, not once per story
    for category in CATEGORY_KEYWORDS:
        print(f"\nchecking for {category} stories...")

        for story_id in story_ids:
            if len(collected[category]) >= MAX_PER_CATEGORY:
                break  # already have 25 for this one, no need to keep going

            story = fetch_story_details(story_id)
            if story is None:
                continue

            title = story.get("title")
            matched = get_category(title)

            if matched == category:
                collected[category].append({
                    "post_id": story.get("id"),
                    "title": title,
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", "unknown"),
                    "collected_at": datetime.now().isoformat(),
                })

        print(f"  found {len(collected[category])} for {category}")
        time.sleep(2)  # required pause after each category

    # combine everything into one list before saving
    all_stories = []
    for stories in collected.values():
        all_stories.extend(stories)

    os.makedirs("data", exist_ok=True)

    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{date_str}.json"

    with open(filename, "w") as f:
        json.dump(all_stories, f, indent=2)

    print(f"\nCollected {len(all_stories)} stories. Saved to {filename}")


if __name__ == "__main__":
    main()