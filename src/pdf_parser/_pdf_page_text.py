import logging
import re
from enum import Enum

from . import _event_participants

KEYWORDS = {"лет", "младше", "старше"} | _event_participants.MALE_KEYWORDS | _event_participants.FEMALE_KEYWORDS
DATE_REGEX = re.compile(r"^\d{2}\.\d{2}\.\d{4}$")
ID_LENGTH = 16


class State(Enum):
    SPORT_TEAM_ID = 0
    TITLE = 1
    PARTICIPANTS_START = 2
    CATEGORIES_START = 3
    END = 4
    COUNTRY = 5
    CITY_PARTICIPANTS_COUNT = 6


logger = logging.getLogger(__name__)

sport = team = ""


def parse(text: str) -> list[dict]:
    global sport, team
    data = []
    state = State.SPORT_TEAM_ID
    id_ = title = start = end = country = city = participants = categories = ""

    def reset_variables() -> None:
        nonlocal id_, title, start, end, participants_count, country, city, participants, categories
        id_ = title = start = end = participants_count = country = city = participants = categories = ""

    for line in text.split("\n"):
        if not line:
            continue
        match state:
            case State.SPORT_TEAM_ID:
                if line.isdigit() and len(line) == ID_LENGTH:
                    id_ = int(line)
                    state = State.TITLE
                elif not line.isdigit():
                    if line.isupper():
                        sport = line
                    elif not line.startswith("Стр."):
                        team = line
            case State.TITLE:
                if line[0].islower():
                    participants = line
                    state = State.PARTICIPANTS_START
                else:
                    title += " " + line
            case State.PARTICIPANTS_START:
                if line[0].isupper():
                    categories = line
                    state = State.CATEGORIES_START
                elif any(word in line for word in KEYWORDS):
                    participants += " " + line
                elif DATE_REGEX.match(line):
                    start = line
                    state = State.END
                else:
                    categories = line
                    state = State.CATEGORIES_START
            case State.CATEGORIES_START:
                if DATE_REGEX.match(line):
                    start = line
                    state = State.END
                else:
                    categories += " " + line
            case State.END:
                end = line
                state = State.COUNTRY
            case State.COUNTRY:
                country = line
                state = State.CITY_PARTICIPANTS_COUNT
            case State.CITY_PARTICIPANTS_COUNT:
                if not line.isdigit():
                    city += " " + line
                else:
                    participants_count = int(line)
                    state = State.SPORT_TEAM_ID

                    data.append(
                        {
                            "sport": sport,
                            "team": team,
                            "id": id_,
                            "title": title.lstrip(),
                            "categories": categories.split(", ") if categories else [],
                            "participants": participants,
                            **_event_participants.parse(participants),
                            "country": country,
                            "city": city.lstrip(),
                            "start": start,
                            "end": end,
                            "participants_count": participants_count,
                        },
                    )
                    reset_variables()

    return data
