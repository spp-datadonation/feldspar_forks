import port.instagram_extraction_functions as ef

# defines which extraction functions are used and what titles are displayed
# patterns are names of files or paths to that file if filename in path (like in personal_information/personal_information)

extraction_dict = {
    "time_spent": {
        "extraction_function": ef.extract_time_spent,
        "patterns": [
            "posts_viewed",
            "videos_watched",
        ],  # This function requires both files
        "title": {
            "en": "How much time did you spend on Instagram? [seconds per day]",
            "de": "Wie viel Zeit haben Sie auf Instagram verbracht? [Sekunden pro Tag]",
            "nl": "Hoeveel tijd heb je op Instagram doorgebracht? [seconden per dag]",
        },
    },
    "ads_seen": {
        "extraction_function": ef.extract_ads_seen,
        "patterns": ["ads_viewed"],
        "title": {
            "en": "How often did you see ads? [per day]",
            "de": "Wie oft haben Sie Werbung angesehen? [pro Tag]",
            "nl": "Hoe vaak heb je advertenties gezien? [per dag]",
        },
    },
    "ads_clicked": {
        "extraction_function": ef.extract_ads_clicked,
        "patterns": ["ads_clicked"],
        "title": {
            "en": "On how many ads did you click? [per day]",
            "de": "Wie oft haben Sie Werbung angeklickt? [pro Tag]",
            "nl": "Hoeveel productnamen (advertenties) heb je aangeklikt? [per dag]",
        },
    },
    "recently_viewed_items": {
        "extraction_function": ef.extract_recently_viewed_items,
        "patterns": ["recently_viewed_items"],
        "title": {
            "en": "Which shopping items have you recently viewed?",
            "de": "Welche Einkaufsartikel haben Sie sich kürzlich angesehen?",
            "nl": "Welke winkelartikelen heb je onlangs bekeken?",
        },
    },
    "combined_views": {
        "extraction_function": ef.extract_combined_views,
        "patterns": ["posts_viewed", "videos_watched"],
        "title": {
            "en": "How often did you view Instagram content? [per day]",
            "de": "Wie oft haben Sie Posts und Videos angesehen? [pro Tag]",
            "nl": "Hoe vaak heb je Instagram-inhoud bekeken? [per dag]",
        },
    },
    "combined_blocks": {
        "extraction_function": ef.extract_combined_blocks,
        "patterns": ["blocked_accounts", "restricted_accounts"],
        "title": {
            "en": "How often did you block or restrict other profiles? [per day]",
            "de": "Wie oft haben Sie andere Profile blockiert und eingeschränkt? [pro Tag]",
            "nl": "Hoe vaak heb je andere profielen geblokkeerd of beperkt? [per dag]",
        },
    },
    "combined_comments": {
        "extraction_function": ef.extract_combined_comments,
        "patterns": ["post_comments_1", "reels_comments"],
        "title": {
            "en": "How often did you comment on Instagram content? [per day]",
            "de": "Wie oft haben Sie Posts und Reels kommentiert? [pro Tag]",
            "nl": "Hoe vaak heb je gereageerd op Instagram-inhoud? [per dag]",
        },
    },
    "combined_likes": {
        "extraction_function": ef.extract_combined_likes,
        "patterns": ["liked_posts", "story_likes", "liked_comments"],
        "title": {
            "en": "How often did you like Instagram content? [per day]",
            "de": "Wie oft haben Sie Posts, Stories oder Kommentare geliked? [pro Tag]",
            "nl": "Hoe vaak heb je Instagram-inhoud geliked? [per dag]",
        },
    },
    "combined_story_interactions": {
        "extraction_function": ef.extract_combined_story_interactions,
        "patterns": ["countdowns", "emoji_sliders", "polls", "questions", "quizzes"],
        "title": {
            "en": "How often did you interact with Stories? [per day]",
            "de": "Wie oft haben Sie mit Stories interagiert? [pro Tag]",
            "nl": "Hoe vaak heb je met Stories geïnteracteerd? [per dag]",
        },
    },
    "posts_created": {
        "extraction_function": ef.extract_posts_created,
        "patterns": ["posts_1"],
        "title": {
            "en": "How often did you post and did you include location information?  [per day]",
            "de": "Wie oft haben Sie Posts veröffentlicht und haben Sie Standortinformationen hinzugefügt? [pro Tag]",
            "nl": "Hoe vaak heb je gepost en heb je locatie-informatie toegevoegd? [per dag]",
        },
    },
    "stories_created": {
        "extraction_function": ef.extract_stories_created,
        "patterns": ["stories"],
        "title": {
            "en": "How often did you post stories and did you include location information? [per day]",
            "de": "Wie oft haben Sie Stories gepostet und haben Sie Standortinformationen hinzugefügt? [pro Tag]",
            "nl": "Hoe vaak heb je stories gepost en heb je locatie-informatie toegevoegd? [per dag]",
        },
    },
    "reels_created": {
        "extraction_function": ef.extract_reels_created,
        "patterns": ["content/reels"],
        "title": {
            "en": "How often did you post reels? [per day]",
            "de": "Wie oft haben Sie Reels gepostet? [pro Tag]",
            "nl": "Hoe vaak heb je reels gepost? [per dag]",
        },
    },
    "followers_new": {
        "extraction_function": ef.extract_followers_new,
        "patterns": ["followers_1"],
        "title": {
            "en": "How often did you gain new followers? [per day]",
            "de": "Wie oft haben Sie neue Follower? [pro Tag]",
            "nl": "Hoe vaak heb je nieuwe volgers gekregen? [per dag]",
        },
    },
    "search_history": {
        "extraction_function": ef.extract_search_history,
        "patterns": ["word_or_phrase_searches"],
        "title": {
            "en": "How often have you searched on Instagram? [per day]",
            "de": "Wie oft haben Sie nach etwas gesucht? [pro Tag]",
            "nl": "Hoe vaak heb je gezocht op Instagram? [per dag]",
        },
    },
    "messages": {
        "extraction_function": ef.extract_messages,
        "patterns": ["message_1.json"],
        "title": {
            "en": "How often have you sent messages on Instagram? [per day]",
            "de": "Wie oft haben Sie mit anderen Menschen auf Instagram geschrieben? [pro Tag]",
            "nl": "Hoe vaak heb je berichten gestuurd op Instagram? [per dag]",
        },
    },
    "contact_syncing": {
        "extraction_function": ef.extract_contact_syncing,
        "patterns": ["instagram_profile_information"],
        "title": {
            "en": "Have you enabled contact syncing?",
            "de": "Haben Sie die Kontaktsynchronisierung aktiviert?",
            "nl": "Heb je contact synchronisatie ingeschakeld?",
        },
    },
    "private_account": {
        "extraction_function": ef.extract_private_account,
        "patterns": ["personal_information/personal_information.json"],
        "title": {
            "en": "Do you have private (not public) account on Instagram?",
            "de": "Haben Sie ein privates (nicht öffentliches) Konto auf Instagram?",
            "nl": "Heb je een profielfoto, e-mail, telefoon, een privéaccount en gebruik je je echte naam?",
        },
    },
    "topic_interests": {
        "extraction_function": ef.extract_topic_interests,
        "patterns": ["your_topics"],
        "title": {
            "en": "What are your Topics inferred by Instagram?",
            "de": "Was sind Ihre, von Instagram abgeleiteten, Themen?",
            "nl": "Je onderwerpen afgeleid door Instagram?",
        },
    },
    "login_activity": {
        "extraction_function": ef.extract_login_activity,
        "patterns": ["login_activity"],
        "title": {
            "en": "When and with which user agent did you log in to Instagram?",
            "de": "Wann und mit welchem Gerät haben Sie sich bei Instagram angemeldet?",
            "nl": "Wanneer en met welke user-agent heb je ingelogd op Instagram?",
        },
    },
    "logout_activity": {
        "extraction_function": ef.extract_logout_activity,
        "patterns": ["logout_activity"],
        "title": {
            "en": "When and with which user agent did you log out of Instagram?",
            "de": "Wann und mit welchem Gerät haben Sie sich Instagram abgemeldet?",
            "nl": "Wanneer en met welke user agent heb je uitgelogd op Instagram?",
        },
    },
}
