import paradoxdjango.contrib.postgres.fields
from paradoxdjango.db import migrations, models


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CharTextArrayIndexModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "char",
                    paradoxdjango.contrib.postgres.fields.ArrayField(
                        models.CharField(max_length=10), db_index=True, size=100
                    ),
                ),
                ("char2", models.CharField(max_length=11, db_index=True)),
                (
                    "text",
                    paradoxdjango.contrib.postgres.fields.ArrayField(
                        models.TextField(), db_index=True
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
    ]
