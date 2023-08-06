import PySimpleGUI as sg

messages = [
    'This is the start of your chat!',
    'demo messages',
    'dont know what to right',
]

command = ['Delete', 'Favourite', 'Reply', 'Copy', 'Edit']
cmd_layout = [[sg.Button(cmd, size=(10, 1))] for cmd in command]
layout = [
    [sg.Listbox(values=messages, size=(35, 22), key='chat'),
     sg.Column(cmd_layout)],
    [sg.InputText(key='input', size=(25, 10)),
     sg.Button('Send', bind_return_key=True, size=(9, 1))],
]
window = sg.Window("Test", layout, finalize=True)
window['input'].expand(expand_x=True)

while True:

    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    print(event, values)

window.close()