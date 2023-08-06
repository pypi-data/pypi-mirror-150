from unittest.mock import MagicMock

from curia.api.swagger_client import PlatformApi, ProcessJob, CreateManyProcessJobDto, Process, ModelJob, \
    ModelPopulation, DataQuery, Dataset
from curia.mock.api import MockApiInstance, MockApiConfiguration


def test_mock_api_instance():
    api_instance: PlatformApi = MockApiInstance()
    process_job = api_instance.create_one_base_process_job_controller_process_job(
        ProcessJob(process_id="foo", project_id="bar", config={})
    )
    alt_process_job = api_instance.create_many_base_process_job_controller_process_job(
        CreateManyProcessJobDto(
            bulk=[ProcessJob(process_id="quz", project_id="baz", config={})]
        )
    ).bulk[0]
    res = api_instance.get_one_base_process_job_controller_process_job(id=process_job.id)
    assert res.id == process_job.id
    assert res.process_id == process_job.process_id

    dto = api_instance.get_many_base_process_job_controller_process_job(
        filter=[f"id||$eq||{process_job.id}"]
    )
    res = dto.data[0]
    assert res.id == process_job.id
    assert res.process_id == process_job.process_id

    dto = api_instance.get_many_base_process_job_controller_process_job(
        filter=["projectId||$ne||baz"]
    )
    res = dto.data[0]
    assert res.id == process_job.id
    assert res.process_id == process_job.process_id

    dto = api_instance.get_many_base_process_job_controller_process_job(
        filter=["projectId||$ne||quz"]
    )
    res = dto.data[0]
    assert res.id in (process_job.id, alt_process_job.id)
    assert res.process_id in (process_job.process_id, alt_process_job.process_id)
    res = dto.data[1]
    assert res.id in (process_job.id, alt_process_job.id)
    assert res.process_id in (process_job.process_id, alt_process_job.process_id)

    api_instance.update_one_base_process_job_controller_process_job(
        id=process_job.id,
        body=ProcessJob(id=process_job.id, process_id="baz", project_id="bar", config={})
    )
    res = api_instance.get_one_base_process_job_controller_process_job(id=process_job.id)
    assert res.id == process_job.id
    assert res.process_id == "baz"

    api_instance.replace_one_base_process_job_controller_process_job(
        id=process_job.id,
        body=ProcessJob(id=process_job.id, process_id="quz", project_id="qaz", config={})
    )
    res = api_instance.get_one_base_process_job_controller_process_job(id=process_job.id)
    assert res.id == process_job.id
    assert res.process_id == "quz"

    api_instance.process_job_controller_start(
        id=process_job.id,
    )
    res = api_instance.get_one_base_process_job_controller_process_job(id=process_job.id)
    assert res.status == "RUNNING"

    api_instance.process_job_controller_stop(
        id=process_job.id,
    )
    res = api_instance.get_one_base_process_job_controller_process_job(id=process_job.id)
    assert res.status == "ABORTED"

    api_instance.delete_one_base_process_job_controller_process_job(id=process_job.id)

    dto = api_instance.get_many_base_process_job_controller_process_job(
        filter=["projectId||$ne||quz"]
    )
    assert len(dto.data) == 1
    res = dto.data[0]
    assert res.id == alt_process_job.id
    assert res.process_id == alt_process_job.process_id

    api_instance.delete_one_base_process_job_controller_process_job(id=alt_process_job.id)


def test_mock_api_instance_joins():
    with MockApiConfiguration(
            [
                ProcessJob(
                    id="fuz",
                    process_id="bar",
                    project_id="buz"
                ),
                ProcessJob(
                    id="foo",
                    process_id="bar",
                    project_id="buz"
                ),
                Process(id="bar", project_id="buz", type="test_type")
            ],
            {}
    ):
        api_instance = MockApiInstance()

        res = api_instance.get_one_base_process_job_controller_process_job(id="foo", join=["process"])
        assert res.process is not None

        res = api_instance.get_one_base_process_controller_process(id="bar", join=["processJobs"])
        assert len(res.process_jobs) == 2


