import json
import apache_beam as beam
from apache_beam import coders
from apache_beam.io.iobase import Write
from apache_beam.transforms import PTransform
from apache_beam.io.filesystem import CompressionTypes


class JsonSink(beam.io.FileBasedSink):
    """A Dataflow sink for writing GeoJSON files."""

    def __init__(self,
                 file_path_prefix,
                 crs_code,
                 file_name_suffix='',
                 num_shards=0,
                 shard_name_template=None,
                 coder=coders.StrUtf8Coder(),
                 compression_type=CompressionTypes.AUTO):

        super(JsonSink, self).__init__(
            file_path_prefix,
            file_name_suffix=file_name_suffix,
            num_shards=num_shards,
            shard_name_template=shard_name_template,
            coder=coder,
            mime_type='text/plain',
            compression_type=compression_type)

        self.last_rows = dict()
        self.crs_code = crs_code

    def open(self, temp_path):
        """ Open file and initialize it w opening a list."""
        file_handle = super(JsonSink, self).open(temp_path)
        crs_value = f'urn:ogc:def:axis:{self.crs_code}'
        start_of_file = f'{{"type": "FeatureCollection", "crs": "{crs_value}", "features": [\n'
        file_handle.write(bytes(start_of_file, encoding="utf-8"))
        return file_handle

    def write_record(self, file_handle, value):
        """Writes a single encoded record converted to JSON and terminates the
        line w a comma."""
        if self.last_rows.get(file_handle, None) is not None:
            file_handle.write(self.coder.encode(
                json.dumps(self.last_rows[file_handle])))
            file_handle.write(bytes(',\n', encoding="utf-8"))

        self.last_rows[file_handle] = value

    def close(self, file_handle):
        """Finalize the JSON list and close the file handle returned from
        ``open()``. Called after all records are written.
        """
        if file_handle is not None:
            # Write last row without a comma
            file_handle.write(self.coder.encode(
                json.dumps(self.last_rows[file_handle])))

            # Close list and then the file
            file_handle.write(bytes('\n] }', encoding="utf-8"))
            file_handle.close()


class WriteToGeoJSONFeatureCollection(PTransform):
    """PTransform for writing to GeoJSON files.
    Assumes a list of features according to the GeoJSON specification, that gets put into a FeatureCollection.

    The crs of the json-file defaults to EPSG:4326 (corresponding to WGS:84).
    This can be overwritten by defining a crs_code on class initialization.
    """

    def __init__(self,
                 file_path_prefix,
                 crs_code='EPSG:4326',
                 file_name_suffix='',
                 num_shards=0,
                 shard_name_template=None,
                 coder=coders.StrUtf8Coder(),
                 compression_type=CompressionTypes.AUTO):
        self._sink = JsonSink(file_path_prefix, crs_code, file_name_suffix, num_shards,
                              shard_name_template, coder, compression_type)

    def expand(self, pcoll):
        return pcoll | Write(self._sink)
