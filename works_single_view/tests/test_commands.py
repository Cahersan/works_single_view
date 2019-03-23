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

        # From introspecting the works_metadata.csv file, 4 different works should
        # result from import
        assert Work.objects.count() == 4

        # Now lets see if the data in the database is what we expected
        expected = [
            {
                'title': 'Adventure of a Lifetime',
                'contributors': [
                    'O Brien Edward John',
                    'Yorke Thomas Edward',
                    'Greenwood Colin Charles',
                    'Selway Philip James'
                ],
                'iswc':'T0101974597',
                'source':'warner',
                'source_id':2,
                'alternate':{
                    'iswc': [],
                    'title':[],
                    'source':[],
                    'source_id':['3'],
                }
            },
            {
                'title': 'Me Enamoré',
                'contributors': [
                    'Rayo Gibo Antonio',
                    'Ripoll Shakira Isabel Mebarak'
                ],
                'iswc':'T9214745718',
                'source':'universal',
                'source_id':1,
                'alternate':{
                    'iswc': [],
                    'title':['Me Enamore'],
                    'source':['warner'],
                    'source_id':['4'],
                }
            },
            {
                'title': 'Je ne sais pas',
                'contributors': [
                    'Obispo Pascal Michel',
                    'Florence Lionel Jacques'
                ],
                'iswc':'T0046951705',
                'source':'sony',
                'source_id':2,
                'alternate':{
                    'iswc': [],
                    'title':[],
                    'source':[],
                    'source_id':['3'],
                }
            },
            {
                'title': 'Shape of You',
                'contributors': [
                    'Edward Sheeran',
                    'Edward Christopher Sheeran'
                ],
                'iswc':'T9204649558',
                'source':'warner',
                'source_id':1,
                'alternate':{
                    'iswc': [],
                    'title':[],
                    'source':['sony'],
                    'source_id':['1'],
                }
            }
        ]

        for work in expected:
            imported_as_dict = Work.objects.get(title=work['title']).__dict__

            imported_as_dict.pop('_state')
            imported_as_dict.pop('uid')

            assert imported_as_dict == work
