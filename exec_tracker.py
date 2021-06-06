"""
Because GitHub actions sometimes runs in irregular intervals 
based on server demand and not strictly once every hour,
we will track and store latest execution times. If the script
was not executed that morning at lets say 5 AM local time, we
would run it afterwards at 6AM, 7AM etc...
"""

from datetime import datetime
import pytz

EXEC_TIMETABLE_FILENAME = 'EXEC_TIMETABLE.txt'
DEFAULT_LOCAL_TIME = 5  # AM


class ExecTracker:
    def __init__(self) -> None:
        self.exec_timetable_filepath = EXEC_TIMETABLE_FILENAME

    def _timetable_file_open(self, mode='r'):
        try:
            file = open(self.exec_timetable_filepath, mode)
        except:
            # create file if it doesn't exist
            file = open(self.exec_timetable_filepath, 'w')
            file.close()
            return self._timetable_file_open(mode)
        else:
            return file

    def _timetable_file_close(self, file):
        file.close()

    def _get_exec_times(self):
        file = self._timetable_file_open()
        lines = file.readlines()

        execution_times = []
        for line in lines:
            # remove newline character
            line = line.replace('\n', '')
            # append to list of exec times
            execution_times.append(datetime.strptime(
                line, '%Y-%m-%d %H:%M:%S.%f'))

        self._timetable_file_close(file)

        # return the list
        return execution_times

    def store_execution_time(self):
        # open timetable file for appending
        file = self._timetable_file_open('a')
        # get UTC time
        time_now = datetime.utcnow()
        # store UTC time as string
        file.write(str(time_now) + '\n')
        self._timetable_file_close(file)

    def load_execution_times(self):
        return self._get_exec_times()

    def clean_exec_times(self):
        # open timetable file for both reading and writing
        # if it doesnt exist exit with error
        # else convert every UTC string to UTC time and exec_timetable_filepathexec_timetable_filepathppend to list
        # filter only the ones with the same day
        # close file
        # overwrite the new one
        # close file
        pass

    def script_executed_today(self, local_time):
        exec_times = self.load_execution_times()
        # convert local time to UTC
        local_time_utc = local_time.astimezone(pytz.utc)
        # go through every UTC time and return if the script did run that day
        for exec_time in exec_times:
            if exec_time.date() == local_time_utc.date():
                return True

        return False
