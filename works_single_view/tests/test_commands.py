from django.test import TestCase

from works_single_view.models import Work


class TestWorksSingleView(TestCase):

    def setUp(self):
        self.work = Work(
            source_id=1,
            title="Test Work",
            contributors=["Jane Doe", "John Doe"],
            iswc="T1234",
            source="Test Source"
        ).save()

    def test_import_data_from_csv(self):
        assert Work.objects.get().title == "Test Work"
