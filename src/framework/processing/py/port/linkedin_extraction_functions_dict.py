import port.linkedin_extraction_functions as ef

# defines which extraction functions are used and what titles are displayed
# patterns are the exact filenames found in the LinkedIn export

extraction_dict = {
    "connections": {
        "extraction_function": ef.extract_connections,
        "patterns": ["Connections.csv"],
        "title": {
            "en": "How many people have you connected with? [per day]",
            "de": "Mit wie vielen Personen haben Sie sich vernetzt? [pro Tag]",
            "nl": "Met hoeveel mensen heeft u zich verbonden? [per dag]",
        },
    },
    "comments": {
        "extraction_function": ef.extract_comments,
        "patterns": ["Comments.csv"],
        "title": {
            "en": "How often have you written comments? [per day]",
            "de": "Wie oft haben Sie Kommentare geschrieben? [pro Tag]",
            "nl": "Hoe vaak heeft u commentaar geschreven? [per dag]",
        },
    },
    "reactions": {
        "extraction_function": ef.extract_reactions,
        "patterns": ["Reactions.csv"],
        "title": {
            "en": "How have you reacted, e.g. to posts, and how often? [per day]",
            "de": "Wie haben Sie, bspw. auf Beiträge, reagiert und wie oft? [pro Tag]",
            "nl": "Hoe heeft u gereageerd, bijv. op berichten, en hoe vaak? [per dag]",
        },
    },
    "shares": {
        "extraction_function": ef.extract_shares,
        "patterns": ["Shares.csv"],
        "title": {
            "en": "How often have you shared posts? [per day]",
            "de": "Wie oft haben Sie Beiträge geteilt? [pro Tag]",
            "nl": "Hoe vaak heeft u berichten gedeeld? [per dag]",
        },
    },
    "messages": {
        "extraction_function": ef.extract_messages,
        "patterns": ["messages.csv"],
        "title": {
            "en": "How often have you exchanged messages? [per day]",
            "de": "Wie oft haben Sie Nachrichten ausgetauscht? [pro Tag]",
            "nl": "Hoe vaak heeft u berichten uitgewisseld? [per dag]",
        },
    },
    "search_queries": {
        "extraction_function": ef.extract_search_queries,
        "patterns": ["SearchQueries.csv"],
        "title": {
            "en": "How often have you searched for something? [per day]",
            "de": "Wie oft haben Sie nach etwas gesucht? [pro Tag]",
            "nl": "Hoe vaak heeft u naar iets gezocht? [per dag]",
        },
    },
    "interests": {
        "extraction_function": ef.extract_interests,
        "patterns": ["Ad_Targeting.csv"],
        "title": {
            "en": "What interests has LinkedIn inferred about you?",
            "de": "Welche Interessen hat LinkedIn über Sie abgeleitet?",
            "nl": "Welke interesses heeft LinkedIn over u afgeleid?",
        },
    },
    "member_follows": {
        "extraction_function": ef.extract_member_follows,
        "patterns": ["Member_Follows.csv"],
        "title": {
            "en": "How many LinkedIn members have you followed or unfollowed? [per day]",
            "de": "Wie vielen LinkedIn-Mitgliedern sind Sie gefolgt bzw. nicht mehr gefolgt? [pro Tag]",
            "nl": "Hoeveel LinkedIn-leden bent u gaan volgen of niet meer gaan volgen? [per dag]",
        },
    },
    "profile": {
        "extraction_function": ef.extract_profile,
        "patterns": ["Profile.csv"],
        "title": {
            "en": "What information is included in your profile?",
            "de": "Welche Informationen sind in Ihrem Profil enthalten?",
            "nl": "Welke informatie is in uw profiel opgenomen?",
        },
    },
    "positions": {
        "extraction_function": ef.extract_positions,
        "patterns": ["Positions.csv"],
        "title": {
            "en": "What details are included in your job positions?",
            "de": "Welche Details sind zu Ihren beruflichen Positionen enthalten?",
            "nl": "Welke details zijn in uw werkposities opgenomen?",
        },
    },
    "device_usage": {
        "extraction_function": ef.extract_device_usage,
        "patterns": ["Logins.csv"],
        "title": {
            "en": "Which browsers/devices have you used to access LinkedIn?",
            "de": "Mit welchen Browsern/Geräten haben Sie auf LinkedIn zugegriffen?",
            "nl": "Met welke browsers/apparaten heeft u toegang gekregen tot LinkedIn?",
        },
    },
    "saved_jobs": {
        "extraction_function": ef.extract_saved_jobs,
        "patterns": ["Saved Jobs.csv"],
        "title": {
            "en": "How often have you saved jobs? [per day]",
            "de": "Wie oft haben Sie Jobs gespeichert? [pro Tag]",
            "nl": "Hoe vaak heeft u vacatures opgeslagen? [per dag]",
        },
    },
}
