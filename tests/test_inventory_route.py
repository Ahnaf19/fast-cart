import unittest

from fastapi.testclient import TestClient

from inventory.app.main import app

# from httpx import ASGITransport


class TestRouter(unittest.TestCase):
    client: TestClient

    @classmethod
    def setup_class(cls) -> None:
        """
        Setup the test client and initial data for the tests.
        """
        # TODO: fix the deprecation warning for ASGITransport
        cls.client = TestClient(app)

    def test_read_data(self) -> None:
        """
        Test reading all data.
        """
        response = self.client.get("/group/")
        self.assertEqual(response.status_code, 404)
        self.assertDictEqual(response.json(), {"detail": "Not Found"})
