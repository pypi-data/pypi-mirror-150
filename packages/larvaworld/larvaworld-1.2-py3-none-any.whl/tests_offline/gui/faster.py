import PySimpleGUI as sg

def layout_tabgroup(key, number):
    layout = []
    treedata = sg.TreeData()
    for i in range(number):
        layout_tab = [
            [sg.Tree(data=treedata, headings=['None'], num_rows=2),
             sg.Table([], headings=['None'], auto_size_columns=False, col_widths=[10], num_rows=2)]]
        layout.append([sg.Tab(f"{key} {i}", layout_tab, key=f"{key} {i}")])
    return layout

sg.theme("DarkBlue")
sg.set_options(font=('Courier New', 12))

layout = [
    [sg.TabGroup(layout_tabgroup("A", 5))],
    [sg.TabGroup(layout_tabgroup("B", 10))],
    [sg.TabGroup(layout_tabgroup("C", 15))],
    [sg.TabGroup(layout_tabgroup("D", 20))],
    [sg.TabGroup(layout_tabgroup("E", 25))],
]
window = sg.Window("Title", layout, finalize=True)

def all_children(wid) :
    _list = wid.winfo_children()
    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())
    return _list

widget_list = all_children(window.TKroot)

for frame in widget_list:
    print(frame)
    if isinstance(frame, sg.tk.Frame) and frame.children == {}:
        frame.pack_forget()
        print('dd')

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    print(event, values)

window.close()