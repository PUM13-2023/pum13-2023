"""Tests for the modal module."""
import pytest
from dashboard.components.modal import handle_backdrop_click, open_modal
from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict

MODALCLASSNAME = "SUPERUNIQUE"
MODALCLASSNAMEWITHHIDDEN = MODALCLASSNAME + " hidden"
MODALIDS = ["123", "321"]


@pytest.mark.test_modal
class TestHideModalContainer:
    """Tests for hide modal container function."""

    def test_hide_on_child_closed(self) -> None:
        """Test if container is hidden when all children are closed."""
        assert handle_backdrop_click(MODALIDS, MODALCLASSNAME, 0) == (
            [False, False],
            MODALCLASSNAMEWITHHIDDEN,
        )

    def test_open_modal(self) -> None:
        """Test if a modal can be opened."""

        def mocked_ctx():
            context_value.set(
                AttributeDict(**{"triggered_inputs": [{"prop_id": f"{MODALIDS[0]}.id"}]})
            )

            return open_modal(MODALIDS, MODALCLASSNAMEWITHHIDDEN, [True, False])

        ctx = copy_context()
        assert ctx.run(mocked_ctx) == (
                [True, False],
                MODALCLASSNAME,
            )

    def test_close_modal(self) -> None:
        """Test if a modal can be closed."""

        def mocked_ctx():
            context_value.set(
                AttributeDict(**{"triggered_inputs": [{"prop_id": f"{MODALIDS[0]}.id"}]})
            )

            return open_modal(MODALIDS, MODALCLASSNAMEWITHHIDDEN, [False, False])

        ctx = copy_context()
        assert ctx.run(mocked_ctx) == (
                [False, False],
                MODALCLASSNAMEWITHHIDDEN,
            )

