import pytest
from fastapi.testclient import TestClient
from main import app 

# TestClient를 사용해 FastAPI 앱을 테스트할 수 있도록 설정
client = TestClient(app)

# 지연 임포트로 순환 import 문제 해결
def get_app():
    from main import app
    return app

client = TestClient(get_app())

def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "welcome to Tharm"}



@pytest.fixture
def test_user_data():
    return {
        "email": "testuser@example.com",
        "name": "Test User",
        "password": "securepassword",
        "phone": "123-456-7890"
    }

# 홈 페이지 테스트
def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "welcome to Tharm"}
    print('웰컴이요~~')

# 회원가입 테스트
def test_create_user(test_user_data):
    response = client.post("/create/user", json=test_user_data)
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}

# 로그인 테스트
def test_login(test_user_data):
    # 우선 회원가입을 먼저 수행해야 로그인 테스트가 가능합니다.
    client.post("/create/user", json=test_user_data)
    print('로그인 시도 ㄱㄱㄱ')
    # 로그인 시도
    login_data = {"email": test_user_data["email"], "password": test_user_data["password"]}
    response = client.post("/user/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "Bearer"

# 잘못된 비밀번호로 로그인 시도 테스트
def test_login_invalid_password(test_user_data):
    # 회원가입
    client.post("/create/user", json=test_user_data)
    print('회원가입~~')
    # 잘못된 비밀번호로 로그인 시도
    invalid_login_data = {"email": test_user_data["email"], "password": "wrongpassword"}
    response = client.post("/user/login", json=invalid_login_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "이메일 또는 비밀번호가 유효하지 않습니다."}

# 사용자 조회 테스트
def test_get_user(test_user_data):
    # 우선 회원가입을 먼저 수행해야 사용자 조회가 가능합니다.
    response = client.post("/create/user", json=test_user_data)
    
    # Firebase에서 생성된 uid를 가져오기 위해 Firebase Admin SDK를 사용해야 할 수도 있습니다.
    # 여기에선 일단 회원가입이 성공했다는 가정 하에 테스트를 작성합니다.
    
    user_id = response.json().get("id")  # 예시로 id를 response에서 가져왔다고 가정
    if user_id:
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        assert "email" in response.json()
        assert response.json()["email"] == test_user_data["email"]
        print('나왔다 끗')
    else:
        pytest.fail("User ID not returned in the response")
