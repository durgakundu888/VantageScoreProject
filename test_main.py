from fastapi.testclient import TestClient
from main import app, linkedin_posts

client = TestClient(app)

post_example = {"title": "Vacation on the beach", "content": "I just got back from vacation and I'm so stressed.", "category": "Lifestyle", "published": True}
post_example2 = {"title": "Surfing for the first time", "content": "I just had my first surfing lesson and it was wild.", "category": "Health & Wellness", "published": True}
post_example3 = {"title": "Skydiving more than 20000 feet high", "content": "I went skydiving for the first time and would do it again.", "category": "Fun", "published": True}

def setup_function():
    linkedin_posts.clear()

def test_get_all_posts_with_empty_linkedinposts_list():
    response = client.get("/linkedinposts")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Error: No posts found'}

def test_create_linkedin_post():
    response = client.post("/linkedinposts", json=post_example)
    assert response.status_code == 201
    post_id = response.json()['data']['id']
    assert response.json() == {'data': {"title": "Vacation on the beach", "content": "I just got back from vacation and I'm so stressed.", "category": "Lifestyle", "published": True, "id": post_id}}

def test_update_linkedin_post():
    response1 = client.post("/linkedinposts", json=post_example)
    assert response1.status_code == 201
    post_id = response1.json()['data']['id']
    assert response1.json() == {'data': {"title": "Vacation on the beach", "content": "I just got back from vacation and I'm so stressed.", "category": "Lifestyle", "published": True, "id": post_id}}
    response2 = client.put("/linkedinposts/" + str(post_id), json={"title": "Vacation on the beach", "content": "I just got back from vacation and I'm so stressed.", "category": "Entertainment", "published": True, "id": post_id})
    assert response2.status_code == 200
    assert response2.json() == {'message': 'Post with ID ' + str(post_id) + ' successfully updated', 'post_details': {"title": "Vacation on the beach", "content": "I just got back from vacation and I'm so stressed.", "category": "Entertainment", "published": True, "id": post_id}}

def test_delete_linkedin_post():
    response1 = client.post("/linkedinposts", json=post_example)
    assert response1.status_code == 201
    post_id = response1.json()['data']['id']
    assert response1.json() == {'data': {"title": "Vacation on the beach", "content": "I just got back from vacation and I'm so stressed.", "category": "Lifestyle", "published": True, "id": post_id}}
    response2 = client.delete("/linkedinposts/" + str(post_id))
    assert response2.status_code == 200
    assert response2.json() == {'message': 'Post with ID '+str(post_id)+' successfully deleted'}

def test_get_latest_post():
    response1 = client.post("/linkedinposts", json=post_example)
    assert response1.status_code == 201
    post_id1 = response1.json()['data']['id']
    assert response1.json() == {'data': {"title": "Vacation on the beach", "content": "I just got back from vacation and I'm so stressed.", "category": "Lifestyle", "published": True, "id": post_id1}}
    response2 = client.post("/linkedinposts", json=post_example2)
    assert response2.status_code == 201
    post_id2 = response2.json()['data']['id']
    response3 = client.get("/linkedinposts/latest")
    assert response3.status_code == 200
    assert response3.json() == {'post_detail': {'title': 'Surfing for the first time', 'content': 'I just had my first surfing lesson and it was wild.', 'category': 'Health & Wellness', 'published': True, 'id': post_id2}}

def test_get_post_by_id():
    response1 = client.post("/linkedinposts", json=post_example)
    assert response1.status_code == 201
    post_id1 = response1.json()['data']['id']
    assert response1.json() == {'data': {"title": "Vacation on the beach", "content": "I just got back from vacation and I'm so stressed.", "category": "Lifestyle", "published": True, "id": post_id1}}
    response2 = client.post("/linkedinposts", json=post_example2)
    assert response2.status_code == 201
    response3 = client.get("/linkedinposts/"+str(post_id1))
    assert response3.status_code == 200
    assert response3.json() == {'post_detail': {'title': 'Vacation on the beach', 'content': "I just got back from vacation and I'm so stressed.", 'category': 'Lifestyle', 'published': True, 'id': post_id1}}

