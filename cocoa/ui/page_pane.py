ownerclass = 'PMPageController'
ownerimport = 'PMPageController.h'

result = View(None, 602, 295)
pageView = View(result, 598, 257)
prevPageButton = Button(result, "<--")
pageNumberLabel = Label(result, "Page: 0")
nextPageButton = Button(result, "-->")
reorderModeCheckbox = Checkbox(result, "Re-order mode")

owner.pageLabelTextField = pageNumberLabel
owner.pageReprPlaceholder = pageView
owner.reorderModeButton = reorderModeCheckbox

prevPageButton.action = Action(owner, 'prevPage')
nextPageButton.action = Action(owner, 'nextPage')
reorderModeCheckbox.action = Action(owner, 'toggleShowOrder')

prevPageButton.width = 62
pageNumberLabel.width = 72
nextPageButton.width = 62

prevPageButton.packToCorner(Pack.LowerLeft)
# We override layout rules because we need as much screen estate for the page as we can get.
prevPageButton.y = 7
pageNumberLabel.packRelativeTo(prevPageButton, Pack.Right)
nextPageButton.packRelativeTo(pageNumberLabel, Pack.Right)
reorderModeCheckbox.packRelativeTo(nextPageButton, Pack.Right)
reorderModeCheckbox.fill(Pack.Right)
for view in (prevPageButton, pageNumberLabel, nextPageButton, reorderModeCheckbox):
    view.setAnchor(Pack.LowerLeft)
# Same as earlier, we need screen estate
pageView.x = prevPageButton.x
pageView.y = 35
pageView.fill(Pack.Right)
pageView.setAnchor(Pack.UpperLeft, growX=True, growY=True)
