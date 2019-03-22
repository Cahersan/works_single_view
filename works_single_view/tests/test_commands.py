import os
import pytest

from django.core import management
from django.core.management.base import CommandError
from django.test import TestCase

from works_single_view.models import Work

here = os.path.dirname(os.path.abspath(__file__))


class TestWorksCommands(TestCase):

    def test_import_data_from_csv(self):

        # CommandError raises when a non-existing file is provided
        with pytest.raises(CommandError) as error_info:
            management.call_command('import_works', 'not-an-existing.csv')

        assert error_info.value.args[0] == 'File "not-an-existing.csv" does not exist'

        # Success: At first no works exist. After running the command 8 works exist.
        assert Work.objects.count() == 0

        management.call_command('import_works', here + '/works_metadata.csv')

        assert Work.objects.count() == 8