def test_get_post_by_id_with_empty_linkedinposts_list():
    response = client.get("/linkedinposts/1")
    assert response.status_code == 404
    assert response.json()['detail'] == "Error: No posts found"

def test_get_latest_post_with_empty_linkedinposts_list():
    response = client.get("/linkedinposts/latest")
    assert response.status_code == 404
    assert response.json()['detail'] == "Error: No posts found"

def test_get_all_posts_with_populated_linkedinposts_list():
    response1 = client.post("/linkedinposts", json=post_example)
    assert response1.status_code == 201
    post_id1 = response1.json()['data']['id']
    assert response1.json() == {'data': {"title": "Vacation on the beach", "content": "I just got back from vacation and I'm so stressed.", "category": "Lifestyle", "published": True, "id": post_id1}}
    response2 = client.post("/linkedinposts", json=post_example2)
    assert response2.status_code == 201
    post_id2 = response2.json()['data']['id']
    response3 = client.post("/linkedinposts", json=post_example3)
    assert response3.status_code == 201
    post_id3 = response3.json()['data']['id']
    response4 = client.get("/linkedinposts")
    assert response4.status_code == 200
    assert response4.status_code == 200
    response4.json() == {'data': [{'title': 'Vacation on the beach', 'content': "I just got back from vacation and I'm so stressed.", 'category': 'Lifestyle', 'published': True, 'id': post_id1}, {'title': 'Surfing for the first time', 'content': 'I just had my first surfing lesson and it was wild.', 'category': 'Health & Wellness', 'published': True, 'id': post_id2}, {'title': 'Skydiving more than 20000 feet high', 'content': 'I went skydiving for the first time and would do it again.', 'category': 'Fun', 'published': True, 'id': post_id3}]}

def test_get_post_by_id_with_nonexistent_id():
    response1 = client.post("/linkedinposts", json=post_example)
    assert response1.status_code == 201
    post_id1 = response1.json()['data']['id']
    assert response1.json() == {'data': {"title": "Vacation on the beach", "content": "I just got back from vacation and I'm so stressed.", "category": "Lifestyle", "published": True, "id": post_id1}}
    response2 = client.post("/linkedinposts", json=post_example2)
    assert response2.status_code == 201
    response3 = client.post("/linkedinposts", json=post_example3)
    assert response3.status_code == 201
    response = client.get("/linkedinposts/4")
    assert response.status_code == 404
    assert response.json()['detail'] == "Post with ID 4 not found"

def test_get_post_by_id_with_invalid_input():
    response = client.get("/linkedinposts/fjdjfdhfjd")
    assert response.status_code == 422
    print(response.json()['detail'])
    assert response.json()['detail'] == [{'type': 'int_parsing', 'loc': ['path', 'id'], 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'input': 'fjdjfdhfjd', 'url': 'https://errors.pydantic.dev/2.6/v/int_parsing'}]

def test_get_post_by_id_with_negative_number():
    response = client.get("/linkedinposts/-3")
    assert response.status_code == 404
    print(response.json()['detail'])
    assert response.json()['detail'] ==  "Error: No posts found"

def test_create_post_with_no_body():
    response = client.post("/linkedinposts", json={})
    assert response.status_code == 422
    assert response.json() == {'detail': [{'type': 'missing', 'loc': ['body', 'title'], 'msg': 'Field required', 'input': {}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}, {'type': 'missing', 'loc': ['body', 'content'], 'msg': 'Field required', 'input': {}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}, {'type': 'missing', 'loc': ['body', 'category'], 'msg': 'Field required', 'input': {}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}]}

def test_create_post_with_invalid_body():
    response = client.post("/linkedinposts/", json={"likes": 30})
    assert response.status_code == 422
    assert response.json()['detail'] == [{'type': 'missing', 'loc': ['body', 'title'], 'msg': 'Field required', 'input': {'likes': 30}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}, {'type': 'missing', 'loc': ['body', 'content'], 'msg': 'Field required', 'input': {'likes': 30}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}, {'type': 'missing', 'loc': ['body', 'category'], 'msg': 'Field required', 'input': {'likes': 30}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}]

