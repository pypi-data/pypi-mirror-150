from test.application.launchoptions import cancel_options_with_proxy
from test.slurm_assertions import assert_job_canceled
from test.slurmoutput import DEFAULT_JOB_ID
from test.testdoubles.executor import SlurmJobExecutorSpy
from test.testdoubles.filesystem import DummyFilesystemFactory
from typing import Optional
from unittest.mock import Mock

from hpcrocket.core.application import Application
from hpcrocket.ui import UI


def make_sut(executor: SlurmJobExecutorSpy, ui: Optional[UI] = None) -> Application:
    return Application(executor, DummyFilesystemFactory(), ui or Mock())


def test__given_watch_options__when_running__should_poll_job_until_done() -> None:
    executor = SlurmJobExecutorSpy()
    sut = make_sut(executor)

    sut.run(cancel_options_with_proxy())

    assert_job_canceled(executor, DEFAULT_JOB_ID)
