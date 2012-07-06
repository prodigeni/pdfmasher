ownerclass = 'PMMainWindow'
ownerimport = 'PMMainWindow.h'

result = Window(995, 657, "PdfMasher")
loadButton = Button(result, "Load PDF")
filenameLabel = Label(result, "<filename>")
mainTabView = TabView(result)
tableTab = mainTabView.addTab("Table")
elementsTable = TableView(tableTab.view)
elementsTable.OBJC_CLASS = 'PMElementTableView'
sideTabView = TabView(result)

owner.openedFileLabelView = filenameLabel
owner.topTabView = mainTabView
owner.bottomTabView = sideTabView
owner.elementsTableView = elementsTable

elementsTable.allowsMultipleSelection = True
loadButton.action = Action(owner, 'loadPDF:')

loadButton.width = 87
mainTabView.width = 660

loadButton.packToCorner(Pack.UpperLeft)
loadButton.y += 7 # Maximize screen estate
filenameLabel.packRelativeTo(loadButton, Pack.Right)
filenameLabel.fill(Pack.Right)
mainTabView.packRelativeTo(loadButton, Pack.Below)
mainTabView.fill(Pack.Below)
mainTabView.setAnchor(Pack.UpperLeft, growX=True, growY=True)
sideTabView.packRelativeTo(mainTabView, Pack.Right, align=Pack.Above)
sideTabView.fill(Pack.Right)
sideTabView.fill(Pack.Below)
sideTabView.setAnchor(Pack.UpperRight, growY=True)

elementsTable.packToCorner(Pack.UpperLeft)
elementsTable.fill(Pack.Right)
elementsTable.fill(Pack.Below)
elementsTable.setAnchor(Pack.UpperLeft, growX=True, growY=True)
