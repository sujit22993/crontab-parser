import sys


# class CronFieldValidator:
#     def __init__(self, cron_input):
#         self.cron_input = cron_input
#         self.fields = self.parse_cron_input()

#     def parse_cron_input(self):
#         parts = self.cron_input.split()
#         if len(parts) < 6:
#             raise ValueError("Cron input must contain at least 6 fields: minute, hour, day_of_month, month, day_of_week, command_to_run")
#         return {
#             "minute": parts[0],
#             "hour": parts[1],
#             "day_of_month": parts[2],
#             "month": parts[3],
#             "day_of_week": parts[4],
#             "command_to_run": ' '.join(parts[5:])
#         }
#     def validate_fields(self):
#         self.validate_minute()
#         self.validate_hour()
#         self.validate_day_of_month()
#         self.validate_month()
#         self.validate_day_of_week()

#     def validate_minute(self):
#         minute = self.fields['minute']
#         if not (0 <= int(minute) < 60 or minute == '*'):
#             raise ValueError(f"Invalid minute field: {minute}")

#     def validate_hour(self):
#         hour = self.fields['hour']
#         if not (0 <= int(hour) < 24 or hour == '*'):
#             raise ValueError(f"Invalid hour field: {hour}")

#     def validate_day_of_month(self):
#         day_of_month = self.fields['day_of_month']
#         if not (1 <= int(day_of_month) <= 31 or day_of_month == '*'):
#             raise ValueError(f"Invalid day of month field: {day_of_month}")

#     def validate_month(self):
#         month = self.fields['month']
#         if not (1 <= int(month) <= 12 or month == '*'):
#             raise ValueError(f"Invalid month field: {month}")

#     def validate_day_of_week(self):
#         day_of_week = self.fields['day_of_week']
#         if not (0 <= int(day_of_week) <= 6 or day_of_week == '*'):
#             raise ValueError(f"Invalid day of week field: {day_of_week}")


class CronFieldValidator:
    
    def __init__(self, cron_input):
        self.cron_input = cron_input
        self.fields = self.parse_cron_input()
    
    
    def parse_cron_input(self) -> dict[str, str]:
        
        parts = self.cron_input.split()
        if len(parts) < 6:
            raise ValueError("Cron input must contain at least 6 fields: minute, hour, day_of_month, month, day_of_week, command_to_run")
        
        return {
            "minute": parts[0],
            "hour": parts[1],
            "day_of_month": parts[2],
            "month": parts[3],
            "day_of_week": parts[4],
            "command_to_run": ' '.join(parts[5:])
        }
            
    def validate_fields(self):
        self.validate_minute()
        self.validate_hour()
    
    def validate_minute(self):
        
        minute = self.fields['minute']
        if not (0 <= int(minute) < 60 or minute == '*'):
            raise ValueError(f"Invalid Minutes {minute}")
    
    def validate_hour(self):
        
        hour = self.fields['hour']
        if not (0 <= int(hour) < 24 or hour == '*'):
            raise ValueError(f"Invalid Hour {hour}")

    def validate_day_of_month(self):
        day_of_month = self.fields['day_of_month']
        if not (1 <= int(day_of_month) <= 31 or day_of_month == '*'):
            raise ValueError(f"Invalid day of month field: {day_of_month}")

    def validate_month(self):
        
        month = self.fields['month']
        if not (1 <= int(month) <= 12 or month == '*'):
            raise ValueError(f"Invalid month field: {month}")
        
        def validate_day_of_week(self):
            day_of_week = self.fields['day_of_week']
            if not (0 <= int(day_of_week) <= 6 or day_of_week == '*'):
                raise ValueError(f"Invalid day of week field: {day_of_week}")
    
    
    

# class CronFieldParser:
#     def __init__(self, cron_input):
#         self.validator = CronFieldValidator(cron_input)

#     def parse(self):
#         try:
#             self.validator.validate_fields()
#             return self.validator.fields
#         except ValueError as e:
#             print(f"Error parsing cron input: {e}")
#             sys.exit(1)
#     def get_parsed_fields(self):
#         return self.validator.fields


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cronfield_parser.py \"<minute> <hour> <day_of_month> <month> <day_of_week> <command_to_run>\"")
        sys.exit(1)

    cron_input = sys.argv[1]
    print("Parsing cron input:", cron_input)

    