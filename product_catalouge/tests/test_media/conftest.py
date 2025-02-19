import pytest


@pytest.fixture()
def first_media():
    payload = {
        "title": "Blue T-shirt",
        "image": {
            "url": "https://www.google.com/url?sa=i&url=https%3A%2F%2Faac.com.au%2Fproduct%2Ft-shirts%2F&psig=AOvVaw2swZRpPralai5Hn5tnKeTt&ust=1740045852264000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCKjhnIm-z4sDFQAAAAAdAAAAABAJ",
            "alt": "Blue T-shirt",
            "width": 600,
            "height": 600
            }
        }
    return payload


@pytest.fixture()
def second_media():
    payload = {
        "title": "Casual Pants",
        "image": {
            "url": "https://www.google.com/url?sa=i&url=https%3A%2F%2Fbruntworkwear.com%2Fproducts%2Fthe-costello-pant&psig=AOvVaw1qgn1fFq5sdg-5wBth6Nro&ust=1740045948819000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCOjFm72-z4sDFQAAAAAdAAAAABAS",
            "alt": "Casual Pants",
            "width": 600,
            "height": 600
            },
        "thumbnail": {
            "url": "https://www.google.com/url?sa=i&url=https%3A%2F%2Fbruntworkwear.com%2Fproducts%2Fthe-costello-pant&psig=AOvVaw1qgn1fFq5sdg-5wBth6Nro&ust=1740045948819000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCOjFm72-z4sDFQAAAAAdAAAAABAS",
            "width": 20,
            "height": 20
            }
        }
    return payload


@pytest.fixture()
def same_name_first_media():
    payload = {
        "title": "Blue T-shirt",
        "image": {
            "url": "https://www.google.com/url?sa=i&url=https%3A%2F%2Faac.com.au%2Fproduct%2Ft-shirts%2F&psig=AOvVaw2swZRpPralai5Hn5tnKeTt&ust=1740045852264000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCKjhnIm-z4sDFQAAAAAdAAAAABAJ",
            "alt": "Blue T-shirt",
            "width": 600,
            "height": 600
            }
        }
    return payload