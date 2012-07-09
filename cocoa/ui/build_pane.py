ownerclass = 'PMBuildPane'
ownerimport = 'PMBuildPane.h'

result = View(None, 201, 350)
step1Label = Label(result, "Step 1: Generate Mardown")
generateMarkdownButton = Button(result, "Generate Markdown")
lastGenDescLabel = Label(result, "")
step2Label = Label(result, "Step 2: Post processing")
editMarkdownButton = Button(result, "Edit Markdown")
viewHTMLButton = Button(result, "View HTML")
revealButton = Button(result, "Reveal in Finder")
step3Label = Label(result, "Step 3: E-book creation")
ebookTypeRadio = RadioButtons(result, ["MOBI", "EPUB"], columns=2)
titleLabel = Label(result, "Title:")
titleField = TextField(result, "")
authorLabel = Label(result, "Author:")
authorField = TextField(result, "")
createEbookButton = Button(result, "Create e-book")

owner.lastGenDescLabel = lastGenDescLabel
owner.editMarkdownButton = editMarkdownButton
owner.revealMarkdownButton = revealButton
owner.viewHTMLButton = viewHTMLButton
owner.createEbookButton = createEbookButton
owner.ebookTitleTextField = titleField
owner.ebookAuthorTextField = authorField
owner.ebookTypeRadioButtons = ebookTypeRadio

generateMarkdownButton.action = Action(owner, 'generateMarkdown')
editMarkdownButton.action = Action(owner, 'editMarkdown')
viewHTMLButton.action = Action(owner, 'viewHTML')
revealButton.action = Action(owner, 'revealInFinder')
ebookTypeRadio.action = Action(owner, 'selectEbookType')
createEbookButton.action = Action(owner, 'createEbook')
lastGenDescLabel.font = Font(FontFamily.Label, FontSize.SmallControl)
lastGenDescLabel.height = 14

for button in (generateMarkdownButton, editMarkdownButton, viewHTMLButton, revealButton, createEbookButton):
    button.width = 155
ebookTypeRadio.width = 126
ebookTypeRadio.height = 18
titleLabel.width = 50
authorLabel.width = 50

step1Label.packToCorner(Pack.UpperLeft)
step1Label.fill(Pack.Right)
generateMarkdownButton.packRelativeTo(step1Label, Pack.Below, Pack.Left)
lastGenDescLabel.packRelativeTo(generateMarkdownButton, Pack.Below, Pack.Left)
lastGenDescLabel.fill(Pack.Right)
step2Label.packRelativeTo(lastGenDescLabel, Pack.Below, Pack.Left)
step2Label.fill(Pack.Right)
editMarkdownButton.packRelativeTo(step2Label, Pack.Below, Pack.Left)
viewHTMLButton.packRelativeTo(editMarkdownButton, Pack.Below, Pack.Left)
revealButton.packRelativeTo(viewHTMLButton, Pack.Below, Pack.Left)
step3Label.packRelativeTo(revealButton, Pack.Below, Pack.Left)
step3Label.fill(Pack.Right)
ebookTypeRadio.packRelativeTo(step3Label, Pack.Below, Pack.Left)
titleField.packRelativeTo(ebookTypeRadio, Pack.Below, Pack.Right)
titleLabel.packRelativeTo(titleField, Pack.Left, Pack.Middle)
titleField.fill(Pack.Left)
titleField.fill(Pack.Right)
titleField.setAnchor(Pack.UpperLeft, growX=True)
authorField.packRelativeTo(titleField, Pack.Below, Pack.Right)
authorLabel.packRelativeTo(authorField, Pack.Left, Pack.Middle)
authorField.fill(Pack.Left)
authorField.setAnchor(Pack.UpperLeft, growX=True)
createEbookButton.packRelativeTo(authorLabel, Pack.Below, Pack.Left)
