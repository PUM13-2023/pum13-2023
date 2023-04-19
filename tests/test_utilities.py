"""Tests for the utilities module."""
import pytest

from dashboard.utilities import set_classname, toggle_classname

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
