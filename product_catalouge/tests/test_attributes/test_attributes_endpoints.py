import pytest
from httpx import ASGITransport, AsyncClient
# from product_catalouge.web.api.api import app


@pytest.mark.asyncio
async def test_create_str_select_attrs(test_app, str_select_payload):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        res = await ac.post("/api/attributes", json=str_select_payload)
        assert res.status_code == 201
        res_dict = res.json()
        for key in ["measurement_type", "unit"]:
            assert res_dict[key] is None


@pytest.mark.asyncio
async def test_create_str_attr(test_app, str_attr):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        res = await ac.post("/api/attributes", json=str_attr)
        assert res.status_code == 201
        res_dict = res.json()
        for key in ["measurement_type", "unit", "options"]:
            assert res_dict[key] is None


@pytest.mark.asyncio
async def test_create_num_attr(test_app, num_attr):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        res = await ac.post("/api/attributes", json=num_attr)
        assert res.status_code == 201
        res_dict = res.json()
        assert res_dict["options"] is None
        assert res_dict["is_numeric"] == True


@pytest.mark.asyncio
async def test_get_all_attrs(attrs, test_app):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        for attr in attrs:
            await ac.post("/api/attributes", json=attr)
        res = await ac.get("/api/attributes")
        assert res.status_code == 200
        assert len(res.json()) == 3


@pytest.mark.asyncio
async def test_get_attr_by_id(test_app, str_attr):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        res_post = await ac.post("/api/attributes", json=str_attr)
        attr_id = res_post.json()["id"]
        res_get = await ac.get(f"/api/attributes/{attr_id}")
        assert res_get.status_code == 200
        assert res_post.json()["id"] == attr_id

