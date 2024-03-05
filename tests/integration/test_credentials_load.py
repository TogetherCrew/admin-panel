from unittest import TestCase

from utils.creds import get_mongo_credentials


class TestLoadCredentials(TestCase):
    def test_creds_non_empty(self):
        creds = get_mongo_credentials()

        self.assertIsNotNone(creds["user"])
        self.assertIsNotNone(creds["password"])
        self.assertIsNotNone(creds["host"])
        self.assertIsNotNone(creds["port"])
        self.assertNotEqual(creds["connection_str"], "mongodb://None:None@None:None")