def test_create_post_with_extra_json_fields():
    response = client.post("/linkedinposts/", json=post_example)
    post_id = response.json()['data']['id']
    assert response.status_code == 201
    assert response.json()['data'] == {'title': 'Vacation on the beach', 'content': "I just got back from vacation and I'm so stressed.", 'category': 'Lifestyle', 'published': True, 'id': post_id}

def test_update_nonexistent_post():
    response = client.put("/linkedinposts/555", json=post_example)
    assert response.status_code == 404
    assert response.json()['detail'] == "Error: No posts found"

def test_update_post_with_extra_json_fields():
    response = client.post("/linkedinposts/", json=post_example)
    post_id = response.json()['data']['id']
    assert response.status_code == 201
    response2 = client.put("/linkedinposts/"+str(post_id), json={"title": "Vacation on the beach", "likes": 30, "comments": 40, "content": "I just got back from vacation and I'm so stressed.", "category": "Lifestyle", "published": True})
    assert response2.status_code == 200
    print(response2.json())
    assert response2.json() == {'message': 'Post with ID '+str(post_id)+' successfully updated', 'post_details': {'title': 'Vacation on the beach', 'content': "I just got back from vacation and I'm so stressed.", 'category': 'Lifestyle', 'published': True, 'id': post_id}}


def test_update_post_with_extra_json_fields_and_new_values():
    response = client.post("/linkedinposts/", json=post_example)
    post_id = response.json()['data']['id']
    assert response.status_code == 201
    response2 = client.put("/linkedinposts/"+str(post_id), json={"title": "Vacation on the beach", "likes": 30, "comments": 40, "content": "I am ready to get back to work.", "category": "Lifestyle", "published": True})
    assert response2.status_code == 200
    assert response2.json() == {'message': 'Post with ID '+str(post_id)+' successfully updated', 'post_details': {'title': 'Vacation on the beach', 'content': "I am ready to get back to work.", 'category': 'Lifestyle', 'published': True, 'id': post_id}}

def test_update_post_with_invalid_body():
    response = client.post("/linkedinposts/", json=post_example)
    post_id = response.json()['data']['id']
    assert response.status_code == 201
    response2 = client.put("/linkedinposts/"+str(post_id), json={"likes": 100, "comments": 1000})
    assert response2.status_code == 422
    assert response2.json() == {'detail': [{'type': 'missing', 'loc': ['body', 'title'], 'msg': 'Field required', 'input': {'likes': 100, 'comments': 1000}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}, {'type': 'missing', 'loc': ['body', 'content'], 'msg': 'Field required', 'input': {'likes': 100, 'comments': 1000}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}, {'type': 'missing', 'loc': ['body', 'category'], 'msg': 'Field required', 'input': {'likes': 100, 'comments': 1000}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}]}

def test_delete_nonexistent_post():
    response = client.post("/linkedinposts", json=post_example)
    assert response.status_code == 201
    response2 = client.delete("/linkedinposts/22")
    assert response2.status_code == 404
    assert response2.json()['detail'] == "Post with ID 22 does not exist"

def test_get_all_posts_with_populated_linkedinposts_list():
    response1 = client.post("/linkedinposts", json=post_example)
    assert response1.status_code == 201
    post_id1 = response1.json()['data']['id']
    assert response1.json() == {'data': {"title": "Vacation on the beach", "content": "I just got back from vacation and I'm so stressed.", "category": "Lifestyle", "published": True, "id": post_id1}}
    response2 = client.post("/linkedinposts", json=post_example2)
    assert response2.status_code == 201
    post_id2 = response2.json()['data']['id']
    response3 = client.post("/linkedinposts", json=post_example3)
    assert response3.status_code == 201
    post_id3 = response3.json()['data']['id']
    response4 = client.get("/linkedinposts")
    assert response4.status_code == 200
    assert response4.json() == {'data': [{'title': 'Vacation on the beach', 'content': "I just got back from vacation and I'm so stressed.", 'category': 'Lifestyle', 'published': True, 'id': post_id1}, {'title': 'Surfing for the first time', 'content': 'I just had my first surfing lesson and it was wild.', 'category': 'Health & Wellness', 'published': True, 'id': post_id2}, {'title': 'Skydiving more than 20000 feet high', 'content': 'I went skydiving for the first time and would do it again.', 'category': 'Fun', 'published': True, 'id': post_id3}]}

