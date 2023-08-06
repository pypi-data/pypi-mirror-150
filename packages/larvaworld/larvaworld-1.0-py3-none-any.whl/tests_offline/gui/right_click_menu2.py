import PySimpleGUI as sg

commands = ['Delete', 'Favourite', 'Reply', 'Copy', 'Edit']
# layout = [
#     [sg.Listbox(size=(35, 22), key='chat', values=messages,
#                 right_click_menu=['&Right', commands])]
# ]
window = sg.Window("Windows-like program",
                   layout=[[]],
                   default_element_size=(12, 1),
                   grab_anywhere=True,
                   right_click_menu=['&Right', commands],
                   default_button_element_size=(12, 1))

while True:

    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    print(event, values)

window.close()