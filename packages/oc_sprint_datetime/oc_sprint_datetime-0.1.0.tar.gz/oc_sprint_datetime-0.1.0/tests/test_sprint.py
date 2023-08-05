from datetime import datetime, timezone

from oc_sprint_datetime import Sprint


def test_sprint():
    sprint = Sprint("BB.272")
    assert sprint.start_datetime == datetime(2022, 5, 3, 0, 0, tzinfo=timezone.utc)

    # Tuesday as well!
    assert sprint.end_datetime == datetime(2022, 5, 17, 0, 0, tzinfo=timezone.utc)
