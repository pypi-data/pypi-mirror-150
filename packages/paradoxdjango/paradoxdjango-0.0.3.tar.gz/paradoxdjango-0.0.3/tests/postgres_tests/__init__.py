import unittest

from forms_tests.widget_tests.base import WidgetTest

from paradoxdjango.db import connection
from paradoxdjango.test import SimpleTestCase, TestCase, modify_settings


@unittest.skipUnless(connection.vendor == "postgresql", "PostgreSQL specific tests")
class PostgreSQLSimpleTestCase(SimpleTestCase):
    pass


@unittest.skipUnless(connection.vendor == "postgresql", "PostgreSQL specific tests")
class PostgreSQLTestCase(TestCase):
    pass


@unittest.skipUnless(connection.vendor == "postgresql", "PostgreSQL specific tests")
# To locate the widget's template.
@modify_settings(INSTALLED_APPS={"append": "paradoxdjango.contrib.postgres"})
class PostgreSQLWidgetTestCase(WidgetTest, PostgreSQLSimpleTestCase):
    pass
