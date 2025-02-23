import re

from src.logger import get_logger

MIN_AGE, MAX_AGE = 0, 150
MALE_KEYWORDS = {"мальчики", "юноши", "юниоры", "мужчины"}
FEMALE_KEYWORDS = {"девочки", "девушки", "юниорки", "женщины"}
HYPHEN_REGEX = re.compile(r"\s*-\s*")

logger = get_logger(__name__)


def parse(source: str) -> dict[str, list[bool] | list[int]]:
    genders: list[bool] = [False, False]
    ages: list[tuple[int, int]] = []
    last_word = ""
    source = HYPHEN_REGEX.sub("-", source)

    try:
        for word in source.split():
            if any(keyword in word.lower() for keyword in MALE_KEYWORDS):
                genders[0] = True
            elif any(keyword in word.lower() for keyword in FEMALE_KEYWORDS):
                genders[1] = True
            elif word.isdigit():
                if last_word == "от":
                    ages.append((int(word), MAX_AGE))
                elif last_word == "до":
                    ages.append((MIN_AGE, int(word)))
            elif "-" in word:
                start, end = map(int, word.split("-"))
                ages.append((start, end))
            last_word = word
        if not ages:
            ages.append((MIN_AGE, MAX_AGE))
    except:  # noqa: E722
        logger.exception("Error when parsing the event participants")

    return {"ages": ages, "genders": genders}
