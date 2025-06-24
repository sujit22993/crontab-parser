import pytest
from cronfield_parser import CronParser

@pytest.mark.parametrize("cron_str, expected", [
    ("*/15 0 1,15 * 1-5 /usr/bin/find", {
        'minute': list(range(0, 60, 15)),
        'hour': [0],
        'day of month': [1, 15],
        'month': list(range(1, 13)),
        'day of week': list(range(1, 6)),
    }),
    ("0 12 * 1,6 0 /bin/echo", {
        'minute': [0],
        'hour': [12],
        'day of month': list(range(1, 32)),
        'month': [1, 6],
        'day of week': [0],
    }),
    ("5 4 * * 0 /bin/date", {
        'minute': [5],
        'hour': [4],
        'day of month': list(range(1, 32)),
        'month': list(range(1, 13)),
        'day of week': [0],
    }),
])
def test_cron_parser_expansion(cron_str, expected):
    parser = CronParser(cron_str)
    for field, exp in expected.items():
        assert parser.expanded[field] == exp

def test_invalid_cron_string_too_few():
    with pytest.raises(ValueError):
        CronParser("* * * * /bin/ls")

def test_invalid_cron_string_too_many():
    with pytest.raises(ValueError):
        CronParser("* * * * * * * /bin/ls")

def test_invalid_minute_value():
    with pytest.raises(ValueError):
        CronParser("61 0 1 1 0 /bin/ls")

def test_invalid_hour_range():
    with pytest.raises(ValueError):
        CronParser("0 0-25 1 1 0 /bin/ls")

def test_invalid_day_of_month():
    with pytest.raises(ValueError):
        CronParser("0 0 0 1 0 /bin/ls")

def test_invalid_month():
    with pytest.raises(ValueError):
        CronParser("0 0 1 13 0 /bin/ls")

def test_invalid_day_of_week():
    with pytest.raises(ValueError):
        CronParser("0 0 1 1 7 /bin/ls")

def test_step_expansion():
    parser = CronParser("*/10 * * * * /bin/ls")
    assert parser.expanded['minute'] == list(range(0, 60, 10))

def test_range_expansion():
    parser = CronParser("0 1-3 * * * /bin/ls")
    assert parser.expanded['hour'] == [1, 2, 3]

def test_list_expansion():
    parser = CronParser("0 0 1,15 * * /bin/ls")
    assert parser.expanded['day of month'] == [1, 15]

def test_wildcard_expansion():
    parser = CronParser("* * * * * /bin/ls")
    assert parser.expanded['minute'] == list(range(0, 60))
    assert parser.expanded['hour'] == list(range(0, 24))
    assert parser.expanded['day of month'] == list(range(1, 32))
    assert parser.expanded['month'] == list(range(1, 13))
    assert parser.expanded['day of week'] == list(range(0, 7))
