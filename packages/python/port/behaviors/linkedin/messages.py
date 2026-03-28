from port.extraction_helpers import extract_csv_from_zip, parse_linkedin_datetime
import pandas as pd

patterns = ["messages.csv"]

title = {
    "de": "Nachrichten mit Verbindungen [pro Tag]",
}


def extract_messages(zip_file_path):
    """Extract message count per day from ZIP file."""
    df = extract_csv_from_zip(zip_file_path, "messages.csv")

    if df is None:
        return None

    if "DATE" not in df.columns:
        return None

    df["Datum"] = df["DATE"].apply(parse_linkedin_datetime)

    aggregated = df.groupby("Datum").size().reset_index(name="Anzahl der Nachrichten mit Verbindungen")
    aggregated = aggregated.sort_values(by="Datum").reset_index(drop=True)

    return aggregated
