from port.extraction_helpers import epoch_to_date, extract_single_file_from_zip
import pandas as pd

patterns = ["post_comments_1"]

title = {
    "de": "Kommentare zu Beiträgen und Reels [pro Tag]",
}


def extract_comments(zip_file_path):
    """Extract comments per day per account from ZIP file."""
    data = extract_single_file_from_zip(zip_file_path, patterns[0])

    if data is None:
        return None

    # Handle single dict (one comment) vs list
    if isinstance(data, dict):
        data = [data]

    records = []
    for entry in data:
        try:
            smd = entry.get("string_map_data", {})
            timestamp = smd.get("Time", {}).get("timestamp")
            account = smd.get("Media Owner", {}).get("value", "Unbekannt")
            if timestamp:
                date = epoch_to_date(timestamp)
                records.append((date, account))
        except Exception:
            continue

    if not records:
        return None

    df = pd.DataFrame(records, columns=["Datum", "Account"])
    aggregated = df.groupby(["Datum", "Account"]).size().reset_index(name="Anzahl")
    aggregated = aggregated.sort_values(by="Datum").reset_index(drop=True)

    return aggregated
