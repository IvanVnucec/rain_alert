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

import json
from os import path
from hashlib import pbkdf2_hmac

DATE_FORMAT = '%m/%d/%Y'
TIMETABLE_PATH = 'exec_timetable.json'


class ExecTracker:
    def __init__(self, secrets):
        self.timetable_modified = False
        self.__secrets = secrets

        if path.exists(TIMETABLE_PATH):
            print('DEBUG: Found exec timetable file')
            self.timetable = open(TIMETABLE_PATH, 'r')
            self.exec_times = json.load(self.timetable)
        else:
            print('DEBUG: Did not found exec timetable file. Creating new.')
            self.timetable = open(TIMETABLE_PATH, 'w')
            self.timetable.write('{}')
            self.exec_times = {}

        self.timetable.close()

    def __del__(self):
        if self.timetable_modified:
            self.timetable = open(TIMETABLE_PATH, 'r+')
            json.dump(self.exec_times, self.timetable, indent=4)
            self.timetable.close()

    def __generate_secure_key(self, string):
        string_bytes = string.encode('utf-8')
        secret_bytes = self.__secrets.encode('utf-8')
        hash = pbkdf2_hmac('sha256', string_bytes, secret_bytes, 100000)

        return hash.hex()

    def __generate_local_exec_time_key(self, location):
        local_time_str = location.get_local_time_str(DATE_FORMAT)
        return self.__generate_secure_key(local_time_str)

    def __generate_location_name_key(self, location):
        return self.__generate_secure_key(location.name)

    def script_executed_today(self, location):
        location_name_key = self.__generate_location_name_key(location)

        if location_name_key in self.exec_times:
            local_exec_time_key = self.__generate_local_exec_time_key(location)

            for exec_time_key in self.exec_times[location_name_key]:
                if exec_time_key == local_exec_time_key:
                    return True

        return False

    def mark_exec_time(self, location):
        self.timetable_modified = True

        location_name_key = self.__generate_location_name_key(location)
        exec_time_key = self.__generate_local_exec_time_key(location)

        if location_name_key in self.exec_times:
            self.exec_times[location_name_key].append(exec_time_key)
        else:
            self.exec_times[location_name_key] = [exec_time_key]
