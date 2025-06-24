import datetime

from app.utils.datetime import get_server_now


def test_get_server_now_returns_datetime_with_utc_tz() -> None:
    result = get_server_now()
    assert result.tzinfo == datetime.UTC


def test_get_server_now_recent() -> None:
    server_now = get_server_now()
    utc_now = datetime.datetime.now(datetime.UTC)
    assert server_now.minute == utc_now.minute
    assert server_now.hour == utc_now.hour
    assert server_now.day == utc_now.day
    assert server_now.month == utc_now.month
    assert server_now.year == utc_now.year
