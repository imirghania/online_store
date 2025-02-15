import pytest
from httpx import ASGITransport, AsyncClient



@pytest.mark.asyncio
async def test_create_category(test_app, main_category):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        res = await ac.post("/api/categories", json=main_category)
        assert res.status_code == 201
        res_dict = res.json()
        assert res_dict["parent"] is None
        assert res_dict["sub_categories"] == []


@pytest.mark.asyncio
async def test_create_with_parent_category(test_app, main_category, child_category):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        main_cat_res = await ac.post("/api/categories", json=main_category)
        main_cat_dict = main_cat_res.json()
        child_category["parent"] = main_cat_dict["id"]

        child_cat_res = await ac.post("/api/categories", json=child_category)
        child_cat_dict = child_cat_res.json()
        main_cat_res_get = await ac.get(f"/api/categories/{main_cat_dict['id']}")
        main_cat_get_dict = main_cat_res_get.json()

        assert main_cat_res.status_code == 201
        assert child_cat_res.status_code == 201
        assert child_cat_dict["parent"] == main_cat_get_dict['id']
        assert child_cat_dict["id"] in main_cat_get_dict["sub_categories"]


@pytest.mark.asyncio
async def test_get_category(test_app, child_category):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        post_res = await ac.post("/api/categories", json=child_category)
        post_res_dict = post_res.json()
        get_res = await ac.get(f"/api/categories/{post_res_dict['id']}")
        get_res_dict = get_res.json()
        assert get_res.status_code == 200
        for item1, item2 in zip(post_res_dict, get_res_dict):
            assert item1[1] == item2[1]


@pytest.mark.asyncio
async def test_get_all_category(test_app, categories):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        for cat in categories:
            await ac.post("/api/categories", json=cat)
        res = await ac.get("/api/categories")
        assert res.status_code == 200
        assert len(res.json()) == 3


@pytest.mark.asyncio
async def test_create_update_category(test_app, main_category, update_payload):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        main_cat_res = await ac.post("/api/categories", json=main_category)
        main_cat_dict = main_cat_res.json()
        
        updated_main_cat_res = await ac.patch(f"/api/categories/{main_cat_dict['id']}", 
                                            json=update_payload)
        updated_main_cat_dict = updated_main_cat_res.json()

        get_res = await ac.get(f"/api/categories/{main_cat_dict['id']}")
        get_res_dict = get_res.json()

        assert main_cat_res.status_code == 201
        assert updated_main_cat_res.status_code == 200
        for item1, item2 in zip(updated_main_cat_dict, get_res_dict):
            assert item1 == item2


@pytest.mark.asyncio
async def test_delete_with_parent_child_category(test_app, 
                                        main_category, 
                                        child_category,
                                        grand_child_category):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        main_cat_res = await ac.post("/api/categories", json=main_category)
        main_cat_dict = main_cat_res.json()
        child_category["parent"] = main_cat_dict["id"]

        child_cat_res = await ac.post("/api/categories", json=child_category)
        child_cat_dict = child_cat_res.json()
        grand_child_category["parent"] = child_cat_dict["id"]

        grand_child_cat_res = await ac.post("/api/categories", json=grand_child_category)
        grand_child_cat_dict = grand_child_cat_res.json()

        del_res = await ac.delete(f"/api/categories/{child_cat_dict['id']}")
        
        main_cat_res_get = await ac.get(f"/api/categories/{main_cat_dict['id']}")
        main_cat_get_dict = main_cat_res_get.json()

        grand_child_res_get = await ac.get(f"/api/categories/{grand_child_cat_dict['id']}")
        grand_child_get_dict = grand_child_res_get.json()
        
        assert main_cat_res.status_code == 201
        assert child_cat_res.status_code == 201
        assert grand_child_cat_res.status_code == 201
        assert del_res.status_code == 204
        assert grand_child_get_dict["parent"] == main_cat_get_dict['id']
        assert child_cat_dict["id"] not in main_cat_get_dict["sub_categories"]