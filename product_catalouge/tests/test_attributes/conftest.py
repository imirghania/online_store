import pytest
import pytest_asyncio
from product_catalouge.models.attribute import AttributeModel



@pytest.fixture()
def str_attr():
    payload = {
        "label": "String",
        "internal_code": "String",
        "type": "string",
        "is_required": True,
        "measurement_type": "distance",
        "unit": "cm",
        "options": ["option1"]
        }
    return payload


@pytest.fixture()
def num_attr():
    payload = {
        "label": "Number",
        "internal_code": "Number",
        "type": "number",
        "is_required": True,
        "measurement_type": "distance",
        "unit": "m",
        "options": ["option1"]
        }
    return payload


@pytest.fixture()
def select_attr():
    payload = {
        "label": "Select",
        "internal_code": "Select",
        "type": "select",
        "is_required": True,
        "measurement_type": "distance",
        "unit": "m",
        "options": ["option1"]
        }
    return payload



@pytest.fixture(params=["str_attr", "select_attr"])
def str_select_payload(request):
    return request.getfixturevalue(request.param)


@pytest.fixture()
def attrs(str_attr, num_attr, select_attr):
    return [str_attr, num_attr, select_attr]


@pytest_asyncio.fixture()
async def three_attrs(testdb, attrs):
    inserted_attrs = []
    for attr in attrs:
        inserted_attr = await AttributeModel(**attr).insert()
        inserted_attrs.append(inserted_attr)
    yield inserted_attrs

