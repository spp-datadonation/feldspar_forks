from port.extraction_helpers import (
    epoch_to_date,
    extract_multiple_files_from_zip,
    extract_username_from_label_values,
)
import pandas as pd

patterns = ["liked_posts", "liked_comments", "story_likes"]

title = {
    "de": "Likes von Inhalten von Accounts [pro Tag]",
}


def _extract_liked_posts(data):
    """liked_posts.json: NEW format flat list with label_values."""
    records = []
    if isinstance(data, list):
        for entry in data:
            if "timestamp" in entry and "label_values" in entry:
                date = epoch_to_date(entry["timestamp"])
                account = extract_username_from_label_values(entry["label_values"])
                records.append((date, account))
    return records


def _extract_liked_comments(data):
    """liked_comments.json: OLD format dict with likes_comment_likes key."""
    records = []
    items = []
    if isinstance(data, dict):
        items = data.get("likes_comment_likes", [])
    elif isinstance(data, list):
        items = data

    for entry in items:
        try:
            account = entry.get("title", "Unbekannt")
            timestamp = entry.get("string_list_data", [{}])[0].get("timestamp")
            if timestamp:
                date = epoch_to_date(timestamp)
                records.append((date, account))
        except Exception:
            continue
    return records


def _extract_story_likes(data):
    """story_likes.json: NEW format flat list with label_values."""
    records = []
    if isinstance(data, list):
        for entry in data:
            if "timestamp" in entry and "label_values" in entry:
                date = epoch_to_date(entry["timestamp"])
                account = extract_username_from_label_values(entry["label_values"])
                records.append((date, account))
    return records


def extract_likes(zip_file_path):
    """Extract likes per day per account from ZIP file (posts, comments, stories)."""
    combined_data = extract_multiple_files_from_zip(zip_file_path, patterns)

    if combined_data is None:
        return None

    records = []
    records.extend(_extract_liked_posts(combined_data.get("liked_posts", [])))
    records.extend(_extract_liked_comments(combined_data.get("liked_comments", {})))
    records.extend(_extract_story_likes(combined_data.get("story_likes", [])))

    if not records:
        return None

    df = pd.DataFrame(records, columns=["Datum", "Account"])
    aggregated = df.groupby(["Datum", "Account"]).size().reset_index(name="Anzahl")
    aggregated = aggregated.sort_values(by="Datum").reset_index(drop=True)

    return aggregated
