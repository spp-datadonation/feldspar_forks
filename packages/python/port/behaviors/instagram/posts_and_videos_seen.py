from port.extraction_helpers import (
    epoch_to_date,
    extract_multiple_files_from_zip,
    extract_username_from_label_values,
)
import pandas as pd

patterns = ["posts_viewed", "videos_watched"]

title = {
    "de": "Gesehene Beiträge und Videos von Accounts [pro Tag]",
}


def extract_posts_and_videos_seen(zip_file_path):
    """Extract posts/videos seen per day per account from ZIP file."""
    combined_data = extract_multiple_files_from_zip(zip_file_path, patterns)

    if combined_data is None:
        return None

    records = []

    for source_key in ["posts_viewed", "videos_watched"]:
        data = combined_data.get(source_key, [])
        if isinstance(data, list):
            for entry in data:
                if "timestamp" in entry and "label_values" in entry:
                    date = epoch_to_date(entry["timestamp"])
                    account = extract_username_from_label_values(entry["label_values"])
                    records.append((date, account))

    if not records:
        return None

    df = pd.DataFrame(records, columns=["Datum", "Account"])
    aggregated = df.groupby(["Datum", "Account"]).size().reset_index(name="Anzahl")
    aggregated = aggregated.sort_values(by="Datum").reset_index(drop=True)

    return aggregated
