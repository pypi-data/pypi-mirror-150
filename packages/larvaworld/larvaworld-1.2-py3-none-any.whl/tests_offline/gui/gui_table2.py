import PySimpleGUI as sg

def gui_row(label, option_list, key1, key2):
    return sg.Text(label, size=(15,1)), sg.OptionMenu(option_list, size=(15,5)), sg.Text('Did not understand this'), sg.Input(size=(10,1), key=key1), sg.Input(size=(10,1), key=key2)

layout = [  [sg.Text('The test of Reddit layout')],
            *[gui_row('test', (1,2,3,4,5), f'key1 {i}', f'key2 {i}') for i in range(6)],
            [sg.Button('Go'), sg.Button('Exit')]]

window = sg.Window('Window Title', layout)

while True:             # Event Loop
    event, values = window.read()
    print(event, values)
    if event in (None, 'Exit'):
        break
window.close()