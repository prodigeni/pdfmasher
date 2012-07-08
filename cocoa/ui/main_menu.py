ownerclass = 'PMAppDelegate'
ownerimport = 'PMAppDelegate.h'

result = Menu("")
appMenu = result.addMenu("PdfMasher")
fileMenu = result.addMenu("File")
editMenu = result.addMenu("Edit")
windowMenu = result.addMenu("Window")
helpMenu = result.addMenu("Help")

appMenu.addItem("About PdfMasher", Action(owner, 'showAboutBox'))
appMenu.addItem("Check for Updates...", Action(owner.updater, 'checkForUpdates:'))
appMenu.addSeparator()
NSApp.servicesMenu = appMenu.addMenu("Services")
appMenu.addSeparator()
appMenu.addItem("Hide PdfMasher", Action(NSApp, 'hide:'), 'cmd+h')
appMenu.addItem("Hide Others", Action(NSApp, 'hideOtherApplications:'), 'cmd+alt+h')
appMenu.addItem("Show All", Action(NSApp, 'unhideAllApplications:'))
appMenu.addSeparator()
appMenu.addItem("Quit PdfMasher", Action(NSApp, 'terminate:'), 'cmd+q')

fileMenu.addItem("Load PDF", Action(owner.mainWindow, 'loadPDF:'), 'cmd+o')
fileMenu.addItem("Close", Action(None, 'performClose:'), 'cmd+w')

editMenu.addItem("Cut", Action(None, 'cut:'), 'cmd+x')
editMenu.addItem("Copy", Action(None, 'copy:'), 'cmd+c')
editMenu.addItem("Paste", Action(None, 'paste:'), 'cmd+v')
editMenu.addItem("Select All", Action(None, 'selectAll:'), 'cmd+a')

windowMenu.addItem("Minimize", Action(None, 'performMinimize:'), 'cmd+m')
windowMenu.addItem("Zoom", Action(None, 'performZoom:'))
windowMenu.addSeparator()
windowMenu.addItem("Bring All to Front", Action(None, 'arrangeInFront:'))

helpMenu.addItem("PdfMasher Help", Action(owner, 'openHelp'), 'cmd+?')
helpMenu.addItem("PdfMasher Website", Action(owner, 'openWebsite'), 'cmd+?')
