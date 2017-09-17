import pytest

from buildnotifylib.core.projects import ProjectsPopulator
from test.fake_conf import ConfigBuilder


@pytest.mark.functional
def test_should_fetch_projects(qtbot):
    conf = ConfigBuilder().build()
    populator = ProjectsPopulator(conf)
    with qtbot.waitSignal(populator.updated_projects, timeout=1000):
        populator.process()
