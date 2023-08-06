import unittest
from dask_felleskomponenter.common.api_client import ApiClient


class TestApiClient(unittest.TestCase):

	def test_api_setup(self):
		base_url = "base/url/for/api"
		client = ApiClient(base_url=base_url)
		self.assertEqual(base_url, client.base_url)
