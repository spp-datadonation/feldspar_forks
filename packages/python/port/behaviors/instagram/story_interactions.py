from port.extraction_helpers import epoch_to_date, extract_multiple_files_from_zip
import pandas as pd

patterns = ["countdowns", "polls"]

title = {
    "de": "Story-Interaktionen mit Inhalten von Accounts [pro Tag]",
}


def extract_story_interactions(zip_file_path):
    """Extract story interactions per day per account from ZIP file (countdowns, polls)."""
    combined_data = extract_multiple_files_from_zip(zip_file_path, patterns)

    if combined_data is None:
        return None

    records = []

    # countdowns.json: key story_activities_countdowns
    countdowns_data = combined_data.get("countdowns", {})
    if isinstance(countdowns_data, dict):
        for entry in countdowns_data.get("story_activities_countdowns", []):
            try:
                account = entry.get("title", "Unbekannt")
                timestamp = entry.get("string_list_data", [{}])[0].get("timestamp")
                if timestamp:
                    date = epoch_to_date(timestamp)
                    records.append((date, account))
            except Exception:
                continue

    # polls.json: key story_activities_polls
    polls_data = combined_data.get("polls", {})
    if isinstance(polls_data, dict):
        for entry in polls_data.get("story_activities_polls", []):
            try:
                account = entry.get("title", "Unbekannt")
                timestamp = entry.get("string_list_data", [{}])[0].get("timestamp")
                if timestamp:
                    date = epoch_to_date(timestamp)
                    records.append((date, account))
            except Exception:
                continue

    if not records:
        return None

    df = pd.DataFrame(records, columns=["Datum", "Account"])
    aggregated = (
        df.groupby(["Datum", "Account"])
        .size()
        .reset_index(name="Anzahl an Interaktionen")
    )
    aggregated = aggregated.sort_values(by="Datum").reset_index(drop=True)

    return aggregated
