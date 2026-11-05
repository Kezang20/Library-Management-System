import wx


def show_message(event):
    wx.MessageBox(
        "Hello! Welcome to wxPython.",
        "Message",
        wx.OK | wx.ICON_INFORMATION
    )


app = wx.App()

frame = wx.Frame(
    None,
    title="wxPython Hello World",
    size=(400, 250)
)

panel = wx.Panel(frame)

label = wx.StaticText(
    panel,
    label="Hello World!",
    pos=(130, 50)
)

font = wx.Font(
    18,
    wx.FONTFAMILY_DEFAULT,
    wx.FONTSTYLE_NORMAL,
    wx.FONTWEIGHT_BOLD
)
label.SetFont(font)

button = wx.Button(
    panel,
    label="Click Me",
    pos=(145, 120),
    size=(100, 35)
)

button.Bind(wx.EVT_BUTTON, show_message)

frame.Centre()
frame.Show()

app.MainLoop()