def test_update_all_posts():
    response1 = client.post("/linkedinposts", json=post_example)
    assert response1.status_code == 201
    post_id1 = response1.json()['data']['id']
    assert response1.json() == {'data': {"title": "Vacation on the beach", "content": "I just got back from vacation and I'm so stressed.", "category": "Lifestyle", "published": True, "id": post_id1}}
    response2 = client.post("/linkedinposts", json=post_example2)
    assert response2.status_code == 201
    post_id2 = response2.json()['data']['id']
    response3 = client.post("/linkedinposts", json=post_example3)
    assert response3.status_code == 201
    post_id3 = response3.json()['data']['id']
    response4 = client.put("/linkedinposts", json={"title": "New Title", "content": "New Content", "category": "New Category", "published": False})
    assert response4.status_code == 200
    assert response4.json() == {'message': 'All posts successfully updated', 'Updated Posts': [{'title': 'New Title', 'content': 'New Content', 'category': 'New Category', 'published': False, 'id': post_id1}, {'title': 'New Title', 'content': 'New Content', 'category': 'New Category', 'published': False, 'id': post_id2}, {'title': 'New Title', 'content': 'New Content', 'category': 'New Category', 'published': False, 'id': post_id3}]}

def test_update_all_posts_with_empty_linkedin_posts_list():
    response = client.put("/linkedinposts", json={"title": "New Title", "content": "New Content", "category": "New Category", "published": False})
    assert response.status_code == 404
    assert response.json()['detail'] == 'Error: No posts found'

def test_update_all_posts_with_extra_json_fields():
    response1 = client.post("/linkedinposts", json=post_example)
    assert response1.status_code == 201
    post_id1 = response1.json()['data']['id']
    assert response1.json() == {'data': {"title": "Vacation on the beach", "content": "I just got back from vacation and I'm so stressed.", "category": "Lifestyle", "published": True, "id": post_id1}}
    response2 = client.post("/linkedinposts", json=post_example2)
    assert response2.status_code == 201
    post_id2 = response2.json()['data']['id']
    response3 = client.post("/linkedinposts", json=post_example3)
    assert response3.status_code == 201
    post_id3 = response3.json()['data']['id']
    response4 = client.put("/linkedinposts", json={"title": "New Title", "likes": 30, "comments": 40, "shares": 100, "content": "New Content", "category": "New Category", "published": False})
    assert response4.status_code == 200
    assert response4.json() == {'message': 'All posts successfully updated', 'Updated Posts': [{'title': 'New Title', 'content': 'New Content', 'category': 'New Category', 'published': False, 'id': post_id1}, {'title': 'New Title', 'content': 'New Content', 'category': 'New Category', 'published': False, 'id': post_id2}, {'title': 'New Title', 'content': 'New Content', 'category': 'New Category', 'published': False, 'id': post_id3}]}

def test_update_all_posts_with_invalid_fields_only():
    response1 = client.post("/linkedinposts", json=post_example)
    assert response1.status_code == 201
    post_id1 = response1.json()['data']['id']
    assert response1.json() == {'data': {"title": "Vacation on the beach", "content": "I just got back from vacation and I'm so stressed.", "category": "Lifestyle", "published": True, "id": post_id1}}
    response2 = client.post("/linkedinposts", json=post_example2)
    assert response2.status_code == 201
    response3 = client.post("/linkedinposts", json=post_example3)
    assert response3.status_code == 201
    response4 = client.put("/linkedinposts", json={"likes": 30, "comments": 40, "shares": 100})
    assert response4.status_code == 422
    assert response4.json()['detail'] == [{'type': 'missing', 'loc': ['body', 'title'], 'msg': 'Field required', 'input': {'likes': 30, 'comments': 40, 'shares': 100}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}, {'type': 'missing', 'loc': ['body', 'content'], 'msg': 'Field required', 'input': {'likes': 30, 'comments': 40, 'shares': 100}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}, {'type': 'missing', 'loc': ['body', 'category'], 'msg': 'Field required', 'input': {'likes': 30, 'comments': 40, 'shares': 100}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}]

