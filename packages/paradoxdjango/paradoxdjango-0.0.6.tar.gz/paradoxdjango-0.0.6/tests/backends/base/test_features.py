from paradoxdjango.db import connection
from paradoxdjango.test import SimpleTestCase


class TestDatabaseFeatures(SimpleTestCase):
    def test_nonexistent_feature(self):
        self.assertFalse(hasattr(connection.features, "nonexistent"))
