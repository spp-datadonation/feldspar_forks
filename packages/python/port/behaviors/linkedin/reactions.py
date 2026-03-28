from port.extraction_helpers import extract_csv_from_zip, parse_linkedin_datetime
import pandas as pd

patterns = ["Reactions.csv"]

title = {
    "de": "Reaktionen auf Inhalte [pro Tag]",
}

TYPE_MAPPING = {
    "LIKE": "Like",
    "PRAISE": "Celebrate",
    "EMPATHY": "Love",
    "INTEREST": "Insightful",
    "ENTERTAINMENT": "Funny",
    "APPRECIATION": "Support",
}


def extract_reactions(zip_file_path):
    """Extract reactions per day by type from ZIP file."""
    df = extract_csv_from_zip(zip_file_path, "Reactions.csv")

    if df is None:
        return None

    if "Date" not in df.columns or "Type" not in df.columns:
        return None

    df["Datum"] = df["Date"].apply(parse_linkedin_datetime)
    df["Typ"] = df["Type"].map(lambda t: TYPE_MAPPING.get(str(t).strip(), str(t).strip()))

    aggregated = (
        df.groupby(["Datum", "Typ"])
        .size()
        .reset_index(name="Anzahl der Reaktionen auf Inhalte")
    )
    aggregated = aggregated.sort_values(by="Datum").reset_index(drop=True)

    return aggregated
