from paradoxdjango.test import SimpleTestCase
from paradoxdjango.utils.connection import BaseConnectionHandler


class BaseConnectionHandlerTests(SimpleTestCase):
    def test_create_connection(self):
        handler = BaseConnectionHandler()
        msg = "Subclasses must implement create_connection()."
        with self.assertRaisesMessage(NotImplementedError, msg):
            handler.create_connection(None)
