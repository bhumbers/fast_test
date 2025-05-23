from backend.schemas import User, Post, Comment


def test_create_and_read_comment(client):
    # First create a user
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

    # Create a comment
    comment_data = {
        "text": "This is a test comment!"
    }
    comment_response = client.post(
        f"/comments/?post_id={created_post.id}&user_id={created_user.id}", 
        json=comment_data
    )
    assert comment_response.status_code == 200, comment_response.text
    created_comment = Comment(**comment_response.json())
    assert created_comment.text == comment_data["text"]
    assert created_comment.post_id == created_post.id
    assert created_comment.user_id == created_user.id

    # Read comments for the post
    comments_response = client.get(f"/posts/{created_post.id}/comments/")
    assert comments_response.status_code == 200, comments_response.text
    comments = [Comment(**comment) for comment in comments_response.json()]
    assert len(comments) == 1
    assert comments[0].id == created_comment.id
    assert comments[0].text == created_comment.text


def test_read_multiple_comments_with_ordering(client):
    # Create user and post
    user_data = {
        "email": "testuser2@example.com",
        "password": "password123",
        "username": "testuser2"
    }
    user_response = client.post("/users/", json=user_data)
    created_user = User(**user_response.json())

    post_data = {
        "image_url": "https://example.com/image.jpg",
        "caption": "Test post caption"
    }
    post_response = client.post(f"/posts/?owner_id={created_user.id}", json=post_data)
    created_post = Post(**post_response.json())

    # Create multiple comments
    comment_texts = ["First comment", "Second comment", "Third comment"]
    created_comments = []
    
    for text in comment_texts:
        comment_data = {"text": text}
        comment_response = client.post(
            f"/comments/?post_id={created_post.id}&user_id={created_user.id}", 
            json=comment_data
        )
        assert comment_response.status_code == 200
        created_comments.append(Comment(**comment_response.json()))

    # Read all comments - should be ordered by created_at desc (newest first)
    comments_response = client.get(f"/posts/{created_post.id}/comments/")
    assert comments_response.status_code == 200
    comments = [Comment(**comment) for comment in comments_response.json()]
    assert len(comments) == 3
    
    # Comments should be in reverse order (newest first)
    assert comments[0].text == "Third comment"
    assert comments[1].text == "Second comment" 
    assert comments[2].text == "First comment"


def test_read_comments_with_limit(client):
    # Create user and post
    user_data = {
        "email": "testuser3@example.com",
        "password": "password123",
        "username": "testuser3"
    }
    user_response = client.post("/users/", json=user_data)
    created_user = User(**user_response.json())

    post_data = {
        "image_url": "https://example.com/image.jpg",
        "caption": "Test post caption"
    }
    post_response = client.post(f"/posts/?owner_id={created_user.id}", json=post_data)
    created_post = Post(**post_response.json())

    # Create 5 comments
    for i in range(5):
        comment_data = {"text": f"Comment {i+1}"}
        comment_response = client.post(
            f"/comments/?post_id={created_post.id}&user_id={created_user.id}", 
            json=comment_data
        )
        assert comment_response.status_code == 200

    # Read comments with limit of 3
    comments_response = client.get(f"/posts/{created_post.id}/comments/?limit=3")
    assert comments_response.status_code == 200
    comments = [Comment(**comment) for comment in comments_response.json()]
    assert len(comments) == 3

    # Should get the 3 most recent comments
    assert comments[0].text == "Comment 5"
    assert comments[1].text == "Comment 4"
    assert comments[2].text == "Comment 3"


def test_create_comment_with_nonexistent_post(client):
    # Create a user first
    user_data = {
        "email": "testuser4@example.com",
        "password": "password123",
        "username": "testuser4"
    }
    user_response = client.post("/users/", json=user_data)
    created_user = User(**user_response.json())

    # Try to create comment on non-existent post
    comment_data = {"text": "This comment won't work"}
    comment_response = client.post(
        f"/comments/?post_id=999999&user_id={created_user.id}", 
        json=comment_data
    )
    assert comment_response.status_code == 404
    assert "Post not found" in comment_response.json()["detail"]


def test_create_comment_with_nonexistent_user(client):
    # Create a post first
    user_data = {
        "email": "testuser5@example.com",
        "password": "password123",
        "username": "testuser5"
    }
    user_response = client.post("/users/", json=user_data)
    created_user = User(**user_response.json())

    post_data = {
        "image_url": "https://example.com/image.jpg",
        "caption": "Test post caption"
    }
    post_response = client.post(f"/posts/?owner_id={created_user.id}", json=post_data)
    created_post = Post(**post_response.json())

    # Try to create comment with non-existent user
    comment_data = {"text": "This comment won't work"}
    comment_response = client.post(
        f"/comments/?post_id={created_post.id}&user_id=999999", 
        json=comment_data
    )
    assert comment_response.status_code == 404
    assert "User not found" in comment_response.json()["detail"]


def test_read_comments_for_nonexistent_post(client):
    # Try to read comments for non-existent post
    comments_response = client.get("/posts/999999/comments/")
    assert comments_response.status_code == 404
    assert "Post not found" in comments_response.json()["detail"]


def test_read_comments_for_post_with_no_comments(client):
    # Create user and post
    user_data = {
        "email": "testuser6@example.com",
        "password": "password123",
        "username": "testuser6"
    }
    user_response = client.post("/users/", json=user_data)
    created_user = User(**user_response.json())

    post_data = {
        "image_url": "https://example.com/image.jpg",
        "caption": "Test post with no comments"
    }
    post_response = client.post(f"/posts/?owner_id={created_user.id}", json=post_data)
    created_post = Post(**post_response.json())

    # Read comments for post with no comments
    comments_response = client.get(f"/posts/{created_post.id}/comments/")
    assert comments_response.status_code == 200
    comments = comments_response.json()
    assert len(comments) == 0
    assert comments == []


def test_create_comment_with_empty_text(client):
    # Create user and post
    user_data = {
        "email": "testuser7@example.com",
        "password": "password123",
        "username": "testuser7"
    }
    user_response = client.post("/users/", json=user_data)
    created_user = User(**user_response.json())

    post_data = {
        "image_url": "https://example.com/image.jpg",
        "caption": "Test post caption"
    }
    post_response = client.post(f"/posts/?owner_id={created_user.id}", json=post_data)
    created_post = Post(**post_response.json())

    # Try to create comment with empty text
    comment_data = {"text": ""}
    comment_response = client.post(
        f"/comments/?post_id={created_post.id}&user_id={created_user.id}", 
        json=comment_data
    )
    # Should still work - the API doesn't currently validate empty text
    # but we could add validation if needed
    assert comment_response.status_code == 200
    created_comment = Comment(**comment_response.json())
    assert created_comment.text == ""
