import os
import pytest
import shutil
from scheduler import app
from scheduler.common.helper import Global
from scheduler.common.constants import STATUS_PASS, STATUS_FAIL
from scheduler.common.metrics import Metrics
from scheduler.configuration import Configuration


class TestScheduler:
    """
    Test the scheduler types: sequential, parallel
    """

    @pytest.fixture()
    def setup_dirs(self):
        """
        Initialize members
        """
        # Defines and creates log folder for running tests
        #
        Global.CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
        Global.WORKING_DIR = Global.CURRENT_PATH
        Global.LOG_DIR = Global.WORKING_DIR + '/.validate_log/'

        if os.path.exists(Global.LOG_DIR):
            shutil.rmtree(Global.LOG_DIR)
        os.makedirs(Global.LOG_DIR)

    def test_scheduler_sequential(self, setup_dirs, logger):
        """
        Test the sequential scheduler
        """

        # Constants
        #
        configFile = "config/config-scheduler-sequential.yaml"
        group1 = "Group 1"
        group2 = "Group 2"

        # Case 1: success tasks
        #

        logger.info("Running the success case for sequential ordering")

        metrics = Metrics()
        config = Configuration(configFile, "all")
        result = app.execGroups(config, metrics)

        assert result is True
        assert config.groups[group1]["Tasks"][0]["result"]["status"] == STATUS_PASS
        assert config.groups[group1]["Tasks"][1]["result"]["status"] == STATUS_PASS
        assert config.groups[group2]["Tasks"][0]["result"]["status"] == STATUS_PASS

        # Case 2: failed tasks with "waitall" mode
        #
        logger.info(
            "Running failure case for sequential ordering with wait all mode")

        config = Configuration(configFile, "all")
        config.mode = "waitall"
        config.groups[group1]["Tasks"][0]['Command'] = 'exit 1'
        result = app.execGroups(config, metrics)

        assert result is False
        assert config.groups[group1]["Tasks"][0]["result"]["status"] == STATUS_FAIL
        assert config.groups[group1]["Tasks"][1]["result"]["status"] == STATUS_PASS
        assert config.groups[group2]["Tasks"][0]["result"]["status"] == STATUS_PASS

        # Case 3: failed tasks with "failfast" mode
        #
        logger.info(
            "Running failure case for sequential ordering with wait all mode")

        config = Configuration(configFile, "all")
        config.mode = "failfast"
        config.groups[group1]["Tasks"][0]['Command'] = 'exit 1'
        result = app.execGroups(config, metrics)

        assert result is False
        assert config.groups[group1]["Tasks"][0]["result"]["status"] == STATUS_FAIL
        assert 'result' not in config.groups[group1]["Tasks"][1]
        assert 'result' not in config.groups[group2]["Tasks"][0]

    def test_scheduler_parallel(self, setup_dirs, logger):
        """
        Test the parallel scheduler
        """

        # Constants
        #
        configFile = "config/config-scheduler-parallel.yaml"
        group1 = "Group 1"
        group2 = "Group 2"

        # Case 1: success tasks
        #
        logger.info("Running the success case for parallel ordering")

        metrics = Metrics()
        config = Configuration(configFile, "all")
        result = app.execGroups(config, metrics)

        assert result is True
        assert 'result' in config.groups[group1]["Tasks"][0]
        assert 'result' in config.groups[group1]["Tasks"][1]
        assert 'result' in config.groups[group2]["Tasks"][0]

        # Case 2: failed tasks with "waitall" mode
        #
        logger.info(
            "Running the failure case for parallel ordering with waitall mode")

        config = Configuration(configFile, "all")
        config.mode = "waitall"
        config.groups[group1]["Tasks"][0]['Command'] = 'exit 1'
        result = app.execGroups(config, metrics)

        assert result is False
        assert 'result' in config.groups[group1]["Tasks"][0]
        assert 'result' in config.groups[group1]["Tasks"][1]
        assert 'result' in config.groups[group2]["Tasks"][0]

        # Case 3: failed tasks with "waitcurrent" mode
        #
        logger.info(
            "Running the failure case for parallel ordering with waitcurrent mode")

        config = Configuration(configFile, "all")
        config.mode = "failfast"
        config.groups[group1]["Tasks"][0]['Command'] = 'exit 1'
        result = app.execGroups(config, metrics)

        assert result is False
        assert 'result' in config.groups[group1]["Tasks"][0]
        assert 'result' in config.groups[group1]["Tasks"][1]
        assert 'result' not in config.groups[group2]["Tasks"][0]

        # Case 4: failed tasks with "failfast" mode
        #
        logger.info(
            "Running the failure case for parallel ordering with failfast mode")

        config = Configuration(configFile, "all")
        config.mode = "failfast"
        config.groups[group1]["Tasks"][0]['Command'] = 'exit 1'
        result = app.execGroups(config, metrics)

        assert result is False
        assert 'result' in config.groups[group1]["Tasks"][0]
        assert 'result' in config.groups[group1]["Tasks"][1]
        assert 'result' not in config.groups[group2]["Tasks"][0]
