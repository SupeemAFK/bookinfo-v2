import unittest
import requests_mock
import productpage
import re

class ApplianceTest(unittest.TestCase):

    def setUp(self):
        self.app = productpage.app.test_client()

    @requests_mock.Mocker()
    def test_header_propagation_reviews(self, m):
        product_id = 0
        
        url_pattern = re.compile(r'^http://(bookinfo-)?reviews(-dev|-uat)?:9080/reviews/\d+$')

        expected_headers = {
            'x-request-id': '34eeb41d-d267-9e49-8b84-dde403fc5b72',
            'sw8': '40c7fdf104e3de67'
        }
        
        m.get(url_pattern, text='{}', request_headers=expected_headers)

        uri = "/api/v1/products/%d/reviews" % product_id
        headers = {
            'x-request-id': '34eeb41d-d267-9e49-8b84-dde403fc5b72',
            'sw8': '40c7fdf104e3de67',
            'x-b3-traceid': '40c7fdf104e3de67' 
        }
        actual = self.app.get(uri, headers=headers)
        self.assertEqual(200, actual.status_code)

    @requests_mock.Mocker()
    def test_header_propagation_ratings(self, m):
        product_id = 0
        
        url_pattern = re.compile(r'^http://(bookinfo-)?ratings(-dev|-uat)?:9080/ratings/\d+$')

        expected_headers = {
            'x-request-id': '34eeb41d-d267-9e49-8b84-dde403fc5b73',
            'sw8': '40c7fdf104e3de67'
        }
        
        m.get(url_pattern, text='{}', request_headers=expected_headers)

        uri = "/api/v1/products/%d/ratings" % product_id
        headers = {
            'x-request-id': '34eeb41d-d267-9e49-8b84-dde403fc5b73',
            'sw8': '40c7fdf104e3de67',
            'x-b3-traceid': '30c7fdf104e3de66'
        }
        actual = self.app.get(uri, headers=headers)
        self.assertEqual(200, actual.status_code)