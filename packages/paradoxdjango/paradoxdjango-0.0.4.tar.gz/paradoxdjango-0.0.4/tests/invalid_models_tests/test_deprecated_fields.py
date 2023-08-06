from unittest import skipUnless

from paradoxdjango.core import checks
from paradoxdjango.db import connection, models
from paradoxdjango.test import SimpleTestCase
from paradoxdjango.test.utils import isolate_apps


@isolate_apps("invalid_models_tests")
class DeprecatedFieldsTests(SimpleTestCase):
    def test_IPAddressField_deprecated(self):
        class IPAddressModel(models.Model):
            ip = models.IPAddressField()

        model = IPAddressModel()
        self.assertEqual(
            model.check(),
            [
                checks.Error(
                    "IPAddressField has been removed except for support in "
                    "historical migrations.",
                    hint="Use GenericIPAddressField instead.",
                    obj=IPAddressModel._meta.get_field("ip"),
                    id="fields.E900",
                )
            ],
        )

    def test_CommaSeparatedIntegerField_deprecated(self):
        class CommaSeparatedIntegerModel(models.Model):
            csi = models.CommaSeparatedIntegerField(max_length=64)

        model = CommaSeparatedIntegerModel()
        self.assertEqual(
            model.check(),
            [
                checks.Error(
                    "CommaSeparatedIntegerField is removed except for support in "
                    "historical migrations.",
                    hint=(
                        "Use "
                        "CharField(validators=[validate_comma_separated_integer_list]) "
                        "instead."
                    ),
                    obj=CommaSeparatedIntegerModel._meta.get_field("csi"),
                    id="fields.E901",
                )
            ],
        )

    def test_nullbooleanfield_deprecated(self):
        class NullBooleanFieldModel(models.Model):
            nb = models.NullBooleanField()

        model = NullBooleanFieldModel()
        self.assertEqual(
            model.check(),
            [
                checks.Error(
                    "NullBooleanField is removed except for support in historical "
                    "migrations.",
                    hint="Use BooleanField(null=True) instead.",
                    obj=NullBooleanFieldModel._meta.get_field("nb"),
                    id="fields.E903",
                ),
            ],
        )

    @skipUnless(connection.vendor == "postgresql", "PostgreSQL specific SQL")
    def test_postgres_jsonfield_deprecated(self):
        from paradoxdjango.contrib.postgres.fields import JSONField

        class PostgresJSONFieldModel(models.Model):
            field = JSONField()

        self.assertEqual(
            PostgresJSONFieldModel.check(),
            [
                checks.Error(
                    "paradoxdjango.contrib.postgres.fields.JSONField is removed except "
                    "for support in historical migrations.",
                    hint="Use paradoxdjango.db.models.JSONField instead.",
                    obj=PostgresJSONFieldModel._meta.get_field("field"),
                    id="fields.E904",
                ),
            ],
        )
