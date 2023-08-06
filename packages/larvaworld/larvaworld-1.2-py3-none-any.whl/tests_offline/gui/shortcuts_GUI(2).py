import PySimpleGUI as sg
import copy


sg.theme('DarkGrey13')

w_kws = {
    'finalize': True,
    'resizable': True,
    'default_button_element_size': (6, 1),
    'default_element_size': (14, 1),
    'font': ('size', 8),
    'auto_size_text': False,
    'auto_size_buttons': False,
    'text_justification': 'left',
}


text1_args = {'font': 'Courier 8',
              'size': (14, 1),
              'justification': 'center'}

text2_args = {'font': 'Courier 8',
              'size': (10, 1),
              'justification': 'center'}

input_args = {'font': 'Courier 8',
              'size': (10, 1),
              'justification': 'center'}

# shortcut_vis_render = {
#    'mode': ['', 'video', 'image'],
#    'image_mode': ['final', 'snapshots', 'overlap'],
#    'video_speed': int,
#    'media_name': str,
#    'show_display': bool,
# }

shortcut_vis_draw = {
    # 'trajectory_dt' : ['MINUS', 'PLUS'],
    'trajectories': 'p',
    'focus_mode': 'f',
    'draw_head': 'h',
    'draw_centroid': 'e',
    'draw_midline': 'm',
    'draw_contour': 'c'
}

value_vis_draw = {
    # 'trajectory_dt' : ['MINUS', 'PLUS'],
    'trajectories': False,
    'focus_mode': False,
    'draw_head': False,
    'draw_centroid': False,
    'draw_midline': True,
    'draw_contour': True,
}

shortcut_vis_color = {
    'black_background': 'g',
    'random_colors': 'r',
    'color_behavior': 'b',
}

value_vis_color = {
    'black_background': False,
    'random_colors': False,
    'color_behavior': False,
}

shortcut_vis_aux = {
    'visible_clock': 't',
    # 'visible_scale': '',
    'visible_state': 'sigma',
    'visible_ids': 'TAB',
}

value_vis_aux = {
    'visible_clock': True,
    # 'visible_scale': '',
    'visible_state': True,
    'visible_ids': False,
}

shortcut_moving = {
    'move_up': 'ARROW UP',
    'move_down': 'ARROW DOWN',
    'move_left': 'ARROW LEFT',
    'move_right': 'ARROW RIGHT',
}

value_moving = {
    'move_up': True,
    'move_down': True,
    'move_left': True,
    'move_right': True,
}

shortcut_mouse = {
    'place_larvae': 'RIGHT MOUSE BUTTON',
    'edit_larvae': 'LEFT MOUSE BUTTON',
    '?': 'MIDDLE MOUSE BUTTON',
    'zoom_in': 'SCROLL UP',
    'zoom_up': 'SCROLL DOWN',
}

value_mouse = {
    'place_larvae': True,
    'edit_larvae': True,
    'function': True,
    'zoom_in': True,
    'zoom_up': True,
}

shortcut_all_default = {}
shortcut_all_default.update(shortcut_vis_draw)
shortcut_all_default.update(shortcut_vis_color)
shortcut_all_default.update(shortcut_vis_aux)
shortcut_all_default.update(shortcut_moving)
shortcut_all_default.update(shortcut_mouse)
shortcut_all_current = copy.deepcopy(shortcut_all_default)

shortcut_pygame = {k: f'pygame.K_{v}' for k, v in shortcut_all_current.items()}

value_all_default = {}
value_all_default.update(value_vis_draw)
value_all_default.update(value_vis_color)
value_all_default.update(value_vis_aux)
value_all_default.update(value_moving)
value_all_default.update(value_mouse)
value_all_current = copy.deepcopy(value_all_default)

layout_vis_draw = [
    [sg.Text("DRAW", **text1_args)],
    *[[sg.Text(k, **text1_args),
        sg.InputText(default_text=v, key=f'SHORT {k}', background_color='black', **input_args),
        sg.Button('Edit', k=f'EDIT {k}')] for k, v in shortcut_vis_draw.items()],
    [sg.Text("", **text1_args)],
]

layout_vis_draw_value = [
    [sg.Text("", **text1_args)],
    *[[sg.Checkbox(text='', key=f'VALUE {k}', disabled=False, default=v, pad=(5, 5), enable_events=True)]
      for k, v in value_vis_draw.items()],
    [sg.Text("", **text1_args)],
]

layout_vis_color = [
    [sg.Text("COLORS", **text1_args)],
    *[[sg.Text(k, **text1_args),
        sg.Text(text=v, key=f'SHORT {k}', background_color='black', **input_args),
        sg.Button('Edit', k=f'EDIT {k}')] for k, v in shortcut_vis_color.items()],
    [sg.Text("", **text1_args)],
]

layout_vis_color_value = [
    [sg.Text("", **text1_args)],
    *[[sg.Checkbox(text='', key=f'VALUE {k}', disabled=False, default=v, pad=(5, 5), enable_events=True)]
      for k, v in value_vis_color.items()],
    [sg.Text("", **text1_args)],
]

