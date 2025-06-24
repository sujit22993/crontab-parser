import sys
from cronfield_parser import CronParser, CronTableFormatter

def main():
    if len(sys.argv) != 2:
        print("Usage: python -m cron_parser_cli '<cron_string>'")
        sys.exit(1)
    cron_string = sys.argv[1]
    try:
        parser = CronParser(cron_string)
        formatter = CronTableFormatter(parser.expanded, parser.command, parser.field_objects)
        print(formatter.format_table())
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
