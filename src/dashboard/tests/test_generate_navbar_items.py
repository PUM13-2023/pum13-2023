import pytest
from dashboard.components.navbar_component import generate_navbar_items, navbar_items

ITEM_EXIST = "Dashboard"
ITEM_NOT_EXIST = "😂😂😂"
NAVBAR_ITEMS_COUNT = len(navbar_items)


@pytest.mark.test_generate_navbar_items
class TestGenerateNavbarItems:
    def test_item_not_exist(self):
        navbar_list = generate_navbar_items(ITEM_NOT_EXIST)
        assert navbar_list == 'Item to highlight does not exist in the navbar'

    def test_item_exist(self):
        navbar_list = generate_navbar_items(ITEM_EXIST)
        assert navbar_list

    def test_correct_number_items(self):
        navbar_list = generate_navbar_items(ITEM_EXIST)
        assert len(navbar_list) == NAVBAR_ITEMS_COUNT

    def test_incorrect_number_items(self):
        navbar_list = generate_navbar_items(ITEM_NOT_EXIST)
        assert len(navbar_list) != NAVBAR_ITEMS_COUNT




