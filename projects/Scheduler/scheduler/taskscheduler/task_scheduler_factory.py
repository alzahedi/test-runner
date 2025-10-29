from ..taskscheduler.sequential_task_scheduler import SequentialScheduler
from ..taskscheduler.parallel_task_scheduler import ParallelScheduler

from ..common.constants import *
from ..common.metrics import Metrics


class TaskSchedulerFactory(object):
    """
    Factory class to create a scheduler instance
    """

    @staticmethod
    def createTaskScheduler(strategy: str, mode: str, metrics: Metrics):
        """
        Create a task scheduler for the given strategy
        """

        if strategy == SEQUENTIAL_STRATEGY:
            return SequentialScheduler(mode, metrics)
        elif strategy == PARALLEL_STRATEGY:
            return ParallelScheduler(mode, metrics)
        else:
            raise ValueError("Unknown strategy: " + strategy)
