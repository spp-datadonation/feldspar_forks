import importlib
import json
import zipfile

import pandas as pd

import port.api.props as props
from port.api.assets import *
from port.api.commands import CommandSystemDonate, CommandSystemExit, CommandUIRender

############################
# PLATFORM CONFIGURATION
############################

INSTAGRAM_BEHAVIORS = [
    "usage_frequency",
    "posts_and_videos_seen",
    "comments",
    "likes",
    "story_interactions",
    "following",
    "unfollowing",
]

LINKEDIN_BEHAVIORS = [
    "connections",
    "comments",
    "reactions",
    "shares",
    "messages",
]


############################
# MAIN FUNCTION INITIATING THE DONATION PROCESS
############################


def process(sessionId):
    key = "wp2-data-donation"

    # STEP 1: select the file
    data = None
    platform = None
    behaviors_to_extract = []

    while True:
        promptFile = prompt_file("application/zip")
        fileResult = yield render_data_submission_page([promptFile])

        if fileResult.__type__ == "PayloadFile":
            detected = detect_platform(fileResult.value)

            if detected == "instagram":
                platform = "instagram"
                behaviors_to_extract = INSTAGRAM_BEHAVIORS

            elif detected == "instagram_html":
                retry_result = yield render_data_submission_page(
                    retry_confirmation_instagram_html()
                )
                if retry_result.__type__ == "PayloadTrue":
                    continue
                else:
                    break

            elif detected == "linkedin_complete":
                platform = "linkedin"
                behaviors_to_extract = LINKEDIN_BEHAVIORS

            elif detected == "linkedin_basic":
                retry_result = yield render_data_submission_page(
                    retry_confirmation_linkedin_basic()
                )
                if retry_result.__type__ == "PayloadTrue":
                    continue
                else:
                    break

            else:  # unknown
                retry_result = yield render_data_submission_page(retry_confirmation())
                if retry_result.__type__ == "PayloadTrue":
                    continue
                else:
                    break

            # Extract behaviors
            extraction_result = []

            for index, behavior_name in enumerate(behaviors_to_extract, start=1):
                percentage = (index / len(behaviors_to_extract)) * 100
                message = f"Verarbeitet Datei: {behavior_name}"

                promptMessage = prompt_extraction_message(message, percentage)
                yield render_data_submission_page(promptMessage)

                result = extract_behavior(platform, behavior_name, fileResult.value)
                extraction_result.append(result)

            if len(extraction_result) > 0:
                data = extraction_result
                break
            else:
                retry_result = yield render_data_submission_page(retry_confirmation())
                if retry_result.__type__ == "PayloadTrue":
                    continue
                else:
                    break

    # STEP 2: ask for consent
    if data is not None:
        for prompt in prompt_consent(data, behaviors_to_extract, platform):
            result = yield prompt
            if result.__type__ == "PayloadJSON":
                data_submission_data = json.loads(result.value)
                yield donate(
                    f"{sessionId}-{key}-{platform}",
                    json.dumps(data_submission_data),
                )
            if result.__type__ == "PayloadFalse":
                value = json.dumps('{"status" : "data_donation declined"}')
                yield donate(f"{sessionId}-{key}-{platform}", value)


############################
# PLATFORM DETECTION
############################


def detect_platform(filename):
    """
    Auto-detect which platform a ZIP belongs to.
    Returns: "instagram" | "instagram_html" | "linkedin_complete" | "linkedin_basic" | "unknown"
    """
    try:
        with zipfile.ZipFile(filename, "r") as zip_ref:
            file_list = zip_ref.namelist()

            found_ads_information = False
            found_html = False
            found_linkedin_csv = False
            found_messages_csv = False

            for file_name in file_list:
                if "ads_information" in file_name:
                    found_ads_information = True
                if file_name.endswith(".html") or "start_here.html" in file_name:
                    found_html = True
                if file_name.endswith("Connections.csv") or file_name.endswith(
                    "Profile.csv"
                ):
                    found_linkedin_csv = True
                if file_name.endswith("messages.csv"):
                    found_messages_csv = True

            # Instagram detection
            if found_ads_information:
                if found_html:
                    return "instagram_html"
                return "instagram"

            # LinkedIn detection
            if found_linkedin_csv:
                # Check filename prefix for Complete vs Basic
                zip_name = getattr(filename, "name", str(filename))
                zip_name = zip_name.split("/")[-1]
                if zip_name.startswith("Basic_"):
                    return "linkedin_basic"
                return "linkedin_complete"

            return "unknown"

    except zipfile.BadZipFile:
        return "unknown"
    except Exception:
        return "unknown"


############################
# BEHAVIOR EXTRACTION
############################


def extract_behavior(platform, behavior_name, zip_file_path):
    """
    Extract data for a specific behavior using dynamic import.
    """
    try:
        behavior_module = importlib.import_module(
            f"port.behaviors.{platform}.{behavior_name}"
        )
        extraction_function = getattr(behavior_module, f"extract_{behavior_name}")

        try:
            result = extraction_function(zip_file_path)

            if result is None:
                return pd.DataFrame(
                    [f'(Datei "{behavior_name}" fehlt)'],
                    columns=["Keine Informationen"],
                )

            return result
        except Exception as e:
            return pd.DataFrame(
                [
                    f"Extrahierung fehlgeschlagen - {behavior_name}, {type(e).__name__}: {str(e)}"
                ],
                columns=[str(behavior_name)],
            )

    except ImportError as e:
        return pd.DataFrame(
            [f"Behavior '{behavior_name}' nicht gefunden: {str(e)}"],
            columns=["Fehler"],
        )
    except Exception as e:
        return pd.DataFrame(
            [f"Unerwarteter Fehler für '{behavior_name}': {str(e)}"],
            columns=["Fehler"],
        )


