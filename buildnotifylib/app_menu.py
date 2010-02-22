import os
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from distance_of_time import DistanceOfTime
from preferences import PreferencesDialog

class AppMenu:
    def __init__(self, tray, widget, conf, build_icons):
        self.menu = QtGui.QMenu(widget)
        tray.setContextMenu(self.menu)
        self.conf = conf
        self.build_icons = build_icons

    def update(self, projects):
        projects.sort(lambda x, y: (x.lastBuildTime - y.lastBuildTime).days)
        self.menu.clear()
        for project in projects:
            self.create_menu_item(project.name, self.build_icons.for_status(project.get_build_status()), project.url, project.lastBuildTime)
        self.create_default_menu_items()
            
    def create_default_menu_items(self):
        self.menu.addSeparator()
        self.menu.addAction(QtGui.QAction("About", self.menu, triggered=self.about_clicked))
        self.menu.addAction(QtGui.QAction("Preferences", self.menu, triggered=self.preferences_clicked))
        self.menu.addAction(QtGui.QAction("Exit", self.menu, triggered=self.exit))
        
    def about_clicked(self,widget):
        QtGui.QMessageBox.about(self.menu, "About BuildNotify",
        "<b>BuildNotify</b> v 0.1 has been developed using PyQt4 and serves as a build notification tool for cruise control. In case of any suggestions/bugs," +
        "please visit <a href=\"http://bitbucket.org/Anay/buildnotify\">http://bitbucket.org/Anay/buildnotify</a> and provide your feedback.")

    def preferences_clicked(self, widget):
        self.preferences_dialog = PreferencesDialog(self.conf.get_urls())
        self.preferences_dialog.show()
        if self.preferences_dialog.exec_() == QtGui.QDialog.Accepted:
            self.conf.update_urls(self.preferences_dialog.get_urls())
            
    def exit(self,widget):
        sys.exit()

    def create_menu_item(self, label, icon, url, lastBuildTime):
        action = self.menu.addAction(icon, label + ", " + DistanceOfTime(lastBuildTime).age() + " ago")
        receiver = lambda url=url: self.open_url(self, url)
        QtCore.QObject.connect(action, QtCore.SIGNAL('triggered()'), receiver)

    def open_url(self, something, url) :
        os.system(self.conf.browser + " " + url + " &")
