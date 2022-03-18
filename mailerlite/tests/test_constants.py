import ipdb
from mailerlite.constants import validate_or_make_namedtuples, Segment


def test_validate_or_make_namedtuples():

    new_segment = validate_or_make_namedtuples(Segment,
                                               ['id', 'title', 'filter',
                                                'total', 'sent', 'opened',
                                                'clicked','created_at',
                                                'updated_at', 'timed_out'])

    assert new_segment == Segment

    new_segment = validate_or_make_namedtuples(Segment,
                                               ['id', 'title', 'filter',
                                                'total', 'sent',
                                                'opened', 'clicked',
                                                'created_at', 'updated_at',
                                                'timed_out', 'custom'])

    assert new_segment != Segment
    assert 'custom' in new_segment._fields
