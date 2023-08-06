import abc
import time

from six import add_metaclass


@add_metaclass(abc.ABCMeta)
class Clock:

    @abc.abstractmethod
    def current_millis(self):
        """
        :return: epoch millis
        :rtype: int
        """
        pass


class SystemClock(Clock):

    def current_millis(self):
        return int(round(time.time() * 1000))


SYSTEM_CLOCK = SystemClock()
