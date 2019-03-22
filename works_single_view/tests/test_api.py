from rest_framework.test import APITestCase

from works_single_view.models import Work


class TestWorksAPI(APITestCase):

    def setUp(self):
        self.work_1 = Work.objects.create(
            title='Test Work 1',
            contributors=['Test Contibutor 1', 'Test Contibutor 2'],
            iswc='T111111111',
            source='Test Source',
            source_id=1,
        )

        self.work_2 = Work.objects.create(
            title='Test Work 2',
            contributors=['Test Contibutor 1', 'Test Contibutor 2'],
            iswc='T222222222',
            source='Test Source',
            source_id=2,
        )

        self.work_1_json = {
            'uid': str(self.work_1.uid),
            'title': 'Test Work 1',
            'contributors': ['Test Contibutor 1', 'Test Contibutor 2'],
            'iswc': 'T111111111',
            'source': 'Test Source',
            'source_id': 1,
        }

        self.work_2_json = {
            'uid': str(self.work_2.uid),
            'title': 'Test Work 2',
            'contributors': ['Test Contibutor 1', 'Test Contibutor 2'],
            'iswc': 'T222222222',
            'source': 'Test Source',
            'source_id': 2,
        }

    def test_create_works(self):

        body = {
            'title': 'Test Work 3',
            'contributors': ['Test Contibutor 1', 'Test Contibutor 2'],
            'iswc': 'T333333333',
            'source': 'Test Source',
            'source_id': 2,
        }

        response = self.client.post('/works/', body)

        assert response.status_code == 201
        assert response.json() == {
            **{'uid': str(Work.objects.get(title='Test Work 3').uid)},
            **body
        }

    def test_list_works(self):
        response = self.client.get('/works/')

        assert response.json() == [self.work_1_json, self.work_2_json]

    def test_retrieve_works(self):
        response = self.client.get('/works/%s/' % str(self.work_1.uid))

        assert response.json() == self.work_1_json

    def test_update_work(self):
        body = {'contributors': ['Contibutor 4', 'Contibutor 5']}

        response = self.client.patch('/works/%s/' % str(self.work_1.uid), body)

        assert response.status_code == 200
        assert response.json() == {**self.work_1_json, **body}

        self.work_1.refresh_from_db()
        assert self.work_1.contributors == ['Contibutor 4', 'Contibutor 5']

    def test_destroy_works(self):
        response = self.client.delete('/works/%s/' % str(self.work_1.uid))

        assert response.status_code == 204
        assert not Work.objects.filter(uid=self.work_1.uid).first()


