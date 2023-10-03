import pytest
import app.schemas as schemas
from jose import jwt
from app.config import settings


def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == "Hello World!"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/",json={"email":"hello@gmail.com","password":"password123"})
    new_user = schemas.userOut(**res.json())
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201
    print(res.json)

def test_login_user(client,test_user):
    res = client.post("/login", data ={"username":test_user['email'],"password":test_user['password']} )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, [settings.ALGO])
    id:int = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('surya234@gmail.com','12311',403),
    (None,None,422),
    ("12AAAMMMMxaaaany","rubbish",403)])
def test_incorrect_login(test_user,client,email,password,status_code):
    res = client.post("/login", data = {"username": email, "password":password})

    assert res.status_code == status_code
    #assert res.json().get('detail') == "Invalid credentials"