import pytest


@pytest.fixture()
def first_product_type():
    payload = {
        "name": "First product Type",
        "taxes_class": "a tax class",
        "general_attributes": ["67b10c38e251a3e549d68cf1", "37b10c38e251a3e549d68cfh"],
        "variant_attributes": ["45c10c38e251a3e549d68cfe", "69f30c38e251a3e549d68cml"],
        }
    return payload


@pytest.fixture()
def second_product_type():
    payload = {
        "name": "Second product Type",
        "taxes_class": "another tax class",
        "general_attributes": ["67b10c38e251a3e549d68cf1", "37b10c38e251a3e549d68cfh"],
        "variant_attributes": ["45c10c38e251a3e549d68cfe", "69f30c38e251a3e549d68cml"],
        }
    return payload


@pytest.fixture()
def product_type_with_duplicate_attrs():
    payload = {
        "name": "Second product Type",
        "taxes_class": "tax class",
        "general_attributes": ["67b10c38e251a3e549d68cf1", "67b10c38e251a3e549d68cf1", "37b10c38e251a3e549d68cfh"],
        "variant_attributes": ["69f30c38e251a3e549d68cml", "45c10c38e251a3e549d68cfe", "69f30c38e251a3e549d68cml"],
        }
    return payload


@pytest.fixture()
def product_type_common_attr_gen_var():
    payload = {
        "name": "Second product Type",
        "taxes_class": "another tax class",
        "general_attributes": ["67b10c38e251a3e549d68cf1", "37b10c38e251a3e549d68cfh"],
        "variant_attributes": ["45c10c38e251a3e549d68cfe", "67b10c38e251a3e549d68cf1"],
        }
    return payload

