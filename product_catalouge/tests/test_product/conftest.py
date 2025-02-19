import pytest


@pytest.fixture()
def first_product():
    payload = {
        "name": "First product",
        "product_type": "67b10c38e251a3e549d68cf1",
        "categories": ["67b10c38e251a3e549d68cf1", "37b10c38e251a3e549d68cfh"],
        "channels": ["45c10c38e251a3e549d68cfe", "69f30c38e251a3e549d68cml"],
        "main_media": "67b10c38e251a3e549d68cf1",
        "media_gallery": ["45c10c38e251a3e549d68cfe", "69f30c38e251a3e549d68cml"],
        }
    return payload


@pytest.fixture()
def second_product():
    payload = {
        "name": "Second product",
        "product_type": "67b10c38e251a3e549d68cf1",
        "categories": ["67b10c38e251a3e549d68cf1", "37b10c38e251a3e549d68cfh"],
        "channels": ["45c10c38e251a3e549d68cfe", "69f30c38e251a3e549d68cml"],
        "main_media": "67b10c38e251a3e549d68cf1",
        "media_gallery": ["45c10c38e251a3e549d68cfe", "69f30c38e251a3e549d68cml"],
        }
    return payload


@pytest.fixture()
def product_with_duplicate_attrs():
    payload = {
        "name": "First product",
        "product_type": "67b10c38e251a3e549d68cf1",
        "categories": ["67b10c38e251a3e549d68cf1", "67b10c38e251a3e549d68cf1"],
        "channels": ["45c10c38e251a3e549d68cfe", "45c10c38e251a3e549d68cfe"],
        "main_media": "67b10c38e251a3e549d68cf1",
        "media_gallery": ["45c10c38e251a3e549d68cfe", "45c10c38e251a3e549d68cfe"],
        }
    return payload


@pytest.fixture()
def product_common_id():
    payload = {
        "name": "Second product",
        "product_type": "67b10c38e251a3e549d68cf1",
        "categories": ["67b10c38e251a3e549d68cf1", "37b10c38e251a3e549d68cfh"],
        "channels": ["45c10c38e251a3e549d68cfe", "67b10c38e251a3e549d68cf1"],
        "main_media": "67b10c38e251a3e549d68cf1",
        "media_gallery": ["45c10c38e251a3e549d68cfe", "67b10c38e251a3e549d68cf1"],
        }
    return payload

