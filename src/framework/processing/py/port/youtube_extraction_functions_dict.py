import port.youtube_extraction_functions as ef

# defines which extraction functions are used and what titles are displayed
# patterns are the exact filenames found in the YouTube export

extraction_dict = {
    "watch_history": {
        "extraction_function": ef.extract_watch_history,
        "patterns": ["Wiedergabeverlauf.json", "watch-history.json"],
        "title": {
            "en": "How many videos have you watched? [per day]",
            "de": "Wie oft haben Sie sich Videos angesehen? [pro Tag]",
            "nl": "Hoe vaak heb je video's bekeken? [per dag]",
        },
    },
    "comments": {
        "extraction_function": ef.extract_comments,
        "patterns": ["Kommentare.csv", "comments.csv"],
        "title": {
            "en": "How many comments have you made? [per day]",
            "de": "Wie oft haben Sie Kommentare geschrieben? [pro Tag]",
            "nl": "Hoe vaak heb je commentaar gegeven? [per dag]",
        },
    },
    "subscriptions": {
        "extraction_function": ef.extract_subscriptions,
        "patterns": ["Abos.csv", "subscriptions.csv"],
        "title": {
            "en": "Which channels are you subscribed to?",
            "de": "Welche Kanäle haben Sie abonniert?",
            "nl": "Op welke kanalen ben je geabonneerd?",
        },
    },
    "search_history": {
        "extraction_function": ef.extract_search_history,
        "patterns": ["Suchverlauf.json", "search-history.json"],
        "title": {
            "en": "How many searches have you performed? [per day]",
            "de": "Wie oft haben Sie nach etwas gesucht? [pro Tag]",
            "nl": "Hoe vaak heb je naar iets gezocht? [per dag]",
        },
    },
}