def test_update_all_posts_with_empty_body():
    response1 = client.post("/linkedinposts", json=post_example)
    assert response1.status_code == 201
    post_id1 = response1.json()['data']['id']
    assert response1.json() == {'data': {"title": "Vacation on the beach", "content": "I just got back from vacation and I'm so stressed.", "category": "Lifestyle", "published": True, "id": post_id1}}
    response2 = client.post("/linkedinposts", json=post_example2)
    assert response2.status_code == 201
    response3 = client.post("/linkedinposts", json=post_example3)
    assert response3.status_code == 201
    response4 = client.put("/linkedinposts", json={})
    assert response4.status_code == 422
    assert response4.json()['detail'] == [{'type': 'missing', 'loc': ['body', 'title'], 'msg': 'Field required', 'input': {}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}, {'type': 'missing', 'loc': ['body', 'content'], 'msg': 'Field required', 'input': {}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}, {'type': 'missing', 'loc': ['body', 'category'], 'msg': 'Field required', 'input': {}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}]

def test_delete_all_posts_on_empty_linkedinposts_list():
    response = client.delete("/linkedinposts")
    assert response.status_code == 404
    assert response.json()['detail'] == "Error: No posts found"

def test_delete_all_posts_on_populated_linkedinposts_list():
    response1 = client.post("/linkedinposts", json=post_example)
    assert response1.status_code == 201
    post_id1 = response1.json()['data']['id']
    assert response1.json() == {'data': {"title": "Vacation on the beach", "content": "I just got back from vacation and I'm so stressed.", "category": "Lifestyle", "published": True, "id": post_id1}}
    response = client.delete("/linkedinposts")
    assert response.status_code == 200
    print(response.json())
    assert response.json() == {'message': 'All posts deleted'}

def test_get_posts_pagination():
    # Create more than 10 posts
    for _ in range(15):
        client.post("/linkedinposts", json=post_example)
    # Test retrieving posts from different pages
    response_page_1 = client.get("/linkedinposts?page=1&page_size=10")
    response_page_2 = client.get("/linkedinposts?page=2&page_size=10")
    assert response_page_1.status_code == 200
    assert len(response_page_1.json()['data']) == 10
    assert response_page_2.status_code == 200
    assert len(response_page_2.json()['data']) == 5  # Remaining posts

def test_get_posts_invalid_pagination():
    response1 = client.post("/linkedinposts", json=post_example)
    assert response1.status_code == 201
    # Test with negative page number
    response = client.get("/linkedinposts?page=-1")
    assert response.status_code == 400
    assert "Invalid page number. Must be integer greater than 0." in response.json()['detail']
    # Test with negative page size
    response = client.get("/linkedinposts?page_size=-10")
    assert response.status_code == 400
    assert "Invalid page size. Must be integer greater than 0." in response.json()['detail']

def test_partial_update_post_and_validate_error_handling():
    response1 = client.post("/linkedinposts", json=post_example)
    assert response1.status_code == 201
    post_id1 = response1.json()['data']['id']
    assert response1.json() == {'data': {"title": "Vacation on the beach", "content": "I just got back from vacation and I'm so stressed.", "category": "Lifestyle", "published": True, "id": post_id1}}
    # Update only the title of the post
    response2 = client.put("/linkedinposts/" + str(post_id1), json={"title": "Updated Title"})
    assert response2.status_code == 422
    assert response2.json() == {'detail': [{'type': 'missing', 'loc': ['body', 'content'], 'msg': 'Field required', 'input': {'title': 'Updated Title'}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}, {'type': 'missing', 'loc': ['body', 'category'], 'msg': 'Field required', 'input': {'title': 'Updated Title'}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}]}

def test_delete_nonexistent_post():
    response = client.delete("/linkedinposts/999")  # Assuming ID 999 does not exist
    assert response.status_code == 404
    assert "error: no posts found" in response.json()['detail'].lower()

def test_delete_all_posts_with_existing_posts():
    # Create some posts
    for _ in range(5):
        client.post("/linkedinposts", json=post_example)
    response = client.delete("/linkedinposts")
    assert response.status_code == 200
    assert response.json()['message'] == "All posts deleted"

def test_get_latest_post_no_posts():
    response = client.get("/linkedinposts/latest")
    assert response.status_code == 404
    assert "no posts found" in response.json()['detail'].lower()


