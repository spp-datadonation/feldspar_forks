from port.extraction_helpers import extract_csv_from_zip, parse_linkedin_connection_date
import pandas as pd

patterns = ["Connections.csv"]

title = {
    "de": "Verbindungen und berufliche Position [pro Tag]",
}


def extract_connections(zip_file_path):
    """Extract connections per day with job positions from ZIP file."""
    df = extract_csv_from_zip(zip_file_path, "Connections.csv", skip_rows=3)

    if df is None:
        return None

    if "Connected On" not in df.columns:
        return None

    df["Datum"] = df["Connected On"].apply(parse_linkedin_connection_date)

    # Group by date: count connections and collect positions
    grouped = df.groupby("Datum").agg(
        Anzahl_der_Verbindungen=("Datum", "size"),
        Berufliche_Position=("Position", lambda x: "; ".join(
            [str(p) for p in x if pd.notna(p) and str(p).strip()]
        )),
    ).reset_index()

    grouped.columns = ["Datum", "Anzahl der Verbindungen", "Berufliche Position"]
    grouped = grouped.sort_values(by="Datum").reset_index(drop=True)

    return grouped
