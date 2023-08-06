from curia.api.swagger_client import ProcessJob, ModelJob, ModelBatchJob, DatasetJob, AnalysisJob
from curia.mock.api import MockApiConfiguration
from curia.mock.session import MockSession
from curia.session import Session
from curia.utils.job import get_interface, JobInterface


# pylint: disable=W0640,W0622,W0613
from curia.utils.string import to_camel_case


def test_job_interface():
    with MockApiConfiguration(
        seed_data=[
            ProcessJob(
                id="test_id",
                process_id="test_process_id",
                status="Not Started",
                project_id="test_project_id",
                config={"foo": "bar"}
            ),
            ModelJob(
                id="test_id",
                model_id="test_process_id",
                type="train",
                status="Not Started",
                project_id="test_project_id",
                cohort_id="test_cohort_id",
                config={"foo": "bar"}
            ),
            ModelBatchJob(
                id="test_id",
                model_batch_id="test_model_batch_id",
                type="train",
                status="Not Started",
                project_id="test_project_id",
                cohort_id="test_cohort_id",
                config={"foo": "bar"}
            ),
            DatasetJob(
                id="test_id",
                status="Not Started",
                dataset_id="test_dataset_id",
                config={"foo": "bar"}
            ),
            AnalysisJob(
                id="test_id",
                status="Not Started",
                analysis_id="test_analysis_id",
                type="train",
                project_id="test_project_id",
                config={"foo": "bar"}
            )
        ],
        method_overrides={}
    ):
        for job_type_stub in ["process_job", "model_job", "dataset_job", "model_batch_job", "analysis_job"]:
            session: Session = MockSession()
            job_interface: JobInterface = get_interface(session, job_type_stub=job_type_stub)

            def validate_return(obj, expected_status):
                assert obj.config['foo'] == 'bar'
                assert obj.id == 'test_id'
                assert to_camel_case(job_type_stub) == type(obj).__name__
                assert obj.status == expected_status

            validate_return(job_interface.get("test_id"), "Not Started")
            validate_return(job_interface.start("test_id"), "RUNNING")
            validate_return(job_interface.stop("test_id"), "ABORTED")


def test_job_interface_run():
    mock_process_job = ProcessJob(
        id="test_id",
        process_id="test_process_id",
        status="Not Started",
        project_id="test_project_id"
    )
    mock_process_job.counter = 0

    def get_one_base_process_job_controller_process_job(self, id):
        assert id == mock_process_job.id
        if mock_process_job.counter > 1:
            mock_process_job.status = "COMPLETE"
            return mock_process_job
        mock_process_job.counter += 1
        return mock_process_job

    with MockApiConfiguration(
        seed_data=[mock_process_job],
        method_overrides={
            "get_one_base_process_job_controller_process_job": get_one_base_process_job_controller_process_job
        }
    ):
        session: Session = MockSession()
        process_job_interface: JobInterface = get_interface(session, process_job=True)
        job = process_job_interface.run("test_id", timeout=5, interval=.5)
        assert job.status == "COMPLETE"
        assert job.id == mock_process_job.id
