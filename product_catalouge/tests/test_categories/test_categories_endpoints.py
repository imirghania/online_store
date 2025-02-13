import pytest
from httpx import ASGITransport, AsyncClient
# from product_catalouge.web.api.api import app


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



# @pytest.mark.asyncio
# async def test_create_str_attr(test_app, str_attr):
#     async with AsyncClient(transport=ASGITransport(test_app), 
#                             base_url="http://test", 
#                             follow_redirects=True) as ac:
#         res = await ac.post("/api/attributes", json=str_attr)
#         assert res.status_code == 201
#         res_dict = res.json()
#         for key in ["measurement_type", "unit", "options"]:
#             assert res_dict[key] is None


# @pytest.mark.asyncio
# async def test_create_num_attr(test_app, num_attr):
#     async with AsyncClient(transport=ASGITransport(test_app), 
#                             base_url="http://test", 
#                             follow_redirects=True) as ac:
#         res = await ac.post("/api/attributes", json=num_attr)
#         assert res.status_code == 201
#         res_dict = res.json()
#         assert res_dict["options"] is None
#         assert res_dict["is_numeric"] == True


# @pytest.mark.asyncio
# async def test_get_all_attrs(attrs, test_app):
#     async with AsyncClient(transport=ASGITransport(test_app), 
#                             base_url="http://test", 
#                             follow_redirects=True) as ac:
#         for attr in attrs:
#             await ac.post("/api/attributes", json=attr)
#         res = await ac.get("/api/attributes")
#         assert res.status_code == 200
#         assert len(res.json()) == 3


# @pytest.mark.asyncio
# async def test_get_attr_by_id(test_app, str_attr):
#     async with AsyncClient(transport=ASGITransport(test_app), 
#                             base_url="http://test", 
#                             follow_redirects=True) as ac:
#         res_post = await ac.post("/api/attributes", json=str_attr)
#         attr_id = res_post.json()["id"]
#         res_get = await ac.get(f"/api/attributes/{attr_id}")
#         assert res_get.status_code == 200
#         assert res_post.json()["id"] == attr_id

