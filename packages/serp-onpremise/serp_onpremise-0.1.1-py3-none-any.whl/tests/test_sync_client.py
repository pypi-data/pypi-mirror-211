from serp_onpremise import Client


def test_client_default_api_version():
    c = Client(base_url="http://localhost:8080")
    assert c.api_version == 1


def test_get_incorrect_attr():
    c = Client(base_url="http://localhost:8080")
    in_exception = False
    try:
        c.incorrect
    except BaseException:
        in_exception = True
    assert in_exception
