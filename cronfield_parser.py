from enum import Enum
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple

class CronFieldType(Enum):
    """Enumeration of cron field types."""
    MINUTE = 'minute'
    HOUR = 'hour'
    DAY_OF_MONTH = 'day of month'
    MONTH = 'month'
    DAY_OF_WEEK = 'day of week'

FIELD_RANGES: Dict[CronFieldType, Tuple[int, int]] = {
    CronFieldType.MINUTE: (0, 59),
    CronFieldType.HOUR: (0, 23),
    CronFieldType.DAY_OF_MONTH: (1, 31),
    CronFieldType.MONTH: (1, 12),
    CronFieldType.DAY_OF_WEEK: (0, 6),
}

class FieldExpander(ABC):
    """Abstract base class for field expanders."""
    @abstractmethod
    def expand(self, part: str, min_val: int, max_val: int, field_name: str) -> List[int]:
        """Expand a cron field part into a list of integers."""
        pass

class StepExpander(FieldExpander):
    """Expander for step values in cron fields (e.g., */5)."""
    def expand(self, part: str, min_val: int, max_val: int, field_name: str) -> List[int]:
        range_part, step_part = part.split('/')
        step = int(step_part)
        if range_part == '*':
            start, end = min_val, max_val
        elif '-' in range_part:
            start, end = map(int, range_part.split('-'))
            if start > end:
                raise ValueError(f"Invalid range {start}-{end} for {field_name}")
        else:
            start = int(range_part)
            end = max_val
        if not (min_val <= start <= max_val) or not (min_val <= end <= max_val):
            raise ValueError(f"Range {start}-{end} out of range for {field_name}")
        return list(range(start, end + 1, step))

class RangeExpander(FieldExpander):
    """Expander for range values in cron fields (e.g., 1-5)."""
    def expand(self, part: str, min_val: int, max_val: int, field_name: str) -> List[int]:
        start, end = map(int, part.split('-'))
        if start > end:
            raise ValueError(f"Invalid range {start}-{end} for {field_name}")
        if not (min_val <= start <= max_val) or not (min_val <= end <= max_val):
            raise ValueError(f"Range {start}-{end} out of range for {field_name}")
        return list(range(start, end + 1))

class WildcardExpander(FieldExpander):
    """Expander for wildcard values in cron fields (e.g., *)."""
    def expand(self, part: str, min_val: int, max_val: int, field_name: str) -> List[int]:
        return list(range(min_val, max_val + 1))

class SingleValueExpander(FieldExpander):
    """Expander for single values in cron fields (e.g., 5)."""
    def expand(self, part: str, min_val: int, max_val: int, field_name: str) -> List[int]:
        value = int(part)
        if not (min_val <= value <= max_val):
            raise ValueError(f"Value {value} out of range for {field_name}")
        return [value]

class CronField(ABC):
    """Abstract base class for a cron field."""
    def __init__(self, field_str: str) -> None:
        """Initialize with the field string from the cron expression."""
        self.field_str = field_str

    @property
    @abstractmethod
    def field_type(self) -> CronFieldType:
        """Return the CronFieldType for this field."""
        pass

    def expand(self) -> List[int]:
        """Expand the field string into a list of valid values."""
        if not self.field_str:
            raise ValueError("Empty value")
        if ',' in self.field_str:
            values: List[int] = []
            for part in self.field_str.split(','):
                values.extend(self._expand_part(part))
            return values
        else:
            return self._expand_part(self.field_str)

    def _expand_part(self, part: str) -> List[int]:
        """Expand a single part of the field string."""
        min_val, max_val = FIELD_RANGES[self.field_type]
        field_name = self.field_type.value
        if '/' in part:
            return self.get_step_expander().expand(part, min_val, max_val, field_name)
        elif '-' in part:
            return self.get_range_expander().expand(part, min_val, max_val, field_name)
        elif part == '*':
            return self.get_wildcard_expander().expand(part, min_val, max_val, field_name)
        else:
            return self.get_single_value_expander().expand(part, min_val, max_val, field_name)

    def get_step_expander(self) -> FieldExpander:
        """Return the expander for step values."""
        return StepExpander()
    def get_range_expander(self) -> FieldExpander:
        """Return the expander for range values."""
        return RangeExpander()
    def get_wildcard_expander(self) -> FieldExpander:
        """Return the expander for wildcard values."""
        return WildcardExpander()
    def get_single_value_expander(self) -> FieldExpander:
        """Return the expander for single values."""
        return SingleValueExpander()

class MinuteField(CronField):
    """Cron field for minutes."""
    @property
    def field_type(self) -> CronFieldType:
        return CronFieldType.MINUTE

class HourField(CronField):
    """Cron field for hours."""
    @property
    def field_type(self) -> CronFieldType:
        return CronFieldType.HOUR

class DayOfMonthField(CronField):
    """Cron field for day of month."""
    @property
    def field_type(self) -> CronFieldType:
        return CronFieldType.DAY_OF_MONTH

class MonthField(CronField):
    """Cron field for month."""
    @property
    def field_type(self) -> CronFieldType:
        return CronFieldType.MONTH

class DayOfWeekField(CronField):
    """Cron field for day of week."""
    @property
    def field_type(self) -> CronFieldType:
        return CronFieldType.DAY_OF_WEEK

class CronTableFormatter:
    """Formats the expanded cron fields and command into a table."""
    def __init__(self, expanded: Dict[str, List[int]], command: str, field_objects: List[CronField]) -> None:
        self.expanded = expanded
        self.command = command
        self.field_objects = field_objects

    def format_table(self) -> str:
        """Return a formatted string table of the cron fields and command."""
        lines: List[str] = []
        for field_obj in self.field_objects:
            field_name = field_obj.field_type.value
            values = ' '.join(str(v) for v in self.expanded[field_name])
            lines.append(f"{field_name.ljust(14)}{values}")
        lines.append(f"{'command'.ljust(14)}{self.command}")
        return '\n'.join(lines)

class CronParser:
    """Parses a cron string and expands its fields."""
    FIELD_CLASSES: List[Any] = [
        MinuteField,
        HourField,
        DayOfMonthField,
        MonthField,
        DayOfWeekField,
    ]

    def __init__(self, cron_string: str) -> None:
        """Initialize the parser with a cron string."""
        parts = cron_string.strip().split()
        if len(parts) < 6:
            raise ValueError("Invalid cron string: must have 6 parts (5 fields + command)")
        if len(parts) > 6:
            raise ValueError("Invalid cron string: too many fields")
        self.fields: List[str] = parts[:5]
        self.command: str = ' '.join(parts[5:])
        self.expanded: Dict[str, List[int]] = self._expand_fields()

    def _expand_fields(self) -> Dict[str, List[int]]:
        """Expand all cron fields and return a dictionary of their values."""
        expanded: Dict[str, List[int]] = {}
        self.field_objects = []
        for i, field_class in enumerate(self.FIELD_CLASSES):
            field_obj = field_class(self.fields[i])
            field_name = field_obj.field_type.value
            expanded[field_name] = field_obj.expand()
            self.field_objects.append(field_obj)
        return expanded