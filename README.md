# crontab-parser

A robust, extensible Python CLI tool and library for parsing and expanding cron strings. It outputs a formatted table showing the expanded values for each cron field and the command to run. The codebase is modular, OOP, and designed for maintainability and extensibility.

## Features
- Parses standard cron expressions (minute, hour, day of month, month, day of week, command)
- Expands all field types: wildcards, ranges, steps, lists, and single values
- Outputs a human-readable table
- Modular, extensible, and well-tested (84%+ coverage)
- Follows SOLID, DRY, and OOP best practices

## Usage

### Run the CLI

From the project root, use:

```
python -m cron_parser_cli "<cron_string>"
```

Example:

```
python -m cron_parser_cli "*/15 0 1,15 * 1-5 /usr/bin/find"
```

This will output:

```
minute        0 15 30 45
hour          0
...           ...
command       /usr/bin/find
```

### Run Tests

```
pytest --cov=cronfield_parser --cov-report=term-missing
```

## Project Structure
- `cronfield_parser.py`: Core parsing and formatting logic
- `cron_parser_cli.py`: CLI entry point
- `tests/`: Test suite
- `requirements.txt`: Dependencies

## Requirements
- Python 3.8+
- Install dependencies with:
  ```
  pip install -r requirements.txt
  ```

## License
MIT
