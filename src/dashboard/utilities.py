"""Module with utility functions that are reused frequently."""
from datetime import timedelta


def set_classname(class_str: str, class_to_set: str, set_: bool) -> str:
    """Add or remove a specific classname from a classname string.

    Args:
        class_str (str): the classname string to operate on.
        class_to_set (str): the class to add or remove.
        set_ (bool): indicating if the class should be added or removed.

    Returns:
        A string with the class added or removed.
    """
    if len(class_str) == 0 and set_:
        return class_to_set

    if len(class_to_set) == 0:
        return class_str

    if class_to_set in class_str and not set_:
        return class_str.replace(class_to_set, "").strip()
    elif class_to_set not in class_str and set_:
        return f"{class_str} {class_to_set}"
    else:
        return class_str


def toggle_classname(class_str: str, class_to_toggle: str) -> str:
    """Add or remove a specific classname from a classname string.

    Args:
        class_str (str): the classname string to operate on.
        class_to_toggle (str): the class to add or remove.

    Returns:
        A string with the class added or removed.
    """
    if len(class_str) == 0:
        return class_to_toggle

    if len(class_to_toggle) == 0:
        return class_str

    if class_to_toggle in class_str:
        return set_classname(class_str, class_to_toggle, False)
    else:
        return set_classname(class_str, class_to_toggle, True)


def pluralize(unit: str, amount: int) -> str:
    """Pluralize a unit if the amount is greater than 1.

    Args:
        unit (str): The unit.
        amount (int): The amount.

    Returns:
        str: The unit with s appended
        if amount is greater than 1,
        otherwise the unit.
    """
    if amount == 1:
        return unit

    return f"{unit}s"


def singularize(article: str, amount: int) -> str:
    """Singularize an amount if it is equal to one.

    Args:
        article (str): The indefinite
        article of an amount of something.
        E.g. "A" or "An" in english.
        amount (int): An amount.

    Returns:
        str: `article` if the amount
        is equal to 1, otherwise
        a string of amount.
    """
    if amount == 1:
        return article

    return str(amount)


def to_human_time_delta(duration: timedelta, abbreviated: bool = False) -> str:
    """Convert a duration of time to a human readable form.

    Args:
        delta (timedelta): A duration of time.

    Returns:
        str: A human readable form of
        the delta.
    """
    units: list[tuple[str, str, str, timedelta]] = [
        ("A", "year", "y", timedelta(days=365)),
        ("A", "month", "mo", timedelta(weeks=4)),
        ("A", "week", "w", timedelta(weeks=1)),
        ("A", "day", "d", timedelta(days=1)),
        ("An", "hour", "h", timedelta(hours=1)),
        ("A", "minute", "m", timedelta(minutes=1)),
        ("A", "second", "s", timedelta(seconds=1)),
    ]
    for article, unit, unit_abbr, unit_delta in units:
        duration_in_unit = duration // unit_delta
        if duration_in_unit == 0:
            continue

        if abbreviated:
            return f"{duration_in_unit} {unit_abbr}"

        return f"{singularize(article, duration_in_unit)} {pluralize(unit, duration_in_unit)} ago"

    return "Just now"
