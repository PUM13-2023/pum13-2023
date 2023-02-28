import pytest
from dashboard.components.navbar_component import generate_navbar_items, navbar_items
from dash import html
from dash.dependencies import Component

ITEM_EXIST = "Dashboard"
ITEM_NOT_EXIST = "😂😂😂"
HIGHLIGHT_ID = "highlight-home"
navbar_items_count = len(navbar_items)

test_list = [
    html.Div(id='hello')
]


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
        assert len(navbar_list) == navbar_items_count

    def test_incorrect_number_items(self):
        navbar_list = generate_navbar_items(ITEM_NOT_EXIST)
        assert len(navbar_list) != navbar_items_count

    def test_no_highlighted_exist(self):
        navbar_list = generate_navbar_items()
        requested_id = False
        for item in navbar_list:
            if item.id == HIGHLIGHT_ID:
                requested_id = item.id
                break

        assert not requested_id

    def test_highlighted_exist(self):
        navbar_list = generate_navbar_items(ITEM_EXIST)
        found_id = False
        for item in navbar_list:
            if item.id:
                found_id = True
                break

        assert found_id

    def test_highlighted_correct_item(self):
        navbar_list = generate_navbar_items(ITEM_EXIST)
        requested_id = False
        for item in navbar_list:
            if item.id == HIGHLIGHT_ID:
                requested_id = item.id
                break

        assert requested_id == HIGHLIGHT_ID

    def test_highlighted_wrong_item(self):
        navbar_list = generate_navbar_items(ITEM_EXIST)
        not_found = False
        for item in navbar_list:
            if item.id == HIGHLIGHT_ID:
                not_found = True
                break

        assert not_found
