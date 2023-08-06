from unittest import mock

from paradoxdjango.db import migrations

try:
    from paradoxdjango.contrib.postgres.operations import CryptoExtension
except ImportError:
    CryptoExtension = mock.Mock()


class Migration(migrations.Migration):
    # Required for the SHA database functions.
    operations = [CryptoExtension()]
