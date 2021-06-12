"""
Because GitHub actions sometimes runs in irregular intervals 
based on server demand and not strictly once every hour,
we will track and store latest execution times. If the script
was not executed that morning at lets say 5 AM local time, we
would run it afterwards at 6AM, 7AM etc...
"""

from datetime import datetime
import json

DATE_FORMAT = '%m/%d/%Y, %H:%M:%S'
DEFAULT_LOCAL_TIME = 5  # AM


class ExecTracker:
    def __init__(self) -> None:
        pass

    def timetable_open(self, path):
        try:
            timetable = open(path, 'r+')
        except FileNotFoundError:
            timetable = open(path, 'w')
            timetable.write("{}")
            timetable.close()
            return self.timetable_open(path)
        else:
            return timetable

    def timetable_close(self, timetable):
        timetable.close()

    def load_exec_times(self, timetable):
        return json.load(timetable)

    def script_executed_today(self, exec_times, location):
        if location.name in exec_times:
            for exec_time_str in exec_times[location.name]:
                exec_time = datetime.strptime(exec_time_str, DATE_FORMAT)
                if exec_time.date() == location.get_local_time_utc().date():
                    return True

        return False

    def append_exec_time(self, exec_times, location):
        location_name = location.name
        local_time_utc_str = location.get_local_time_utc().strftime(DATE_FORMAT)

        if location_name in exec_times:
            exec_times[location_name].append(local_time_utc_str)
        else:
            exec_times[location_name] = [local_time_utc_str]

    def timetable_store(self, timetable, exec_times):
        timetable.seek(0)
        json.dump(exec_times, timetable, indent=4)
