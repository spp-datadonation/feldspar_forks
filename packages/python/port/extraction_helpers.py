import pandas as pd
from datetime import datetime, timezone, timedelta
import zipfile
import json
from io import StringIO


def epoch_to_date(epoch_timestamp):
    """
    Convert epoch timestamp to DD-MM-YYYY string. Assumes UTC+1.
    """
    try:
        epoch_timestamp = int(epoch_timestamp)
        out = datetime.fromtimestamp(
            epoch_timestamp, tz=timezone(timedelta(hours=1))
        ).isoformat()
    except Exception:
        out = "01-01-1999"

    out = pd.to_datetime(out)
    return out.date().strftime("%d-%m-%Y")


def extract_single_file_from_zip(zip_file_path, pattern):
    """
    Extract a single JSON file from a ZIP based on pattern.
    Returns parsed JSON or None if not found.
    """
    try:
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            for file_name in zip_ref.namelist():
                if file_name.endswith(".json") and pattern in file_name:
                    try:
                        with zip_ref.open(file_name) as json_file:
                            return json.loads(json_file.read())
                    except Exception as e:
                        print(f"Error reading {pattern} file {file_name}: {e}")
            return None
    except Exception as e:
        print(f"Error extracting {pattern} from ZIP: {e}")
        return None


def extract_multiple_files_from_zip(zip_file_path, patterns, key_mapping=None):
    """
    Extract multiple JSON files from a ZIP based on patterns.
    Returns a dict mapping pattern names (or mapped keys) to parsed JSON.
    """
    try:
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            file_names = zip_ref.namelist()
            result = {}

            for pattern in patterns:
                pattern_data = None
                for file_name in file_names:
                    if file_name.endswith(".json") and pattern in file_name:
                        try:
                            with zip_ref.open(file_name) as json_file:
                                pattern_data = json.loads(json_file.read())
                                break
                        except Exception as e:
                            print(f"Error reading {pattern} file {file_name}: {e}")

                result_key = (
                    key_mapping.get(pattern, pattern) if key_mapping else pattern
                )
                result[result_key] = pattern_data or {}

            if any(data for data in result.values() if data):
                return result
            else:
                return None

    except Exception as e:
        print(f"Error extracting multiple files from ZIP: {e}")
        return None


def extract_csv_from_zip(zip_file_path, pattern, skip_rows=0):
    """
    Extract a CSV file from a ZIP based on pattern.
    Returns a DataFrame or None if not found.
    """
    try:
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            for file_name in zip_ref.namelist():
                # Match on filename part only to avoid partial matches
                basename = file_name.split("/")[-1]
                if basename == pattern:
                    try:
                        with zip_ref.open(file_name) as csv_file:
                            content = csv_file.read().decode("utf-8")
                            df = pd.read_csv(
                                StringIO(content), skiprows=skip_rows
                            )
                            if df.empty:
                                return None
                            return df
                    except Exception as e:
                        print(f"Error reading {pattern} file {file_name}: {e}")
            return None
    except Exception as e:
        print(f"Error extracting {pattern} from ZIP: {e}")
        return None


def extract_username_from_label_values(label_values):
    """
    Extract username from Instagram NEW DDP format label_values structure.
    Traverses label_values -> dict -> dict to find the username field.

    Language-agnostic approach: The Owner dict always contains exactly 3 fields
    in order: URL, display name, username. The label names for the latter two
    are translated (e.g. "Name"/"Nome", "Username"/"Benutzername"/"Nome utente"),
    so we simply take the last (3rd) field's value as the username.

    Returns username string or "Unbekannt".
    """
    try:
        for lv in label_values:
            if "dict" in lv:
                for owner_dict in lv["dict"]:
                    fields = owner_dict.get("dict", [])
                    if len(fields) >= 3:
                        value = fields[2].get("value", "")
                        return value if value else "Unbekannt"
    except Exception:
        pass
    return "Unbekannt"


def parse_linkedin_datetime(date_str):
    """
    Parse LinkedIn datetime string to DD-MM-YYYY.
    Handles "YYYY-MM-DD HH:MM:SS" and "YYYY-MM-DD HH:MM:SS UTC".
    """
    try:
        date_str = str(date_str).strip()
        if date_str.endswith(" UTC"):
            date_str = date_str[:-4]
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%d-%m-%Y")
    except Exception:
        return "01-01-1999"


def parse_linkedin_connection_date(date_str):
    """
    Parse LinkedIn connection date string to DD-MM-YYYY.
    Handles "DD Mon YYYY" format (e.g. "26 Nov 2025").
    """
    try:
        date_str = str(date_str).strip()
        dt = datetime.strptime(date_str, "%d %b %Y")
        return dt.strftime("%d-%m-%Y")
    except Exception:
        return "01-01-1999"
