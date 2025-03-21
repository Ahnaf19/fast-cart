import unittest

from app.main import app
from fastapi.testclient import TestClient


class TestRouter(unittest.TestCase):
    client: TestClient

    @classmethod
    def setup_class(cls) -> None:
        """
        Setup the test client and initial data for the tests.
        """
        cls.client = TestClient(app)

    def test_read_data(self) -> None:
        """
        Test reading all data.
        """
        response = self.client.get("/group/")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"message": "ok"})
