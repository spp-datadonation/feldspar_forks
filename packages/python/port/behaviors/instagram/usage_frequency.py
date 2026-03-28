from port.extraction_helpers import epoch_to_date, extract_multiple_files_from_zip
import pandas as pd
from datetime import datetime, timezone, timedelta

patterns = ["posts_viewed", "videos_watched"]

title = {
    "de": "Wie oft waren Sie auf Instagram? [Besuche pro Tag]",
}


def extract_usage_frequency(zip_file_path):
    """
    Calculate Instagram sessions per day.
    A session continues if the time between views is less than 300 seconds.
    Sessions reset at midnight.
    """
    combined_data = extract_multiple_files_from_zip(zip_file_path, patterns)

    if combined_data is None:
        return None

    SESSION_BREAK_THRESHOLD = 300  # seconds

    # NEW format: flat lists with entry["timestamp"] directly
    posts_data = combined_data.get("posts_viewed", [])
    videos_data = combined_data.get("videos_watched", [])

    post_timestamps = []
    if isinstance(posts_data, list):
        post_timestamps = [entry["timestamp"] for entry in posts_data if "timestamp" in entry]
    elif isinstance(posts_data, dict):
        # Fallback for old format
        for key in posts_data:
            if isinstance(posts_data[key], list):
                post_timestamps = [
                    entry.get("string_map_data", {}).get("Time", {}).get("timestamp")
                    for entry in posts_data[key]
                    if entry.get("string_map_data", {}).get("Time", {}).get("timestamp")
                ]
                break

    video_timestamps = []
    if isinstance(videos_data, list):
        video_timestamps = [entry["timestamp"] for entry in videos_data if "timestamp" in entry]
    elif isinstance(videos_data, dict):
        for key in videos_data:
            if isinstance(videos_data[key], list):
                video_timestamps = [
                    entry.get("string_map_data", {}).get("Time", {}).get("timestamp")
                    for entry in videos_data[key]
                    if entry.get("string_map_data", {}).get("Time", {}).get("timestamp")
                ]
                break

    all_timestamps = sorted(post_timestamps + video_timestamps)

    if not all_timestamps:
        return None

    daily_session_count = {}
    daily_first_timestamp = {}
    last_time = None
    current_day = None

    for ts in all_timestamps:
        current_time = datetime.fromtimestamp(ts, tz=timezone(timedelta(hours=1)))
        new_day = current_time.date()

        if new_day not in daily_session_count:
            daily_session_count[new_day] = 0
            daily_first_timestamp[new_day] = ts

        start_new_session = False

        if last_time is None:
            start_new_session = True
        elif new_day != current_day:
            start_new_session = True
        elif (current_time - last_time).total_seconds() > SESSION_BREAK_THRESHOLD:
            start_new_session = True

        if start_new_session:
            daily_session_count[new_day] += 1

        last_time = current_time
        current_day = new_day

    dates = [epoch_to_date(daily_first_timestamp[d]) for d in daily_session_count.keys()]
    session_counts = list(daily_session_count.values())

    result_df = pd.DataFrame({"Datum": dates, "Anzahl": session_counts})
    result_df = result_df.sort_values(by="Datum").reset_index(drop=True)

    return result_df