layout_vis_aux = [
    [sg.Text("AUX", **text1_args)],
    *[[sg.Text(k, **text1_args),
        sg.Text(text=v, key=f'SHORT {k}', background_color='black', **input_args),
        sg.Button('Edit', k=f'EDIT {k}')] for k, v in shortcut_vis_aux.items()],
    [sg.Text("", **text1_args)],
]

layout_vis_aux_value = [
    [sg.Text("", **text1_args)],
    *[[sg.Checkbox(text='', key=f'VALUE {k}', disabled=False, default=v, pad=(5, 5), enable_events=True)]
      for k, v in value_vis_aux.items()],
    [sg.Text("", **text1_args)],
]

layout_moving = [
    [sg.Text("MOVING", **text1_args)],
    *[[sg.Text(k, **text1_args),
        sg.Text(text=v, key=f'SHORT {k}', background_color='black', **input_args),
        sg.Button('Edit', k=f'EDIT {k}', disabled=True)] for k, v in shortcut_moving.items()],
    [sg.Text("", **text1_args)],
]

layout_moving_value = [
    [sg.Text("", **text1_args)],
    *[[sg.Checkbox(text='', key=f'VALUE {k}', disabled=False, default=v, pad=(5, 5), enable_events=True)] for
      k, v in value_moving.items()],
    [sg.Text("", **text1_args)],
]

layout_mouse = [
    [sg.Text("MOUSE", **text1_args)],
    *[[sg.Text(k, **text1_args),
        sg.Text(text=v, key=f'SHORT {k}', background_color='black', **input_args),
        sg.Button('Edit', k=f'EDIT {k}', disabled=True)] for k, v in shortcut_mouse.items()],
    [sg.Text("", **text1_args)],
]

layout_mouse_value = [
    [sg.Text("", **text1_args)],
    *[[sg.Checkbox(text='', key=f'VALUE {k}', disabled=False, default=v, pad=(5, 5), enable_events=True)]
      for k, v in value_mouse.items()],
    [sg.Text("", **text1_args)],
]

layout_col1 = layout_vis_draw + layout_vis_color + layout_vis_aux + layout_moving
              # + layout_mouse
layout_col2 = layout_vis_draw_value + layout_vis_color_value + layout_vis_aux_value + layout_moving_value
              # + layout_mouse_value

layout = [
    [sg.Text("FUNCTION", **text1_args), sg.Text("SHORTCUT", **input_args), sg.Text("", size=(6, 1)),
     sg.Text("TURN ON/OFF", **text1_args)],
    [sg.Column(layout=layout_col1), sg.Column(layout_col2, pad=(10, 5))],
    [sg.Button('Reset defaults'), sg.Button('Close')]
]

window = sg.Window('Keyboard Shortcuts', layout, return_keyboard_events=True,  **w_kws)

while True:
    event, values = window.read()
    print(event)
    for k, v in shortcut_all_current.items():
        if event == f'EDIT {k}':
            window[f'SHORT {k}'].update(background_color='dark grey')
            if len(event) == 1:
                shortcut_all_current[k] = {v: '%s - %s' % (event, ord(event))}
                print(shortcut_all_current)
            if event is not None:
                new_v = event
                print(shortcut_all_current)
            print('test')
        shortcut_pygame = {k: f'pygame.K_{v}' for k, v in shortcut_all_current.items()}
    for k, v in value_all_current.items():
        if f'VALUE {k}' in event:
            value_all_current[k] = not v
    if event == sg.WIN_CLOSED or event == 'Close':
        break

    elif event == 'Reset defaults':
        for k, v in shortcut_all_default.items():
            window[f'SHORT {k}'].update(disabled=True, value=v)
        for k, v in value_all_default.items():
            window[f'VALUE {k}'].update(disabled=False, value=v)
        popup = sg.popup_ok('Your settings were set to default.', title='default settings', font='Courier 10')
    else:
        for k in list(shortcut_all_current.keys()):
            new_v = values[f'SHORT {k}']
            if new_v != '':
                if new_v == shortcut_all_current[k]:
                    window[f'SHORT {k}'].update(value=v, background_color='black')
                elif new_v not in list(shortcut_all_current.values()):
                    window[f'SHORT {k}'].update(value=v, background_color='black')
                    shortcut_all_current[k] = new_v
                elif new_v == '+':
                    window[f'SHORT {k}'].update(value=v, background_color='black')
                    shortcut_all_current[k] = 'PLUS'
                elif new_v == '-':
                    window[f'SHORT {k}'].update(value=v, background_color='black')
                    shortcut_all_current[k] = 'MINUS'
                else:
                    window[f'SHORT {k}'].update(value='', background_color='red')
                    window[f'SHORT {k}'].set_focus()
        shortcut_pygame = {k: f'pygame.K_{v}' for k, v in shortcut_all_current.items()}
