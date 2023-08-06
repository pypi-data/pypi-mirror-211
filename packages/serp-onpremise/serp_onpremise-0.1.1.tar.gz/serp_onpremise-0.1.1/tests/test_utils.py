import os

import pytest

from serp_onpremise.constants import sentinel
from serp_onpremise.utils import (
    prepare_file_processing,
    process_query_params,
    request_dict_processing,
    request_form_processing,
    request_query_processing,
    validate_month_str,
)


def test_prepare_file_processing_binary():
    data = b"test_image_data"
    image = prepare_file_processing(data)

    assert isinstance(image, dict)
    assert "image" in image
    assert isinstance(image["image"], tuple)
    assert len(image["image"]) == 2
    assert image["image"][1] is not None
    assert image["image"][0] == "file"
    assert image["image"][1].read() == data


def test_prepare_file_processing_buffer_reader():
    filename = "test_image_name.jpg"
    data = b"test_image_data"

    with open(filename, "wb") as f:
        f.write(data)

    with open(filename, "rb") as f:
        image = prepare_file_processing(f)

        assert isinstance(image, dict)
        assert "image" in image
        assert isinstance(image["image"], tuple)
        assert len(image["image"]) == 2
        assert image["image"][0] == filename
        assert image["image"][1] is not None

        image_data = image["image"][1].read()

    os.remove(filename)

    assert image_data == data


def test_prepare_file_processing_tuple():
    filename = "test_image_name.jpg"
    data = b"test_image_data"

    with open(filename, "wb") as f:
        f.write(data)

    with open(filename, "rb") as f:
        image = prepare_file_processing((filename, f))

        assert isinstance(image, dict)
        assert "image" in image
        assert isinstance(image["image"], tuple)
        assert len(image["image"]) == 2
        assert image["image"][0] == filename
        assert image["image"][1] is not None

        image_data = image["image"][1].read()

    os.remove(filename)

    assert image_data == data


def test_prepare_image_incorrect():
    with pytest.raises(Exception) as e:
        prepare_file_processing("test_incorrect_data")

    assert str(e.value) == "Wrong file datatype"


def test_process_query_params():
    data = {"foo": 1, "bar": [1, 2, 3]}
    result = process_query_params(data)

    assert result == {"foo": 1, "bar": "1,2,3"}


def test_request_query_processing():
    data = {"one": 1, "two": sentinel, "self": 3, "three": [1, 2, 3]}

    result = request_query_processing(data)
    assert result == {"one": 1, "three": "1,2,3"}


def test_request_dict_processing_empty_exclude():
    data = {"one": 1, "two": sentinel, "self": 3, "three": [1, 2, 3]}

    result = request_dict_processing(data)
    assert result == {"one": 1, "three": [1, 2, 3]}


def test_request_dict_processing_has_exclude():
    data = {"one": 1, "two": sentinel, "self": 3, "three": [1, 2, 3]}

    result = request_dict_processing(data, ["three"])
    assert result == {"one": 1}


def test_request_form_processing_empty_exclude():
    data = {"one": 1, "two": sentinel, "self": 3, "three": "3"}

    result = request_form_processing(data)
    assert result == {"one": "1", "three": "3"}


def test_request_form_processing_has_exclude():
    data = {"one": 1, "two": sentinel, "self": 3, "three": "3"}

    result = request_form_processing(data, ["three"])
    assert result == {"one": "1"}


def test_validate_month_str():
    month_str = "2018*09"
    with pytest.raises(ValueError) as exc_info:
        validate_month_str(month_str)
    assert exc_info.type is ValueError
    assert (
        exc_info.value.args[0]
        == f"Incorrect month format in {month_str}, should be YYYY-MM"
    )
