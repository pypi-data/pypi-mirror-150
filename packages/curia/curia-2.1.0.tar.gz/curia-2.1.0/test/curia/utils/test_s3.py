from unittest.mock import patch, MagicMock
import pyarrow.dataset

from curia.mock.s3 import curia_mock_s3
from curia.utils.s3 import get_parquet_file_metadata, get_metadata, s3_listdir


def test_get_parquet_file_metadata():
    mock_dataset = MagicMock()
    mock_dataset.schema.names = ["column_a", "column_b", "column_c"]
    batch_a = MagicMock()
    batch_b = MagicMock()
    batch_a.num_rows = 50
    batch_b.num_rows = 80
    mock_dataset.to_batches.return_value = [batch_a, batch_b]
    mock_pyarrow_dataset_module = MagicMock(pyarrow.dataset)
    mock_pyarrow_dataset_module.dataset = MagicMock(return_value=mock_dataset)
    with patch("curia.utils.s3.ds", mock_pyarrow_dataset_module):
        n_columns, n_rows = get_parquet_file_metadata("s3://test-bucket/test-uri/file.parquet")
        assert n_columns == 3
        assert n_rows == 130


@curia_mock_s3(
    seed_s3_data={
        "s3://test-bucket/test_data.parquet": dict(
            Body=b'foobarbaz',
            ContentType="binary"
        )
    }
)
def test_get_metadata():
    metadata = get_metadata("s3://test-bucket/test_data.parquet")
    assert metadata['ContentLength'] == 9
    assert metadata['ContentType'] == "binary"


@curia_mock_s3(
    seed_s3_data={
        "s3://test-bucket/a/test_data.parquet": dict(
            Body=b'foobarbaz',
            ContentType="binary"
        ),
        "s3://test-bucket/a/test_data2.parquet": dict(
            Body=b'foobizbaz',
            ContentType="binary"
        ),
        "s3://test-bucket/b/a.parquet": dict(
            Body=b'foobizbaz',
            ContentType="binary"
        ),
        "s3://test-bucket/b/b.parquet": dict(
            Body=b'foobizbaz',
            ContentType="binary"
        ),
        "s3://test-bucket/b/c.parquet": dict(
            Body=b'foobizbaz',
            ContentType="binary"
        )
    }
)
def test_s3_listdir():
    assert tuple(sorted(s3_listdir("s3://test-bucket/a/"))) == \
           ("s3://test-bucket/a/test_data.parquet", "s3://test-bucket/a/test_data2.parquet")

    assert tuple(sorted(s3_listdir("s3://test-bucket/b/"))) == \
           (
               "s3://test-bucket/b/a.parquet",
               "s3://test-bucket/b/b.parquet",
               "s3://test-bucket/b/c.parquet"
           )

    assert tuple(sorted(s3_listdir("s3://test-bucket/b/", max_list_len=2))) == \
           (
               "s3://test-bucket/b/a.parquet",
               "s3://test-bucket/b/b.parquet",
               "s3://test-bucket/b/c.parquet"
           )
