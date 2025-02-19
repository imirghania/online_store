import pytest
from httpx import ASGITransport, AsyncClient



@pytest.mark.asyncio
async def test_create_product_only(test_app, first_product):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        res = await ac.post("/api/product", json=first_product)
        res_dict = res.json()
        print("="*100)
        print(f"[TEST][PAYLOAD]: {first_product}")
        print("-"*100)
        print(f"[TEST][RESPONSE]: {res_dict}")
        assert res.status_code == 201
        for item1, item2 in zip(res_dict, first_product):
            assert item1[0] == item2[0]
            assert item1[1] == item2[1]


@pytest.mark.asyncio
async def test_create_with_duplicate_attr_product_only(test_app, 
                                                    product_with_duplicate_attrs):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        res = await ac.post("/api/product", 
                            json=product_with_duplicate_attrs)
        res_dict = res.json()
        
        assert res.status_code == 201
        assert res_dict["categories"].count(
            product_with_duplicate_attrs["categories"][0]) == 1
        assert res_dict["channels"].count(
            product_with_duplicate_attrs["channels"][0]) == 1
        assert res_dict["media_gallery"].count(
            product_with_duplicate_attrs["media_gallery"][0]) == 1


@pytest.mark.asyncio
async def test_get_one_product_only(test_app, first_product):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        post_res = await ac.post("/api/product", json=first_product)
        post_res_dict = post_res.json()
        
        get_res = await ac.get(f"/api/product/{post_res_dict['id']}")
        get_res_dict = get_res.json()
        
        assert post_res.status_code == 201
        assert get_res.status_code == 200
        assert get_res_dict["id"] == post_res_dict["id"]
        for item1, item2 in zip(get_res_dict, post_res_dict):
            assert item1[0] == item2[0]
            assert item1[1] == item2[1]


@pytest.mark.asyncio
async def test_get_all_product_only(test_app, first_product, second_product):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        await ac.post("/api/product", json=first_product)
        await ac.post("/api/product", json=second_product)
        
        get_res = await ac.get(f"/api/product")
        get_res_dict = get_res.json()
        
        assert get_res.status_code == 200
        assert len(get_res_dict) == 2


@pytest.mark.asyncio
@pytest.mark.parametrize("attr_name, attr_value",
                        [
                            ("name", "Second product EDITED"),
                            ("product_type", "8c210c38e251a3e549d68cw4")
                        ]
                        )
async def test_update_product_only(test_app, second_product, attr_name, attr_value):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        update_payload = {
            attr_name: attr_value
        }
        post_res = await ac.post("/api/product", json=second_product)
        post_res_dict = post_res.json()
        patch_res = await ac.patch(f"/api/product/{post_res_dict['id']}", 
                                json=update_payload)
        patch_res_dict = patch_res.json()
        
        assert patch_res.status_code == 200
        assert patch_res_dict[attr_name] == update_payload[attr_name]


@pytest.mark.asyncio
@pytest.mark.parametrize("item_type, item_key", 
                        [
                            ("category", "categories"), 
                            ("channel", "channels"),
                            ("media", "media_gallery")
                        ])
async def test_add_attr_product_only(test_app, second_product, 
                                    item_type,
                                    item_key):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        params = {
            "item_type": item_type
        }
        payload = {
            "item_id": "45b70c38e251a3e549d68ct3",
        }
        post_res = await ac.post("/api/product", json=second_product)
        post_res_dict = post_res.json()
        patch_res = await ac.patch(f"/api/product/{post_res_dict['id']}/add", 
                                params=params, json=payload)
        patch_res_dict = patch_res.json()
        
        assert patch_res.status_code == 200
        assert len(patch_res_dict[item_key]) == 3


@pytest.mark.asyncio
@pytest.mark.parametrize("item_type, item_key", 
                        [
                            ("category", "categories"), 
                            ("channel", "channels"),
                            ("media", "media_gallery")
                        ])
async def test_remove_attr_product_only(test_app, product_common_id, 
                                    item_type,
                                    item_key):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        params = {
            "item_type": item_type
        }
        payload = {
            "item_id": "67b10c38e251a3e549d68cf1",
        }
        post_res = await ac.post("/api/product", json=product_common_id)
        post_res_dict = post_res.json()
        patch_res = await ac.patch(f"/api/product/{post_res_dict['id']}/remove", 
                                params=params, json=payload)
        patch_res_dict = patch_res.json()
        
        assert patch_res.status_code == 200
        assert len(patch_res_dict[item_key]) == 1