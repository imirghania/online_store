import pytest
from httpx import ASGITransport, AsyncClient



@pytest.mark.asyncio
async def test_create_media(test_app, first_media):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        res = await ac.post("/api/media", json=first_media)
        res_dict = res.json()
        
        assert res.status_code == 201
        for item1, item2 in zip(res_dict, first_media):
            assert item1[0] == item2[0]
            assert item1[1] == item2[1]


@pytest.mark.asyncio
async def test_thumbnail_alt_autonaming_media(test_app, second_media):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        res = await ac.post("/api/media", json=second_media)
        res_dict = res.json()
        
        assert res.status_code == 201
        for item1, item2 in zip(res_dict, second_media):
            assert item1[0] == item2[0]
            assert item1[1] == item2[1]
        assert res_dict["thumbnail"]["alt"] == res_dict["image"]["alt"] + " [thumbnail]"


@pytest.mark.asyncio
async def test_create_duplicate_media(test_app, first_media):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        res1 = await ac.post("/api/media", json=first_media)
        res2 = await ac.post("/api/media", json=first_media)
        
        assert res1.status_code == 201
        assert res2.status_code == 409


@pytest.mark.asyncio
async def test_get_one_media(test_app, first_media):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        post_res = await ac.post("/api/media", json=first_media)
        post_res_dict = post_res.json()
        
        get_res = await ac.get(f"/api/media/{post_res_dict['id']}")
        get_res_dict = get_res.json()
        
        assert post_res.status_code == 201
        assert get_res.status_code == 200
        assert get_res_dict["id"] == post_res_dict["id"]
        for item1, item2 in zip(get_res_dict, post_res_dict):
            assert item1[0] == item2[0]
            assert item1[1] == item2[1]


@pytest.mark.asyncio
async def test_get_all_media(test_app, first_media, second_media):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        await ac.post("/api/media", json=first_media)
        await ac.post("/api/media", json=second_media)
        
        get_res = await ac.get(f"/api/media")
        get_res_dict = get_res.json()
        
        assert get_res.status_code == 200
        assert len(get_res_dict) == 2


@pytest.mark.asyncio
async def test_update_image_media(test_app, second_media):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        update_payload = {
            "image": {
                "url": "https://www.google.com/url?sa=i&url=https%3A%2F%2Fmilitaryequipment.in%2Fproduct%2Ftrouser-6-pocket-without-patch-elastic-bottom%2F&psig=AOvVaw28VfuRLa9KEO2O6mrgPCGK&ust=1740050696446000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCJC6tpXQz4sDFQAAAAAdAAAAABAJ",
                "width": 600,
                "height": 600
            }
        }
        post_res = await ac.post("/api/media", json=second_media)
        post_res_dict = post_res.json()
        patch_res = await ac.patch(f"/api/media/{post_res_dict['id']}", 
                                json=update_payload)
        patch_res_dict = patch_res.json()
        
        assert patch_res.status_code == 200
        assert patch_res_dict["image"]["url"] == update_payload["image"]["url"]
        assert patch_res_dict["title"] is not None


@pytest.mark.asyncio
async def test_delete_one_media(test_app, first_media):
    async with AsyncClient(transport=ASGITransport(test_app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        post_res = await ac.post("/api/media", json=first_media)
        post_res_dict = post_res.json()
        
        delete_res = await ac.delete(f"/api/media/{post_res_dict['id']}")
        
        get_res = await ac.get(f"/api/media/{post_res_dict['id']}")
        
        assert post_res.status_code == 201
        assert delete_res.status_code == 204
        assert get_res.status_code == 404
