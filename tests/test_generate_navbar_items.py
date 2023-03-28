"""Test navbar item generation."""
import pytest

from dashboard.components.navbar_component import HIGHLIGHT_STYLE, generate_navbar_items

ITEM_EXIST = "/"
ITEM_NOT_EXIST = "/this-path-does-not-exist"

# This dict is supposed to simulate the dash.page_registry dict
# Add the name of the page and the paths here in order to test them
PAGE_REGISTRY = {
    "page_home": {"name": "Home", "path": "/", "nav_item": True},
    "page_first": {"name": "First", "path": "/first", "order": 1, "nav_item": True},
    "page_second": {"name": "Second", "path": "/second", "order": 2, "nav_item": True},
    "page_hidden": {"name": "Hidden", "path": "/hidden", "nav_item": False},
    "page_hidden_implicit": {"name": "Hidden Implicit", "path": "/hidden-implicit"},
}

NAVBAR_VISIBLE = ["/", "/first", "/second"]
NAVBAR_HIDDEN_EXPLICIT = "/hidden"
NAVBAR_HIDDEN_IMPLICIT = "/hidden-default"
NAVBAR_HIDDEN = {NAVBAR_HIDDEN_EXPLICIT, NAVBAR_HIDDEN_IMPLICIT}


@pytest.fixture
def navbar_list():
    """Return a list of generated navbar items."""
    return generate_navbar_items(PAGE_REGISTRY)


@pytest.fixture
def navbar_urls(navbar_list):
    """Return the set of urls included in the generated navbar items."""
    return {item.href for item in navbar_list}


class TestGenerateNavbarItems:
    """Class that contains tests for navbar item generation."""
    def test_includes_visible_items(self, navbar_urls) -> None:
        """Test visible items are included.

        Test items marked nav_item=True are included in the
        generated component list. This is tested by checking that the
        set of visible urls is a subset of the set of urls included in
        the navbar list.
        """
        assert set(NAVBAR_VISIBLE) <= navbar_urls

    def test_excludes_item_hidden_explicit(self, navbar_urls) -> None:
        """Test explicitly hidden items are hidden.

        Test items marked nav_item=False are not included in
        the generated component list.
        """
        assert NAVBAR_HIDDEN_EXPLICIT not in navbar_urls

    def test_excludes_item_hidden_implicit(self, navbar_urls) -> None:
        """Test explicitly hidden items are hidden.

        Test items that do not have a nav_itembar key are not
        included in the generated component list.
        """
        assert NAVBAR_HIDDEN_IMPLICIT not in navbar_urls

    def test_navbar_item_order(self, navbar_list):
        """Test url items are listed in correct order.

        Since this test should not fail unnecessarily, the navbar list
        is filtered so that the order is only checked on items that are
        supposed to be included.
        """
        navbar_urls_filtered = [item.href for item in navbar_list if item.href in NAVBAR_VISIBLE]

        assert navbar_urls_filtered == NAVBAR_VISIBLE

    def test_navbar_highlight_correct_item(self):
        """Test that the item that should be highlighted is so.

        Testing all urls is probably unnecessary, but should catch some
        possible incorrect implementations.
        """
        for highlight_url in NAVBAR_VISIBLE:
            navbar_items = generate_navbar_items(PAGE_REGISTRY, highlight_url)

            # Find the first item with the highlighted url.
            should_be_highlighted = next(
                item for item in navbar_items if item.href == highlight_url
            )

            assert HIGHLIGHT_STYLE in should_be_highlighted.className

    def test_navbar_no_highlight_other(self):
        """Test that no other item is highlighted.

        Test that no item other than the highlighted item is
        highlighted when a highlight_url is specified.
        """
        highlight_url = NAVBAR_VISIBLE[0]

        navbar_items = generate_navbar_items(PAGE_REGISTRY, highlight_url)

        for item in navbar_items:
            if item.href == highlight_url:
                continue

            try:
                assert HIGHLIGHT_STYLE not in item.className
            except AttributeError:
                pass  # Not having a className attr is also ok.

    def test_navbar_highlight_none(self, navbar_list):
        """Test that no item is highlighted.

        Test that no item is highlighted when generating a navbar item
        list without specifying a highlight url.
        """
        for item in navbar_list:
            try:
                assert HIGHLIGHT_STYLE not in item.className
            except AttributeError:
                pass  # Not having a className attr is also ok.