def get_behavior_info(platform, behavior_name):
    """Get metadata (title) for a specific behavior."""
    try:
        behavior_module = importlib.import_module(
            f"port.behaviors.{platform}.{behavior_name}"
        )
        return {
            "title": behavior_module.title,
        }
    except Exception:
        return None


############################
# CONSENT FORM
############################


def prompt_consent(data, behaviors_list, platform):
    """Consent form generator showing all extracted behavior tables."""
    description = props.PropsUIPromptText(
        text=props.Translatable(
            {
                "de": "Hier finden Sie nun alle Daten, die Sie an uns spenden können. Wenn Sie bestimmte Daten nicht spenden wollen, können Sie diese löschen oder anpassen."
            }
        )
    )

    table_data_list = []

    if data is not None:
        for i, behavior_name in enumerate(behaviors_list):
            df = data[i]

            behavior_info = get_behavior_info(platform, behavior_name)
            if behavior_info is None:
                behavior_title = {"de": f"Unbekanntes Verhalten: {behavior_name}"}
            else:
                behavior_title = {"de": behavior_info["title"]["de"]}

            # Clean DataFrame for JSON serialization
            df_cleaned = df.copy()
            for col in df_cleaned.columns:
                df_cleaned[col] = df_cleaned[col].fillna("").astype(str)

            table_data_list.append(
                {
                    "behavior_name": behavior_name,
                    "title": behavior_title,
                    "df": df_cleaned,
                }
            )

    # Create tables with sequential numbering
    table_list = []
    for i, table_data in enumerate(table_data_list, start=1):
        table = props.PropsUIPromptConsentFormTable(
            table_data["behavior_name"],
            i,
            props.Translatable(table_data["title"]),
            props.Translatable(table_data["title"]),
            table_data["df"],
        )
        table_list.append(table)

    # Build consent page
    consent_items = []
    consent_items.append(description)
    consent_items.extend(table_list)

    donation_buttons = props.PropsUIDataSubmissionButtons(
        donate_question=props.Translatable(
            {"de": "Möchten Sie die obenstehenden Daten spenden?"}
        ),
        donate_button=props.Translatable({"de": "Ja, spenden"}),
    )
    consent_items.append(donation_buttons)

    result = yield render_data_submission_page(
        [item for item in consent_items if item is not None]
    )

    return result


############################
# RENDER PAGES AND PROMPT MESSAGES
############################


def render_data_submission_page(body):
    header = props.PropsUIHeader(props.Translatable({"de": "Datenspende"}))
    body_items = [body] if not isinstance(body, list) else body
    page = props.PropsUIPageDataSubmission("Zip", header, body_items)
    return CommandUIRender(page)


def retry_confirmation():
    text = props.Translatable(
        {
            "de": "Leider können wir Ihre Datei nicht bearbeiten. Sind Sie sicher, dass Sie Ihre heruntergeladenen Instagram- oder LinkedIn-Daten ausgewählt haben?"
        }
    )
    ok = props.Translatable({"de": "Erneut versuchen"})
    return props.PropsUIPromptConfirm(text, ok)


def retry_confirmation_instagram_html():
    text = props.Translatable(
        {
            "de": 'Leider können wir Ihre Datei nicht verarbeiten. Es scheint so, dass Sie aus Versehen die HTML-Version Ihrer Instagram-Daten beantragt haben.\nBitte beantragen Sie erneut eine Datenspende bei Instagram und wählen Sie dabei "JSON" als Dateiformat aus (wie in der Anleitung beschrieben).'
        }
    )
    ok = props.Translatable({"de": "Erneut versuchen mit richtigen Daten"})
    return props.PropsUIPromptConfirm(text, ok)


def retry_confirmation_linkedin_basic():
    text = props.Translatable(
        {
            "de": "Sie haben das unvollständige Datenpaket hochgeladen, welches LinkedIn bereits nach wenigen Minuten gesendet hat. Für unsere Studie bitten wir Sie, uns das Datenpaket zu spenden, dass Sie normalerweise nach circa 24 Stunden erhalten.\nBitte laden Sie dieses vollständige Datenpaket hoch."
        }
    )
    ok = props.Translatable({"de": "Erneut versuchen mit richtigen Daten"})
    return props.PropsUIPromptConfirm(text, ok)


def prompt_file(extensions):
    description = props.Translatable(
        {
            "de": "Bitte wählen Sie Ihre heruntergeladene ZIP-Datei aus (Instagram oder LinkedIn)."
        }
    )
    return props.PropsUIPromptFileInput(description, extensions)


def prompt_extraction_message(message, percentage):
    description = props.Translatable(
        {
            "de": "Einen Moment bitte. Es werden nun Informationen aus der ausgewählten Datei extrahiert."
        }
    )
    return props.PropsUIPromptProgress(description, message, percentage)


def donate(key, json_string):
    return CommandSystemDonate(key, json_string)


def exit(code, info):
    return CommandSystemExit(code, info)
