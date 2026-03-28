from port.extraction_helpers import extract_csv_from_zip, parse_linkedin_datetime
import pandas as pd

patterns = ["Comments.csv"]

title = {
    "de": "Kommentierung von Inhalten [pro Tag]",
}


def extract_comments(zip_file_path):
    """Extract comment count per day from ZIP file."""
    df = extract_csv_from_zip(zip_file_path, "Comments.csv")

    if df is None:
        return None

    if "Date" not in df.columns:
        return None

    df["Datum"] = df["Date"].apply(parse_linkedin_datetime)

    aggregated = df.groupby("Datum").size().reset_index(name="Anzahl der Kommentare zu Inhalten")
    aggregated = aggregated.sort_values(by="Datum").reset_index(drop=True)

    return aggregated
