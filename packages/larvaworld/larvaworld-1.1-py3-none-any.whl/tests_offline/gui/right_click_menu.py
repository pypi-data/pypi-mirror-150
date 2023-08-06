import PySimpleGUI as sg

def RightClickMenuCallback(event, element):
    widget = element.Widget
    current = widget.curselection()
    if current:
        widget.selection_clear(current[0])
    index = widget.nearest(event.y)
    widget.selection_set(index)
    element.TKRightClickMenu.tk_popup(event.x_root, event.y_root, 0)
    element.TKRightClickMenu.grab_release()

messages = [
    'This is the start of your chat!',
    'demo messages',
    'dont know what to right',
]

command = ['Delete', 'Favourite', 'Reply', 'Copy', 'Edit']
layout = [
    [sg.Listbox(size=(35, 22), key='chat', values=messages,
        right_click_menu=['&Right', command])],
    [sg.InputText(key='input', size=(25, 10)),
     sg.Button('Send', bind_return_key=True, size=(9, 1))],
]
window = sg.Window("Test", layout, finalize=True)
chat = window['chat']
chat.Widget.bind('<Button-3>', lambda event,
    element=chat: RightClickMenuCallback(event, element))

while True:

    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    print(event, values)

window.close()