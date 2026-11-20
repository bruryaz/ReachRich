import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.core.database import get_auth_client
from app.main import app


def make_user():
    return SimpleNamespace(
        id="user-123",
        email="person@example.com",
        user_metadata={"first_name": "Ada", "last_name": "Lovelace"},
    )


def make_session():
    return SimpleNamespace(
        access_token="access-token",
        refresh_token="refresh-token",
        token_type="bearer",
        expires_in=3600,
    )


class AuthenticationApiTests(unittest.TestCase):
    def setUp(self):
        self.auth = Mock()
        self.client = TestClient(app)
        app.dependency_overrides[get_auth_client] = lambda: SimpleNamespace(auth=self.auth)

    def tearDown(self):
        app.dependency_overrides.clear()

    def test_register_returns_user_and_session(self):
        self.auth.sign_up.return_value = SimpleNamespace(user=make_user(), session=make_session())

        response = self.client.post(
            "/auth/register",
            json={
                "email": " Person@Example.com ",
                "password": "secure-password",
                "first_name": "Ada",
                "last_name": "Lovelace",
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["user"]["email"], "person@example.com")
        self.assertEqual(response.json()["session"]["access_token"], "access-token")
        self.auth.sign_up.assert_called_once_with(
            {
                "email": "person@example.com",
                "password": "secure-password",
                "options": {"data": {"first_name": "Ada", "last_name": "Lovelace"}},
            }
        )

    def test_register_handles_email_confirmation(self):
        self.auth.sign_up.return_value = SimpleNamespace(user=make_user(), session=None)

        response = self.client.post(
            "/auth/register",
            json={"email": "person@example.com", "password": "secure-password"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertIsNone(response.json()["session"])
        self.assertIn("Check your email", response.json()["message"])

    def test_login_returns_session_tokens(self):
        self.auth.sign_in_with_password.return_value = SimpleNamespace(
            user=make_user(),
            session=make_session(),
        )

        response = self.client.post(
            "/auth/login",
            json={"email": "person@example.com", "password": "secure-password"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["access_token"], "access-token")
        self.assertEqual(response.json()["user"]["first_name"], "Ada")

    def test_me_requires_and_validates_bearer_token(self):
        missing_token_response = self.client.get("/auth/me")
        self.assertEqual(missing_token_response.status_code, 401)

        self.auth.get_user.return_value = SimpleNamespace(user=make_user())
        response = self.client.get(
            "/auth/me",
            headers={"Authorization": "Bearer access-token"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], "user-123")
        self.auth.get_user.assert_called_once_with("access-token")

    def test_refresh_returns_rotated_tokens(self):
        self.auth.refresh_session.return_value = SimpleNamespace(user=make_user(), session=make_session())

        response = self.client.post("/auth/refresh", json={"refresh_token": "old-refresh-token"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["refresh_token"], "refresh-token")
        self.auth.refresh_session.assert_called_once_with("old-refresh-token")

    def test_logout_revokes_the_current_refresh_session(self):
        self.auth.refresh_session.return_value = SimpleNamespace(user=make_user(), session=make_session())

        response = self.client.post("/auth/logout", json={"refresh_token": "refresh-token"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Signed out successfully.")
        self.auth.sign_out.assert_called_once_with({"scope": "local"})


if __name__ == "__main__":
    unittest.main()
