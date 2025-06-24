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

class TestInvalidFields:
    @pytest.mark.parametrize("cron_str, error_msg", [
        ("61 0 1 1 0 /bin/ls", "Value 61 out of range for minute"),
        ("0 24 1 1 0 /bin/ls", "Value 24 out of range for hour"),
        ("0 0 32 1 0 /bin/ls", "Value 32 out of range for day of month"),
        ("0 0 1 13 0 /bin/ls", "Value 13 out of range for month"),
        ("0 0 1 1 7 /bin/ls", "Value 7 out of range for day of week"),
    ])
    def test_invalid_field_values(self, cron_str, error_msg):
        with pytest.raises(ValueError) as excinfo:
            CronParser(cron_str)
        assert error_msg in str(excinfo.value)

class TestExpansion:
    def test_step_expansion(self):
        parser = CronParser("*/10 * * * * /bin/ls")
        assert parser.expanded['minute'] == list(range(0, 60, 10))

    def test_range_expansion(self):
        parser = CronParser("0 1-3 * * * /bin/ls")
        assert parser.expanded['hour'] == [1, 2, 3]

    def test_list_expansion(self):
        parser = CronParser("0 0 1,15 * * /bin/ls")
        assert parser.expanded['day of month'] == [1, 15]

    def test_wildcard_expansion(self):
        parser = CronParser("* * * * * /bin/ls")
        assert parser.expanded['minute'] == list(range(0, 60))
        assert parser.expanded['hour'] == list(range(0, 24))
        assert parser.expanded['day of month'] == list(range(1, 32))
        assert parser.expanded['month'] == list(range(1, 13))
        assert parser.expanded['day of week'] == list(range(0, 7))

    def test_min_max_values(self):
        parser = CronParser("0 0 1 1 0 /bin/ls")
        assert parser.expanded['minute'] == [0]
        assert parser.expanded['hour'] == [0]
        assert parser.expanded['day of month'] == [1]
        assert parser.expanded['month'] == [1]
        assert parser.expanded['day of week'] == [0]

    @pytest.mark.parametrize("cron_str", [
        "a b c d e /bin/ls",  # non-integer
        "0-100 * * * * /bin/ls",  # out of range
        "*/0 * * * * /bin/ls",  # invalid step
        "0,,1 * * * * /bin/ls",  # malformed list
        "0 0 1 1 /bin/ls",  # too few fields
        "0 0 1 1 0 0 0 /bin/ls",  # too many fields
    ])
    def test_malformed_cron_strings(self, cron_str):
        with pytest.raises(ValueError):
            CronParser(cron_str)

    def test_step_expander_invalid_range(self):
        # Should raise ValueError for start > end in step range
        with pytest.raises(ValueError, match="Invalid range 5-1 for minute"):
            CronParser("5-1/2 * * * * /bin/ls")

    def test_step_expander_single_value_with_step(self):
        # Should expand correctly for single value with step (e.g., 3/2)
        parser = CronParser("3/2 * * * * /bin/ls")
        # Should expand from 3 to max (59) with step 2
        assert parser.expanded['minute'] == list(range(3, 60, 2))

    def test_range_expander_invalid_range(self):
        # Should raise ValueError for start > end in range
        with pytest.raises(ValueError, match="Invalid range 5-1 for hour"):
            CronParser("0 5-1 * * * /bin/ls")
