"""Module with utility functions that are reused frequently."""


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
