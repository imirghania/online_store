import pytest
from httpx import ASGITransport, AsyncClient



@pytest.mark.asyncio
async def test_create_product_type(test_app, first_product_type):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        res = await ac.post("/api/product-types", json=first_product_type)
        res_dict = res.json()
        
        assert res.status_code == 201
        for item1, item2 in zip(res_dict, first_product_type):
            assert item1[0] == item2[0]
            assert item1[1] == item2[1]


@pytest.mark.asyncio
async def test_create_with_duplicate_attr_product_type(test_app, 
                                                    product_type_with_duplicate_attrs):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        res = await ac.post("/api/product-types", 
                            json=product_type_with_duplicate_attrs)
        res_dict = res.json()
        
        assert res.status_code == 201
        assert res_dict["general_attributes"].count(
            product_type_with_duplicate_attrs["general_attributes"][0]) == 1
        assert res_dict["variant_attributes"].count(
            product_type_with_duplicate_attrs["variant_attributes"][0]) == 1


@pytest.mark.asyncio
async def test_get_one_product_type(test_app, first_product_type):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        post_res = await ac.post("/api/product-types", json=first_product_type)
        post_res_dict = post_res.json()
        
        get_res = await ac.get(f"/api/product-types/{post_res_dict['id']}")
        get_res_dict = get_res.json()
        
        assert post_res.status_code == 201
        assert get_res.status_code == 200
        assert get_res_dict["id"] == post_res_dict["id"]
        for item1, item2 in zip(get_res_dict, post_res_dict):
            assert item1[0] == item2[0]
            assert item1[1] == item2[1]


@pytest.mark.asyncio
async def test_get_all_product_type(test_app, first_product_type, second_product_type):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        await ac.post("/api/product-types", json=first_product_type)
        await ac.post("/api/product-types", json=second_product_type)
        
        get_res = await ac.get(f"/api/product-types")
        get_res_dict = get_res.json()
        
        assert get_res.status_code == 200
        assert len(get_res_dict) == 2


@pytest.mark.asyncio
async def test_update_product_type(test_app, second_product_type):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        update_payload = {
            "name": "Product type name UPDATED"
        }
        post_res = await ac.post("/api/product-types", json=second_product_type)
        post_res_dict = post_res.json()
        patch_res = await ac.patch(f"/api/product-types/{post_res_dict['id']}", 
                                json=update_payload)
        patch_res_dict = patch_res.json()
        
        assert patch_res.status_code == 200
        assert patch_res_dict["name"] == update_payload["name"]


@pytest.mark.asyncio
async def test_update_product_type(test_app, second_product_type):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        update_payload = {
            "name": "Product type name UPDATED"
        }
        post_res = await ac.post("/api/product-types", json=second_product_type)
        post_res_dict = post_res.json()
        patch_res = await ac.patch(f"/api/product-types/{post_res_dict['id']}", 
                                json=update_payload)
        patch_res_dict = patch_res.json()
        
        assert patch_res.status_code == 200
        assert patch_res_dict["name"] == update_payload["name"]


@pytest.mark.asyncio
@pytest.mark.parametrize("attribute_type, attribute_type_list_key", 
                        [
                            ("general", "general_attributes"), 
                            ("variant", "variant_attributes")
                        ])
async def test_add_attr_product_type(test_app, second_product_type, 
                                    attribute_type,
                                    attribute_type_list_key):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        params = {
            "attribute_id": "45b70c38e251a3e549d68ct3",
            "attribute_type": attribute_type
        }
        post_res = await ac.post("/api/product-types", json=second_product_type)
        post_res_dict = post_res.json()
        patch_res = await ac.patch(f"/api/product-types/{post_res_dict['id']}/add-attribute", 
                                params=params)
        patch_res_dict = patch_res.json()
        
        assert patch_res.status_code == 200
        assert len(patch_res_dict[attribute_type_list_key]) == 3


@pytest.mark.asyncio
@pytest.mark.parametrize("attribute_type, attribute_type_list_key", 
                        [
                            ("general", "general_attributes"), 
                            ("variant", "variant_attributes")
                        ])
async def test_remove_attr_product_type(test_app, 
                                        product_type_common_attr_gen_var, 
                                        attribute_type,
                                        attribute_type_list_key):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        params = {
            "attribute_id": "67b10c38e251a3e549d68cf1",
            "attribute_type": attribute_type
        }
        post_res = await ac.post("/api/product-types", 
                                json=product_type_common_attr_gen_var)
        post_res_dict = post_res.json()
        patch_res = await ac.patch(
            f"/api/product-types/{post_res_dict['id']}/remove-attribute", 
            params=params)
        patch_res_dict = patch_res.json()
        
        assert patch_res.status_code == 200
        assert len(patch_res_dict[attribute_type_list_key]) == 1