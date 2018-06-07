from django.test import TestCase


class DocsTests(TestCase):
    def test_docs_do_not_explode(self):
        res = self.client.get('/api/docs/')
        self.assertEqual(res.status_code, 200)

    def test_api_root_redirects_to_docs(self):
        res = self.client.get('/api/', follow=False)
        self.assertEqual(res['location'], '/api/docs/')
        self.assertEqual(res.status_code, 302)
