"""Tests for the utilities module."""
from datetime import datetime, timedelta

import pytest

from dashboard.utilities import (
    pluralize,
    set_classname,
    singularize,
    to_human_time_delta,
    toggle_classname,
)

CLASSNAMEWITHCLASS1 = "class3 class2 class1"
CLASSNAMEWITHOUTCLASS1 = "class3 class2"
CLASS1 = "class1"
CLASS4 = "class4"


@pytest.mark.test_utilities
class TestSetClassname:
    """Collection of tests for the set_classname function."""

    def test_with_valid_input(self) -> None:
        """Test that it works with valid input."""
        assert CLASSNAMEWITHCLASS1 == set_classname(CLASSNAMEWITHOUTCLASS1, CLASS1, True)
        assert CLASSNAMEWITHOUTCLASS1 == set_classname(CLASSNAMEWITHCLASS1, CLASS1, False)

    def test_works_with_empty_parameters(self) -> None:
        """Test that it works with empty parameters."""
        assert set_classname("", CLASS1, True) == CLASS1
        assert set_classname(CLASSNAMEWITHCLASS1, "", True) == CLASSNAMEWITHCLASS1
        assert set_classname("", "", True) == ""

        assert set_classname("", CLASS1, False) == ""
        assert set_classname(CLASSNAMEWITHCLASS1, "", False) == CLASSNAMEWITHCLASS1
        assert set_classname("", "", False) == ""


@pytest.mark.test_utilities
class TestToggleClassname:
    """Collection of tests for the toggle_classname function."""

    def test_with_valid_input(self) -> None:
        """Test that it works with valid input."""
        assert CLASSNAMEWITHOUTCLASS1 == toggle_classname(CLASSNAMEWITHCLASS1, CLASS1)
        assert CLASSNAMEWITHCLASS1 == toggle_classname(CLASSNAMEWITHOUTCLASS1, CLASS1)

    def test_works_with_empty_parameters(self) -> None:
        """Test that it works with empty parameters."""
        assert toggle_classname("", CLASS1) == CLASS1
        assert toggle_classname(CLASSNAMEWITHCLASS1, "") == CLASSNAMEWITHCLASS1
        assert toggle_classname("", "") == ""


@pytest.mark.test_utilities
class TestPluralizeAndSingularize:
    """Tests for the pluralize and singularize functions."""

    def test_with_singular_input(self) -> None:
        """Test that the functions work with singular input."""
        assert pluralize("second", 1) == "second"
        assert singularize("a", 1) == "a"

    def test_with_plural_input(self) -> None:
        """Test that the functions work with plural input."""
        assert pluralize("second", 2) == "seconds"
        assert singularize("a", 2) == "2"

    def test_with_negative_input(self) -> None:
        """Test that the functions work with negative input."""
        assert pluralize("second", -1) == "seconds"
        assert singularize("an", -1) == "-1"


@pytest.mark.test_utilities
class TestToHumanTimeDelta:
    """Tests for the to_human_time_delta function."""

    def test_different_parameter_orders(self) -> None:
        """Test that the function has the same result."""
        before = datetime.now()
        after = datetime.now()
        delta1 = to_human_time_delta(before, after)
        delta2 = to_human_time_delta(after, before)
        assert delta1 == delta2

    def test_zero_duration(self) -> None:
        """Test that the function works with identical times."""
        now = datetime.now()
        assert to_human_time_delta(now, now) == "Just now"

    def test_a_time_delta(self) -> None:
        """Test that the function works with a time delta."""
        now = datetime.now()
        an_hour_ago = now - timedelta(hours=1)
        assert to_human_time_delta(now, an_hour_ago) == "An hour ago"
