import pytest
from dashboard.components.navbar_component import generate_navbar_items, navbar_items
from dashboard.components.highlight_item import HIGHLIGHT_CLASSNAME

ITEM_EXIST = "Dashboards"
ITEM_NOT_EXIST = "😂😂😂"
navbar_items_count = len(navbar_items)


@pytest.mark.test_generate_navbar_items
class TestGenerateNavbarItems:
    def test_item_not_exist(self):
        navbar_list = generate_navbar_items(ITEM_NOT_EXIST)
        assert not navbar_list

    def test_item_exist(self):
        navbar_list = generate_navbar_items(ITEM_EXIST)
        assert navbar_list

    def test_correct_number_items(self):
        navbar_list = generate_navbar_items(ITEM_EXIST)
        assert len(navbar_list) == navbar_items_count

    def test_incorrect_number_items(self):
        navbar_list = generate_navbar_items(ITEM_NOT_EXIST)
        assert len(navbar_list) != navbar_items_count

    def test_no_highlighted_exist(self):
        navbar_list = generate_navbar_items()
        for item in navbar_list:
            assert HIGHLIGHT_CLASSNAME not in item

    def test_highlighted_exist(self):
        navbar_list = generate_navbar_items(ITEM_EXIST)
        found_class = False
        for item in navbar_list:
            if HIGHLIGHT_CLASSNAME in item:
                found_class = True

        assert found_class

    def test_highlighted_correct_item(self):
        navbar_list = generate_navbar_items(ITEM_EXIST)
        requested_class = False
        for item in navbar_list:
            if item.classname == HIGHLIGHT_CLASSNAME:
                requested_class = True
                break

        assert requested_class

