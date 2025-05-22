from backend.schemas import User, Post


def test_create_and_read_post(client):
    # First create a user to own the post
    user_data = {
        "email": "testuser@example.com",
        "password": "password123",
        "username": "testuser"
    }
    user_response = client.post("/users/", json=user_data)
    assert user_response.status_code == 200, user_response.text
    created_user = User(**user_response.json())

    # Create a post
    post_data = {
        "image_url": "https://example.com/image.jpg",
        "caption": "Test post caption"
    }
    post_response = client.post(f"/posts/?owner_id={created_user.id}", json=post_data)
    assert post_response.status_code == 200, post_response.text
    created_post = Post(**post_response.json())
    assert created_post.image_url == post_data["image_url"]
    assert created_post.caption == post_data["caption"]
    assert created_post.owner_id == created_user.id

    # Read the post back
    read_response = client.get(f"/posts/{created_post.id}")
    assert read_response.status_code == 200, read_response.text
    read_post = Post(**read_response.json())
    assert read_post.id == created_post.id
    assert read_post.image_url == created_post.image_url
    assert read_post.caption == created_post.caption
    assert read_post.owner_id == created_post.owner_id

def test_read_all_posts(client):
    # Create a user
    user_data = {
        "email": "testuser2@example.com",
        "password": "password123",
        "username": "testuser2"
    }
    user_response = client.post("/users/", json=user_data)
    assert user_response.status_code == 200, user_response.text
    created_user = User(**user_response.json())

    # Create multiple posts
    post_data_1 = {
        "image_url": "https://example.com/image1.jpg",
        "caption": "First test post"
    }
    post_data_2 = {
        "image_url": "https://example.com/image2.jpg", 
        "caption": "Second test post"
    }

    post_response_1 = client.post(f"/posts/?owner_id={created_user.id}", json=post_data_1)
    post_response_2 = client.post(f"/posts/?owner_id={created_user.id}", json=post_data_2)
    assert post_response_1.status_code == 200, post_response_1.text
    assert post_response_2.status_code == 200, post_response_2.text

    # Read all posts
    all_posts_response = client.get("/posts/")
    assert all_posts_response.status_code == 200, all_posts_response.text
    all_posts = [Post(**post) for post in all_posts_response.json()]
    
    # Should have at least our 2 posts (may have more from other tests)
    assert len(all_posts) >= 2

def test_create_post_with_nonexistent_user(client):
    post_data = {
        "image_url": "https://example.com/image.jpg",
        "caption": "Test post caption"
    }
    # Try to create post with non-existent user ID
    post_response = client.post("/posts/?owner_id=999999", json=post_data)
    assert post_response.status_code == 404, post_response.text
    assert "User not found" in post_response.json()["detail"]

def test_read_nonexistent_post(client):
    # Try to read non-existent post
    read_response = client.get("/posts/999999")
    assert read_response.status_code == 404, read_response.text
    assert "Post not found" in read_response.json()["detail"]
