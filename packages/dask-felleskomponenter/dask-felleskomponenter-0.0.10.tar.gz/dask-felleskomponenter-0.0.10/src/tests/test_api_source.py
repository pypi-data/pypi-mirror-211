import unittest
from unittest.mock import MagicMock
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that, equal_to

from dask_felleskomponenter.common.api_client import ApiClient
from dask_felleskomponenter.sources.api_source import ReadFromApi


class TestReadFromApiSource(unittest.TestCase):

    def test_read_from_api(self):
        # Create a sample API response
        sample_response = {"id": 1}

        ApiClient.get_data = MagicMock(return_value=sample_response)
        # Mock the ApiClient
        api_client = ApiClient("https://test.kartverket.no/api")

        path = "/path/to/api/call"

        with TestPipeline() as p:
            result = (
                    p
                    | ReadFromApi(api_client, path)
            )
            assert_that(result, equal_to(sample_response), label="Check output")

        api_client.get_data.assert_called_with(path)
