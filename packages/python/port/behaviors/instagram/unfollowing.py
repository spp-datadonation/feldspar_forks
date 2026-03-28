from port.extraction_helpers import epoch_to_date, extract_single_file_from_zip
import pandas as pd

patterns = ["recently_unfollowed_profiles"]

title = {
    "de": "Entfolgte Accounts [pro Tag]",
}


def extract_unfollowing(zip_file_path):
    """Extract unfollowed accounts per day from ZIP file."""
    data = extract_single_file_from_zip(zip_file_path, patterns[0])

    if data is None:
        return None

    entries = []
    if isinstance(data, dict):
        entries = data.get("relationships_unfollowed_users", [])
    elif isinstance(data, list):
        entries = data

    records = []
    for entry in entries:
        try:
            sld = entry.get("string_list_data", [{}])[0]
            account = sld.get("value", "Unbekannt")
            timestamp = sld.get("timestamp")
            if timestamp:
                date = epoch_to_date(timestamp)
                records.append((date, account))
        except Exception:
            continue

    if not records:
        return None

    df = pd.DataFrame(records, columns=["Datum", "Account"])
    df = df.sort_values(by="Datum").reset_index(drop=True)

    return df
