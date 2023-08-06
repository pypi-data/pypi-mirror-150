from curia.api.swagger_client import ProcessJob
from curia.mock.api import MockApiConfiguration
from curia.mock.session import MockSession


def test_mock_session():
    with MockApiConfiguration(
            [ProcessJob(id="biz", process_id="bar", project_id="fuz")], {}
    ):
        session = MockSession()
        res = session.api_instance.get_one_base_process_job_controller_process_job(id="biz")
        assert res.id == "biz"
        assert res.process_id == "bar"
        assert res.project_id == "fuz"