def test_mock_api_instance_multi_join():
    with MockApiConfiguration(
            [
                ModelJob(
                    id="test_model_job_id",
                    config={"containerConfig": {"strategy": "DEFAULT"}, "train_model_job_id": "train_model_job_id"},
                    type="train",
                    project_id="test_proj_id",
                    model_id="test_mod_id",
                    model_population_id="model-population-id"
                ),
                ModelPopulation(
                    id="model-population-id",
                    created_at="2021-01-01",
                    created_by="created-by-user",
                    last_updated_by="created-by-user",
                    updated_at="2021-01-01",
                    version=4,
                    data_query_id="data-query-id"
                ),
                DataQuery(
                    id="data-query-id",
                    statement="SELECT * FROM FAKE_SQL",
                    dataset_id="dataset-id"
                ),
                Dataset(
                    name="test_dataset",
                    type="train",
                    id="dataset-id",
                    location="s3://curia-local-data-lake/mock_path/dataset_path/"
                )
            ],
            {}
    ):
        api_instance = MockApiInstance()
        model_job = api_instance.get_one_base_model_job_controller_model_job(
            id="test_model_job_id",
            join=["modelPopulation", "modelPopulation.dataQuery", "modelPopulation.dataQuery.dataset"]
        )
        assert model_job.model_population.data_query.dataset.name == "test_dataset"
        assert model_job.model_population.data_query.dataset.type == "train"
        assert model_job.model_population.data_query.dataset.id == "dataset-id"
        assert model_job.model_population.data_query.dataset.location == "s3://curia-local-data-lake/mock_path/dataset_path/"


def test_mock_api_instance_nested_config():
    with MockApiConfiguration(
            [
                ProcessJob(
                    id="fuz",
                    process_id="bar",
                    process=Process(id="biz", project_id="buz", type="test_type"),
                    project_id="buz"
                ),

            ],
            {}
    ):
        api_instance = MockApiInstance()

        res = api_instance.get_one_base_process_job_controller_process_job(id="fuz", join=["process"])
        assert res.process is not None
        assert res.process_id == "biz"
        assert len(res.process.process_jobs) == 1
        assert res.process.process_jobs[0].id == "fuz"


def test_mock_api_instance_configuration():
    mock_process_job_controller_start = MagicMock()

    with MockApiConfiguration(
            [ProcessJob(id="fuz", process_id="baz", project_id="buz")],
            {"process_job_controller_start": mock_process_job_controller_start}
    ):
        with MockApiConfiguration(
                [ProcessJob(id="biz", process_id="bar", project_id="fuz")],
                {"process_job_controller_start": mock_process_job_controller_start}
        ):
            api_instance = MockApiInstance()
            res = api_instance.get_one_base_process_job_controller_process_job(id="fuz")
            assert res.id == "fuz"
            assert res.process_id == "baz"
            assert res.project_id == "buz"

            res = api_instance.get_one_base_process_job_controller_process_job(id="biz")
            assert res.id == "biz"
            assert res.process_id == "bar"
            assert res.project_id == "fuz"

            api_instance.process_job_controller_start(id="fuz")

            mock_process_job_controller_start.assert_called_with(api_instance, id="fuz")


def test_mock_api_instance_404():
    api_instance = MockApiInstance()

    try:
        api_instance.get_one_base_process_job_controller_process_job(id="notid")
    except Exception as e:
        assert "404" in str(e)

    try:
        api_instance.update_one_base_process_job_controller_process_job(
            id="notid",
            body=ProcessJob(id="notid", process_id="baz", project_id="fuz")
        )
    except Exception as e:
        assert "404" in str(e)

    try:
        api_instance.replace_one_base_process_job_controller_process_job(
            id="notid",
            body=ProcessJob(id="notid", process_id="baz", project_id="fuz")
        )
    except Exception as e:
        assert "404" in str(e)

    try:
        api_instance.process_job_controller_start(id="notid")
    except Exception as e:
        assert "404" in str(e)

    try:
        api_instance.process_job_controller_stop(id="notid")
    except Exception as e:
        assert "404" in str(e)


if __name__ == "__main__":
    test_mock_api_instance_multi_join()