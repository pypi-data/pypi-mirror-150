from curia.mock.session import MockSession
from curia.mock.s3 import curia_mock_s3
from curia.session import Session
from curia.utils.dataset import create_dataset_from_s3_path


@curia_mock_s3(seed_s3_data={
    "s3://curia-local-data-lake/foo/file.parquet": dict(
        Body=b'foobarbaz',
        ContentType="binary"
    )
})
def test_dataset():
    session: Session = MockSession()

    dataset, dataset_job = create_dataset_from_s3_path(
        session,
        dataset_name="test_dataset",
        dataset_type="cohort",
        file_type="parquet",
        description="test_description",
        s3_path="s3://curia-local-data-lake/foo",
    )

    created_dataset = session.api_instance.get_one_base_dataset_controller_dataset(id=dataset.id)
    create_dataset_job = session.api_instance.get_one_base_dataset_job_controller_dataset_job(id=dataset_job.id)
    assert created_dataset.name == "test_dataset"
    assert created_dataset.type == "cohort"
    assert created_dataset.file_type == "parquet"
    assert created_dataset.description == "test_description"
    assert create_dataset_job.dataset_id == created_dataset.id
