from apache_beam import DoFn, PTransform, ParDo, Create
import json

class ReadSingleFileFromGcp(DoFn):
    def __init__(self, file_pattern):
        self._file_pattern = file_pattern

    def process(self, element, *args, **kwargs):
        from google.cloud import storage

        client = storage.Client()
        bucket_name, blob_name = self._file_pattern[5:].split("/", 1)
        bucket = client.get_bucket(bucket_name)
        blob = storage.Blob(blob_name, bucket)
        file_str = blob.download_as_text()
        yield file_str


class ReadFileFromGCP(PTransform):
    def __init__(self, file_pattern):
        self._file_pattern = file_pattern

    def expand(self, pcoll):
        return (
            pcoll
            | 'CreateInput' >> Create([None])
            | 'ReadJson' >> ParDo(ReadSingleFileFromGcp(self._file_pattern))
        )
