"""
Because GitHub actions sometimes runs in irregular intervals 
caused by high server demand and not strictly once every hour,
we will track and store latest execution times. If the script
was not executed that morning at 5 AM local time, GitHub Actions
would run it sometimes later that day.
If the script is ran more than once per day, it would check every
time if it was already executed. If yes then skip.
Execution times are being saved in exec_timetable.json file.
Before closing execution timetable file it is being encrypted
with AES into exec_timetable.json.aes file with some password.
Be sure that the password is kept as a secret.
"""

from datetime import datetime
import json
from os import path, remove
from pyAesCrypt import encryptFile, decryptFile
from utils import debug

DATE_FORMAT = '%m/%d/%Y, %H:%M:%S'
TIMETABLE_PATH = path.abspath(path.join('logs', 'exec_timetable.json'))
TIMETABLE_PATH_ENCRYPTED = TIMETABLE_PATH + '.aes'
BUFFERSIZE = 64 * 1024


class ExecTracker:
    def __init__(self, password):
        self.timetable_modified = False
        self.__password = password

        if path.exists(TIMETABLE_PATH_ENCRYPTED):
            debug('Found exec timetable file')
            decryptFile(TIMETABLE_PATH_ENCRYPTED, TIMETABLE_PATH, self.__password, BUFFERSIZE)
            self.timetable = open(TIMETABLE_PATH, 'r')
            self.exec_times = json.load(self.timetable)
            debug(self.exec_times)
        else:
            debug('Did not found exec timetable file. Creating new.')
            self.timetable = open(TIMETABLE_PATH, 'w')
            self.timetable.write('{}')
            self.exec_times = {}
        
        self.timetable.close()

    def close(self):
        if self.timetable_modified:
            debug('Timetable is modified. Saving now.')
            self.timetable = open(TIMETABLE_PATH, 'r+')
            json.dump(self.exec_times, self.timetable, indent=4)
            self.timetable.close()
        else:
            debug('Timetable was not modified.')

        debug('Showing execution timetable before encryption.')
        debug(self.exec_times)

        debug('Encrypting file.')
        if path.exists(TIMETABLE_PATH_ENCRYPTED):
            remove(TIMETABLE_PATH_ENCRYPTED)

        encryptFile(TIMETABLE_PATH, TIMETABLE_PATH_ENCRYPTED, self.__password, BUFFERSIZE)
        debug('Deleting original file.')
        remove(TIMETABLE_PATH)


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
