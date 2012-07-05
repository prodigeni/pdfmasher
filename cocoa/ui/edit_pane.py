ownerclass = 'PMEditPane'
ownerimport = 'PMEditPane.h'

result = View(None, 245, 282)
normalButton = Button(result, "Normal")
ignoredButton = Button(result, "Ignored")
titleButton = Button(result, "Title")
tofixButton = Button(result, "To Fix")
footnoteButton = Button(result, "Footnote")
hideIgnoredCheckbox = Checkbox(result, "Hide ignored elements")
editTextView = TextView(result)
saveButton = Button(result, "Save")
cancelButton = Button(result, "Cancel")

owner.saveButton = saveButton
owner.cancelButton = cancelButton
owner.editTextView = editTextView
owner.hideIgnoredButton = hideIgnoredCheckbox

normalButton.action = Action(owner, 'selectNormal')
ignoredButton.action = Action(owner, 'selectIgnored')
titleButton.action = Action(owner, 'selectTitle')
tofixButton.action = Action(owner, 'selectToFix')
footnoteButton.action = Action(owner, 'selectFootnote')
hideIgnoredCheckbox.action = Action(owner, 'toggleHideIgnored')
saveButton.action = Action(owner, 'saveEdits')
cancelButton.action = Action(owner, 'cancelEdits')

for button in (normalButton, ignoredButton, titleButton, tofixButton, footnoteButton):
    button.width = 84
editTextView.height = 97
saveButton.bezelStyle = const.NSRoundRectBezelStyle
saveButton.width = 70
cancelButton.bezelStyle = const.NSRoundRectBezelStyle
cancelButton.width = 70

normalButton.packToCorner(Pack.UpperLeft)
ignoredButton.packRelativeTo(normalButton, Pack.Right, Pack.Middle)
titleButton.packRelativeTo(normalButton, Pack.Below, Pack.Left)
tofixButton.packRelativeTo(ignoredButton, Pack.Below, Pack.Left)
footnoteButton.packRelativeTo(titleButton, Pack.Below, Pack.Left)
hideIgnoredCheckbox.packRelativeTo(footnoteButton, Pack.Below, Pack.Left)
hideIgnoredCheckbox.fill(Pack.Right)
editTextView.packRelativeTo(hideIgnoredCheckbox, Pack.Below, Pack.Left)
editTextView.fill(Pack.Right)
editTextView.setAnchor(Pack.UpperLeft, growX=True, growY=True)
saveButton.packRelativeTo(editTextView, Pack.Below, Pack.Right)
saveButton.setAnchor(Pack.LowerRight)
cancelButton.packRelativeTo(saveButton, Pack.Left, Pack.Middle)
cancelButton.setAnchor(Pack.LowerRight)
