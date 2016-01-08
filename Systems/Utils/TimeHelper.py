import datetime


class Time:
    @staticmethod
    def now():
        return datetime.datetime.now()

    @staticmethod
    def interval_as_float(time_interval):
        result = float(time_interval.seconds)  # add seconds to result
        result += float(time_interval.microseconds / 1000000.0)  # add scaled microseconds
        return result
