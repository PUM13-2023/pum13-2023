import pytest

from dashboard.components.navbar_component import generate_navbar_items

ITEM_EXIST = "Home"
ITEM_NOT_EXIST = "Item_x"
navbar_items_count = 1

# This dict is supposed to simulate the dash.page_registry dict
# Add the name of the page and the paths here in order to test them
navbar_items = {"page_home": {"name": "Home", "path": "/"}}


@pytest.mark.test_generate_navbar_items
class TestGenerateNavbarItems:
    def test_item_not_exist(self) -> None:
        """
        Test that you cannot generate a list with tags when trying to
        highlight an item that does not exist in the navbar
        """
        navbar_list = generate_navbar_items(navbar_items, ITEM_NOT_EXIST)
        assert not navbar_list

    def test_item_exist(self) -> None:
        """
        Test that a list is generated when a correct
        item to highlight exists
        """
        navbar_list = generate_navbar_items(navbar_items, ITEM_EXIST)
        assert navbar_list

    def test_correct_number_items(self) -> None:
        """
        Test that the generated list has the same
        amount of items to the original navbar list
        """
        navbar_list = generate_navbar_items(navbar_items, ITEM_EXIST)
        assert len(navbar_list) == navbar_items_count

    def test_incorrect_number_items(self) -> None:
        """
        Test that a generated list with items that do not exist will
        not be the same length as the original navbar list
        """
        navbar_list = generate_navbar_items(navbar_items, ITEM_NOT_EXIST)
        assert len(navbar_list) != navbar_items_count

    def test_no_highlighted_exist(self) -> None:
        """
        Test that it is possible to generate a list
        without any highlighted items
        """
        navbar_list = generate_navbar_items(navbar_items)
        assert all(item.className == "" for item in navbar_list)

    def test_highlighted_exist(self) -> None:
        """
        Test that it is possible to
        generate a list with a highlighted item
        """
        navbar_list = generate_navbar_items(navbar_items, ITEM_EXIST)
        found_class = False

        for item in navbar_list:
            if hasattr(item, "className"):
                found_class = True
                break

        assert found_class

    def test_highlighted_correct_item(self) -> None:
        """
        Test that the generated list highlights the correct item
        """
        navbar_list = generate_navbar_items(navbar_items, ITEM_EXIST)
        requested_class = False
        for item in navbar_list:
            if hasattr(item, "className") and item.children == ITEM_EXIST:
                requested_class = True
                break

        assert requested_class
