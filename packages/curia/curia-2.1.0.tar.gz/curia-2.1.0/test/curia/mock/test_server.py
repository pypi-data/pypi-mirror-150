import json

import requests

from curia.mock.server import using_test_server, TestServer


def handle_spam(data_summary):
    return data_summary.url_qs


def handle_eggs(data_summary):
    return data_summary.content_qs


def broken_server(data_summary):
    raise Exception(data_summary)


@using_test_server(port=3000, response_map={
    "/foo": {"bar": "baz"},
    "/spam": handle_spam,
    "/eggs": handle_eggs,
    "/broken": broken_server,
    "/response-config": TestServer.ResponseConfig(
        accepted_methods=["GET"],
        content_type="application/json",
        content=json.dumps({"foo": "bar"}).encode("utf-8")
    )
})
def test_server():
    r = requests.get('http://localhost:3000/healthcheck')
    assert r.status_code == 200

    r = requests.get('http://localhost:3000/teapot')
    assert r.status_code == 418  # teapot

    r = requests.get('http://localhost:3000/foo')
    assert r.status_code == 200
    assert r.headers['content-type'] == "application/json"
    assert r.encoding == "utf-8"
    assert r.json()["bar"] == "baz"

    r = requests.get('http://localhost:3000/spam?abc=cde')
    assert r.status_code == 200
    assert r.headers['content-type'] == "application/json"
    assert r.encoding == "utf-8"
    assert r.json()["abc"] == ["cde"]

    r = requests.post('http://localhost:3000/eggs', json={"fee": "fi"})
    assert r.status_code == 200
    assert r.headers['content-type'] == "application/json"
    assert r.encoding == "utf-8"
    assert r.json()["fee"] == "fi"

    r = requests.get('http://localhost:3000/broken')
    assert r.status_code == 500

    r = requests.get('http://localhost:3000/not-a-path')
    assert r.status_code == 404

    r = requests.get('http://localhost:3000/response-config')
    assert r.status_code == 200
    assert r.headers['content-type'] == "application/json"
    assert r.encoding == "utf-8"
    assert r.json()["foo"] == "bar"

    r = requests.post('http://localhost:3000/response-config')
    assert r.status_code == 405

    debug_logs = TestServer.debug_logs(3000)
    assert len(debug_logs) == 7
