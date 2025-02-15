import pytest



@pytest.fixture()
def main_category():
    payload = {
        "name": "Main Category",
        "slug": "main-category",
        "description": "The description of the Main Category",
        }
    return payload


@pytest.fixture()
def child_category():
    payload = {
        "name": "Child Category",
        "slug": "child-category",
        "description": "The description of the Child Category",
        }
    return payload


@pytest.fixture()
def grand_child_category():
    payload = {
        "name": "Grand Child Category",
        "slug": "grand-child-category",
        "description": "The description of the Grand Child Category",
        }
    return payload


@pytest.fixture()
def update_payload():
    payload = {
        "name": "Test Category",
        "slug": "test-category",
        "description": "The description of the Test Category",
        }
    return payload



@pytest.fixture(params=["main_category", "child_category", "grand_child_category"])
def category_payload(request):
    return request.getfixturevalue(request.param)


@pytest.fixture()
def categories(main_category, child_category, grand_child_category):
    return [main_category, child_category, grand_child_category]

