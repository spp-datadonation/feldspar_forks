from port.extraction_helpers import extract_csv_from_zip, parse_linkedin_datetime
import pandas as pd

patterns = ["Shares.csv"]

title = {
    "de": "Geteilte Beiträge [pro Tag]",
}


def extract_shares(zip_file_path):
    """Extract shared posts count per day from ZIP file."""
    df = extract_csv_from_zip(zip_file_path, "Shares.csv")

    if df is None:
        return None

    if "Date" not in df.columns:
        return None

    df["Datum"] = df["Date"].apply(parse_linkedin_datetime)

    aggregated = df.groupby("Datum").size().reset_index(name="Anzahl geteilter Beiträge")
    aggregated = aggregated.sort_values(by="Datum").reset_index(drop=True)

    return aggregated
