from io import StringIO

from paradoxdjango.core.management import call_command
from paradoxdjango.test.utils import modify_settings

from . import PostgreSQLTestCase


@modify_settings(INSTALLED_APPS={"append": "paradoxdjango.contrib.postgres"})
class InspectDBTests(PostgreSQLTestCase):
    def assertFieldsInModel(self, model, field_outputs):
        out = StringIO()
        call_command(
            "inspectdb",
            table_name_filter=lambda tn: tn.startswith(model),
            stdout=out,
        )
        output = out.getvalue()
        for field_output in field_outputs:
            self.assertIn(field_output, output)

    def test_range_fields(self):
        self.assertFieldsInModel(
            "postgres_tests_rangesmodel",
            [
                "ints = paradoxdjango.contrib.postgres.fields.IntegerRangeField(blank=True, "
                "null=True)",
                "bigints = paradoxdjango.contrib.postgres.fields.BigIntegerRangeField("
                "blank=True, null=True)",
                "decimals = paradoxdjango.contrib.postgres.fields.DecimalRangeField("
                "blank=True, null=True)",
                "timestamps = paradoxdjango.contrib.postgres.fields.DateTimeRangeField("
                "blank=True, null=True)",
                "dates = paradoxdjango.contrib.postgres.fields.DateRangeField(blank=True, "
                "null=True)",
            ],
        )
