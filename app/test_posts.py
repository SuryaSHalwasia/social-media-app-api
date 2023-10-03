from typing import List
from app.schemas import postOut, Post
import pytest
def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return postOut(**post)
    
    posts_map = map(validate, res.json())
    print(list(posts_map))
    post_list = list(posts_map)
    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get("/posts/{}".format(test_posts[0].id))
    print(len(res.json()))
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client,test_posts):
        res = authorized_client.get("/posts/999")
        
        assert res.status_code == 404

def test_get_one_post(authorized_client,test_posts):
    res = authorized_client.get("/posts/{}".format(test_posts[0].id))
    print(res.json())
    post = postOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.body == test_posts[0].body
    assert post.Post.title == test_posts[0].title

@pytest.mark.parametrize("title,body, published",[
     ("One day in Jersey", "I visited New Jersey", True),
     ("I played soccer", "I had the chance to play soccer", True),
     ("I ate pizza on my date", "It was cheesy", False)
])
def test_create_post(authorized_client,test_user,test_posts, title, body, published):
     res = authorized_client.post("/posts", json={"title":title,"body":body,"published":published})
     created_post = Post(**res.json())
     assert res.status_code == 201
     assert created_post.title == title
     assert created_post.body == body
     assert created_post.published == published
     assert created_post.user_id == test_user["id"]

def test_create_post_default_published(authorized_client,test_user,test_posts):
     res = authorized_client.post("/posts", json={"title":"My favorite instrument","body":"Violin, hands down"})
     created_post = Post(**res.json())
     assert res.status_code == 201
     assert created_post.title == "My favorite instrument"
     assert created_post.body == "Violin, hands down"
     assert created_post.published == True
     assert created_post.user_id == test_user["id"]

def test_unauthorized_user_post_one_post(client, test_user, test_posts):
    res = client.post("/posts", json={"title":"My favorite instrument","body":"Violin, hands down"})
    print(len(res.json()))
    assert res.status_code == 401

def test_unauthorized_delete_post(client,test_posts,test_user):
    res = client.delete("/posts/{}".format(test_posts[0].id))
    assert res.status_code == 401
     
def test_authorized_delete_post(authorized_client,test_posts,test_user):
    res = authorized_client.delete("/posts/{}".format(test_posts[0].id))
    assert res.status_code == 204

def test_delete_non_exist_post(authorized_client,test_posts,test_user):
     res = authorized_client.delete("/posts/222222")
     assert res.status_code == 404

def test_delete_other_user_post(authorized_client,test_posts,test_user):
     res = authorized_client.delete("/posts/{}".format(test_posts[2].id))
     assert res.status_code == 403

def test_update_post(authorized_client,test_posts,test_user):
     data = {
          "title":"My favorite book",
          "body":"I change my mind. My fav book is Guliver's Travels",
          "id":test_posts[0].id
     }
     res = authorized_client.put("/posts/{}".format(test_posts[0].id), json=data)
     updated_post = Post(**res.json())
     assert res.status_code == 200
     assert updated_post.title == data["title"]
     assert updated_post.body == data["body"]

def test_update_other_post(authorized_client,test_posts,test_user,test_user_second):
     data = {
          "title":"My favorite book",
          "body":"I change my mind. My fav book is Guliver's Travels",
          "id":test_posts[2].id
     }
     res = authorized_client.put("/posts/{}".format(test_posts[2].id), json=data)
     assert res.status_code == 403


def test_unauthorized_update_post(client,test_posts,test_user):
    data = {
          "title":"My favorite book",
          "body":"I change my mind. My fav book is Guliver's Travels",
          "id":test_posts[0].id
     }
    res = client.put("/posts/{}".format(test_posts[0].id), json=data)
    assert res.status_code == 401