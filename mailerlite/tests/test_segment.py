"""Module to tests Segment."""
import pytest

from mailerlite.constants import API_KEY_TEST
from mailerlite.segment import Segments


@pytest.fixture
def header():
    headers = {'content-type': "application/json",
               'x-mailerlite-apikey': API_KEY_TEST
               }
    return headers


def test_wrong_headers():
    headers_2 = {'content-type': "application/json",
                 'x-mailerlite-apikey': 'FAKE_KEY'
                 }
    headers_3 = {'content-type': "application/json",
                 }
    headers_4 = {'x-mailerlite-apikey': 'FAKE_KEY'
                 }

    with pytest.raises(OSError):
        segm = Segments(headers_2)
        segm.count()

    with pytest.raises(ValueError):
        segm = Segments(headers_3)

    with pytest.raises(ValueError):
        segm = Segments(headers_4)


def test_segments_error(header):
    segm = Segments(header)

    with pytest.raises(OSError):
        segm.all(order='upper')


def test_segments_crud(header):
    segm = Segments(header)
    all_segm, meta = segm.all()

    assert len(all_segm) == meta.pagination.count
    assert len(all_segm) == segm.count()

    all_segm, meta = segm.all(as_json=True)

    assert len(all_segm)
    assert 'pagination' in meta.keys()
