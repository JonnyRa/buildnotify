BuildNotify
===========

BuildNotify is a CCMenu/CCTray equivalent for Ubuntu. It resides in your system tray and notifies you of the build status for different projects on your continuous integration servers. BuildNotify is largely inspired from the awesome CCMenu available for Mac.

Features
========

* Monitor projects on multiple CruiseControl continuous integration servers.
* Access to overall continuous integration status from the system tray.
* Access individual project pages through the tray menu.
* Receive notifications for fixed/broken/still failing builds.
* Easy access to the last build time for each project
* Customize build notifications.

.. image:: https://anaynayak.github.io/buildnotify/images/projectlist.png

Building from source
=======

The ubuntu package is pretty old!  This might mean you need to build from source.

To do so do the following::

    git clone https://github.com/anaynayak/buildnotify
    cd buildnotify
    chmod u+x setup.py
    sh setup.sh
    sudo setup.py install


this will put buildnotifyapplet.py on your path in ``/usr/local/bin``
