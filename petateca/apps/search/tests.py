from django.test import TestCase

class SearchTest(TestCase):
    fixtures = ['twin_peaks.json']
    
    def test_opensearch_lookup(self):
        ''' OpenSearch autocomplete '''
        url = '/search/opensearch/?q=T'
        r = self.client.get(url, {})
        self.assertEqual(r.status_code, 200)
        result_expected = '["T", ["Twin Peaks"]]'
        self.assertEqual(r._get_content(), result_expected)

    def test_search_lookup(self):
        ''' La busqueda de AJAX '''
        url = '/search/lookup/?query=Twin'
        res = self.client.get(url, {})
        self.assertContains(res, 'Twin Peaks')
