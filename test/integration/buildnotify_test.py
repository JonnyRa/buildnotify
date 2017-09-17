import os
import re

import keyring
import keyring.backend
import pytest
from PyQt5.QtWidgets import QWidget, QSystemTrayIcon
from builtins import str

from buildnotifylib import BuildNotify
from test.fake_conf import ConfigBuilder
from test.fake_keyring import FakeKeyring


@pytest.mark.functional
def test_should_consolidate_build_status(qtbot):
    keyring.set_keyring(FakeKeyring())
    parent = QWidget()
    file_path = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + "../../../data/cctray.xml")
    conf = ConfigBuilder().server("file://" + file_path).build()
    b = BuildNotify(parent, conf, 10)
    qtbot.addWidget(b.app)
    parent.show()

    qtbot.waitUntil(lambda: hasattr(b, 'app_ui'))

    def projects_loaded():
        assert len([str(a.text()) for a in b.app_ui.app_menu.menu.actions()]) == 11

    if QSystemTrayIcon.isSystemTrayAvailable():
        qtbot.waitUntil(lambda: re.compile("Last checked.*").match(b.app_ui.tray.toolTip()) is not None, timeout=5000)
        qtbot.waitUntil(projects_loaded)
