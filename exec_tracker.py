"""
Because GitHub actions sometimes runs in irregular intervals 
caused by high server demand and not strictly once every hour,
we will track and store latest execution times. If the script
was not executed that morning at 5 AM local time, GitHub Actions
would run it sometimes later that day.
If the script is ran more than once per day, it would check every
time if it was already executed. If yes then skip.
Execution times are being saved in exec_timetable.json file.
"""

from datetime import datetime
import json
from os import path

DATE_FORMAT = '%m/%d/%Y, %H:%M:%S'
TIMETABLE_PATH = 'exec_timetable.json'


class ExecTracker:
    def __init__(self):
        self.timetable_modified = False

        if path.exists(TIMETABLE_PATH):
            self.timetable = open(TIMETABLE_PATH, 'r')
            self.exec_times = json.load(self.timetable)
        else:
            self.timetable = open(TIMETABLE_PATH, 'w')
            self.timetable.write('{}')
            self.exec_times = {}

        self.timetable.close()

    def __del__(self):
        if self.timetable_modified:
            self.timetable = open(TIMETABLE_PATH, 'r+')
            json.dump(self.exec_times, self.timetable, indent=4)
            self.timetable.close()

    def script_executed_today(self, location):
        if location.name in self.exec_times:
            local_time = location.get_local_time()

            for exec_time_str in self.exec_times[location.name]:
                exec_time = datetime.strptime(exec_time_str, DATE_FORMAT)

                if exec_time.date() == local_time.date():
                    return True

        return False

    def mark_exec_time(self, location):
        self.timetable_modified = True

        location_name = location.name
        local_time_str = location.get_local_time().strftime(DATE_FORMAT)

        if location_name in self.exec_times:
            self.exec_times[location_name].append(local_time_str)
        else:
            self.exec_times[location_name] = [local_time_str]
