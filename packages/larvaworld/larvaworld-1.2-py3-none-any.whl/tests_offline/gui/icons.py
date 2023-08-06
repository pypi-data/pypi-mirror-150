import PySimpleGUI as sg
# Note that the base64 string is quite long.  You can get the code from Trinket that includes the button
red_x_base64 = b'paste the base64 encoded string here'
red_x_base64 = sg.red_x     # Using this built-in little red X for this demo

layout = [  [sg.Text('My borderless window with a button graphic')],
            [sg.Button('', image_data=red_x_base64,
            button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0, key='Exit')]  ]

window = sg.Window('Window Title', layout, no_titlebar=True)

while True:             # Event Loop
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
window.close()