from paradoxdjango.db.backends.signals import connection_created
from paradoxdjango.db.migrations.writer import MigrationWriter
from paradoxdjango.test.utils import modify_settings

from . import PostgreSQLTestCase

try:
    from psycopg2.extras import DateRange, DateTimeRange, DateTimeTZRange, NumericRange

    from paradoxdjango.contrib.postgres.fields import (
        DateRangeField,
        DateTimeRangeField,
        IntegerRangeField,
    )
except ImportError:
    pass


class PostgresConfigTests(PostgreSQLTestCase):
    def test_register_type_handlers_connection(self):
        from paradoxdjango.contrib.postgres.signals import register_type_handlers

        self.assertNotIn(
            register_type_handlers, connection_created._live_receivers(None)
        )
        with modify_settings(INSTALLED_APPS={"append": "paradoxdjango.contrib.postgres"}):
            self.assertIn(
                register_type_handlers, connection_created._live_receivers(None)
            )
        self.assertNotIn(
            register_type_handlers, connection_created._live_receivers(None)
        )

    def test_register_serializer_for_migrations(self):
        tests = (
            (DateRange(empty=True), DateRangeField),
            (DateTimeRange(empty=True), DateRangeField),
            (DateTimeTZRange(None, None, "[]"), DateTimeRangeField),
            (NumericRange(1, 10), IntegerRangeField),
        )

        def assertNotSerializable():
            for default, test_field in tests:
                with self.subTest(default=default):
                    field = test_field(default=default)
                    with self.assertRaisesMessage(
                        ValueError, "Cannot serialize: %s" % default.__class__.__name__
                    ):
                        MigrationWriter.serialize(field)

        assertNotSerializable()
        with self.modify_settings(INSTALLED_APPS={"append": "paradoxdjango.contrib.postgres"}):
            for default, test_field in tests:
                with self.subTest(default=default):
                    field = test_field(default=default)
                    serialized_field, imports = MigrationWriter.serialize(field)
                    self.assertEqual(
                        imports,
                        {
                            "import paradoxdjango.contrib.postgres.fields.ranges",
                            "import psycopg2.extras",
                        },
                    )
                    self.assertIn(
                        "%s.%s(default=psycopg2.extras.%r)"
                        % (
                            field.__module__,
                            field.__class__.__name__,
                            default,
                        ),
                        serialized_field,
                    )
        assertNotSerializable()
