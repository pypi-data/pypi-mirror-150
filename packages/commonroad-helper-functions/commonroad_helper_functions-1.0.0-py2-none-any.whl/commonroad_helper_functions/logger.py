"""Logging functions for CommonRoad.

Author: Matthias Rowold <matthias.rowold@tum.de
"""

from commonroad.scenario.trajectory import State
from pathlib import Path
import csv
import os


class ObjectStateLogger(object):
    """Object State Logger

    Logging class for objects with commonroad states
    """

    def __init__(self, log_path: str, object_id):

        self._log_path = log_path
        self._object_id = object_id

        # create log path if it does not exist
        Path(self._log_path).mkdir(parents=True, exist_ok=True)
        # create a unique logging file name
        self._log_file = self._log_path + '/object_' + str(self._object_id)

    def initialize(self):
        # header in logging file
        self._header = (
            'x, y, '
            + ', '.join([slot for slot in State.__slots__ if slot != 'position'])
            + ', time'
            + '\n'
        )
        with open(self._log_file, "w") as fh:
            fh.write(self._header)

    def log_state(self, state: State, time: float):
        """Log State

        This method writes a commonroad state to the log file

        :param state: commonroad state
        :param time: time of the state to log
        """
        if not isinstance(state, State):
            raise TypeError('state is not of the correct type "State"')

        log_values = []
        for slot in State.__slots__:
            if hasattr(state, slot):
                if slot == 'position':
                    log_values.append(state.position[0])
                    log_values.append(state.position[1])
                else:
                    log_values.append(state.__getattribute__(slot))
            else:
                log_values.append(None)

        log_text = ', '.join([str(val) for val in log_values]) + ', ' + str(time) + '\n'

        with open(self._log_file, "a") as fh:
            fh.write(log_text)

    def log_file2dict(self):
        """Log file to dictionary

        This method generates a dictionary with all logged states

        :return: dictionary with logged states
        :rtype: dict
        """
        log_dict = dict()

        with open(self._log_file, "r") as fh:
            reader = csv.reader(fh, delimiter=',')

            for column in list(zip(*reader)):
                log_dict[column[0]] = []
                for i in range(1, len(column)):
                    try:
                        log_dict[column[0]].append(float(column[i]))
                    except ValueError:
                        log_dict[column[0]].append(None)

        self._log_dict = log_dict

        return log_dict


# EOF
