import PySimpleGUI as Sg
import copy
import time

pygame_keys1 = {
    'BackSpace': 'BACKSPACE',
    'Tab': 'TAB',
    'clear': 'CLEAR',
    'Return': 'RETURN',
    'Escape': 'ESCAPE',
    'space': 'SPACE',
    'exclam': 'EXCLAIM',
    'quotedbl': 'QUOTEDBL',
    'plus': 'PLUS',
    'comma': 'COMMA',
    'minus': 'MINUS',
    'period': 'PERIOD',
    'slash': 'SLASH',
    'numbersign': 'HASH',
    'Down:': 'DOWN',
    'Up:': 'UP',
    'Right:': 'RIGHT',
    'Left:': 'LEFT',
    'dollar': 'DOLLAR',
    'ampersand': 'AMPERSAND',
    'parenleft': 'LEFTPAREN',
    'parenright': 'RIGHTPAREN',
    'asterisk': 'ASTERISK',
}

pygame_keys2 = {
    'exclam': '!',
    'quotedbl': '"',
    'plus': '+',
    'comma': ',',
    'minus': '-',
    'period': '.',
    'slash': '/',
    'numbersign': '#',
    'dollar': '$',
    'ampersand': '&',
    'parenleft': '(',
    'parenright': ')',
    'asterisk': '*',
}

Sg.theme('DarkGrey13')

text1_args = {'font': 'Courier 10',
              'size': (18, 1),
              'justification': 'center'}

text2_args = {'font': 'Courier 10',
              'size': (10, 1),
              'justification': 'center'}

input_args = {'font': 'Courier 10',
              'size': (20, 1),
              'justification': 'center'}

head_args = {'font': 'Courier 10',
              'size': (18, 1),
              'justification': 'center'}

font_args = {'font': 'Courier 10',
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
    'move_up': 'UP',
    'move_down': 'DOWN',
    'move_left': 'LEFT',
    'move_right': 'RIGHT',
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
    [Sg.Text("DRAW", **text1_args)],
    *[[Sg.Text(k, **text1_args),
       Sg.InputText(default_text=v, key=f'SHORT {k}', disabled=True, disabled_readonly_background_color='black',
                    **input_args),
       Sg.Button('Edit', k=f'EDIT {k}')] for k, v in shortcut_vis_draw.items()],
    [Sg.Text("", **text1_args)],
]

layout_vis_draw_value = [
    [Sg.Text("", **text1_args)],
    *[[Sg.Checkbox(text='', key=f'VALUE {k}', disabled=False, default=v, pad=(5, 5), enable_events=True)]
      for k, v in value_vis_draw.items()],
    [Sg.Text("", **text1_args)],
]

layout_vis_color = [
    [Sg.Text("COLORS", **text1_args)],
    *[[Sg.Text(k, **text1_args),
       Sg.InputText(default_text=v, key=f'SHORT {k}', disabled=True, disabled_readonly_background_color='black',
                    **input_args),
       Sg.Button('Edit', k=f'EDIT {k}')] for k, v in shortcut_vis_color.items()],
    [Sg.Text("", **text1_args)],
]

layout_vis_color_value = [
    [Sg.Text("", **text1_args)],
    *[[Sg.Checkbox(text='', key=f'VALUE {k}', disabled=False, default=v, pad=(5, 5), enable_events=True)]
      for k, v in value_vis_color.items()],
    [Sg.Text("", **text1_args)],
]

layout_vis_aux = [
    [Sg.Text("AUX", **text1_args)],
    *[[Sg.Text(k, **text1_args),
       Sg.InputText(default_text=v, key=f'SHORT {k}', disabled=True, disabled_readonly_background_color='black',
                    **input_args),
       Sg.Button('Edit', k=f'EDIT {k}')] for k, v in shortcut_vis_aux.items()],
    [Sg.Text("", **text1_args)],
]

layout_vis_aux_value = [
    [Sg.Text("", **text1_args)],
    *[[Sg.Checkbox(text='', key=f'VALUE {k}', disabled=False, default=v, pad=(5, 5), enable_events=True)]
      for k, v in value_vis_aux.items()],
    [Sg.Text("", **text1_args)],
]

layout_moving = [
    [Sg.Text("MOVING", **text1_args)],
    *[[Sg.Text(k, **text1_args, pad=(0, 5)),
       Sg.InputText(default_text=v, key=f'SHORT {k}', disabled=True, disabled_readonly_background_color='black',
                    **input_args),
       Sg.Button('Edit', k=f'EDIT {k}')] for k, v in shortcut_moving.items()],
    [Sg.Text("", **text1_args)],
]

layout_moving_value = [
    [Sg.Text("", **text1_args)],
    *[[Sg.Checkbox(text='', key=f'VALUE {k}', disabled=False, default=v, pad=(5, 5), enable_events=True)] for
      k, v in value_moving.items()],
    [Sg.Text("", **text1_args)],
]

layout_mouse = [
    [Sg.Text("MOUSE", **text1_args)],
    *[[Sg.Text(k, **text1_args),
       Sg.InputText(default_text=v, key=f'SHORT {k}', disabled=True, disabled_readonly_background_color='black',
                    **input_args),
       Sg.Button('Edit', k=f'EDIT {k}', disabled=True)] for k, v in shortcut_mouse.items()],
    [Sg.Text("", **text1_args)],
]

layout_mouse_value = [
    [Sg.Text("", **text1_args)],
    *[[Sg.Checkbox(text='', key=f'VALUE {k}', disabled=False, default=v, pad=(5, 5), enable_events=True)]
      for k, v in value_mouse.items()],
    [Sg.Text("", **text1_args)],
]

layout_col1 = layout_vis_draw + layout_vis_color + layout_vis_aux + layout_moving + layout_mouse
layout_col2 = layout_vis_draw_value + layout_vis_color_value + layout_vis_aux_value \
              + layout_moving_value + layout_mouse_value

layout = [
    [Sg.Text("")],
    [Sg.Text("FUNCTION", **font_args, size=(18, 1)), Sg.Text("SHORTCUT", **font_args, size=(20, 1)),
     Sg.Text("", size=(10, 1)), Sg.Text(" TURN ON/OFF", **font_args, size=(12, 1))],
    [Sg.Text("")],
    [Sg.Column(layout=layout_col1), Sg.Column(layout_col2, pad=((60, 0), (0, 0)))],
    [Sg.Text("")],
    [Sg.Button('Reset defaults'), Sg.Button('Close')]
]

window = Sg.Window('Keyboard Shortcuts', layout, default_element_size=(20, 1), element_padding=(1, 1),
                   return_keyboard_events=True, finalize=True, resizable=True, element_justification='left')


def is_another_shortcut(set_of_shortcuts, element):
    if element in set_of_shortcuts:
        return True
    return False

delay=1
cur=None
while True:
    event, values = window.read()

    if event == Sg.WIN_CLOSED or event == 'Close':
        break
    elif event == 'Reset defaults':
        for k, v in shortcut_all_default.items():
            window[f'SHORT {k}'].update(disabled=True, value=v)
        shortcut_all_current = copy.deepcopy(shortcut_all_default)
        for k, v in value_all_default.items():
            window[f'VALUE {k}'].update(disabled=False, value=v)
        shortcut_all_current = copy.deepcopy(value_all_default)

    elif 'EDIT' in event:
        if cur is None :
            k = event.split()[-1]
            window[f'SHORT {k}'].update(disabled=False, value='', background_color='grey')
            window[f'SHORT {k}'].set_focus()
            cur=k
    elif cur is not None:
        if event == shortcut_all_current[cur]:
            window[f'SHORT {cur}'].update(disabled=True)
            cur=None
        elif is_another_shortcut(list(shortcut_all_current.values()), event):
            window[f'SHORT {cur}'].update(disabled=False, value='ALREADY USED',background_color='red')
            window.refresh()
            # window.disable()
            time.sleep(delay)
            # window.enable()
            window[f'SHORT {cur}'].update(disabled=False, value='', background_color='grey')
            window[f'SHORT {cur}'].set_focus()
        else :
            window[f'SHORT {cur}'].update(disabled=True, value=event)
            shortcut_all_current[cur] = event
            cur = None

        # print(values[f'SHORT {cur}'])
        # print(values[f'SHORT {cur}']=='ALREADY USED')



#     for k, v in shortcut_all_current.items():
#         if f'EDIT {k}' in event:
#             k = event.split()[-1]
#             window[f'SHORT {k}'].update(disabled=False, value='', background_color='grey')
#             window[f'SHORT {k}'].set_focus()
#             event, values = window.read()
#             # print(event, k, v)
#             if event is not None:
#                 # string = str(event)
#                 # x = slice(0, -3)
#                 # print(string, string[x], v)
#                 if event == v:
#                     # print(v,'zzz')
#                     window[f'SHORT {k}'].update(disabled=True, value=event)
#                 elif is_another_shortcut(shortcut_all_current.values(), event):
#                     window[f'SHORT {k}'].update(disabled=True, value='ALREADY USED',
#                                                     background_color='red', text_color='black')
#                     # time.sleep(delay)
#                     window[f'SHORT {k}'].update(disabled=False, value='', background_color='grey')
#                     window[f'SHORT {k}'].set_focus()
#                     # event, values = window.read()
#
# #                        time.sleep(2)
# #                        window[f'SHORT {k}'].update(disabled=True, value=shortcut_all_current[k],
# #                                                    background_color='black', text_color='white')
#                 elif event in list(pygame_keys1.keys()):
#                     if is_another_shortcut(shortcut_all_current.values(), pygame_keys1[event]):
#                         window[f'SHORT {k}'].update(disabled=True, value='ALREADY USED',
#                                                         background_color='red', text_color='black')
#                         # time.sleep(delay)
#                         window[f'SHORT {k}'].update(disabled=False, value='', background_color='grey')
#                         window[f'SHORT {k}'].set_focus()
#                         # event, values = window.read()
# #                            time.sleep(2)
# #                            window[f'SHORT {k}'].update(disabled=True, value=shortcut_all_current[k],
# #                                                        background_color='black', text_color='white')
#                     else:
#                         shortcut_all_current[k] = pygame_keys1[event]
#                         if event in pygame_keys2:
#                             window[f'SHORT {k}'].update(disabled=True, value=pygame_keys2[event], text_color='white')
#                         else:
#                             window[f'SHORT {k}'].update(disabled=True, value=pygame_keys1[event], text_color='white')
#                 elif len(event) == 1:
#                     shortcut_all_current[k] = event
#                     window[f'SHORT {k}'].update(disabled=True, value=shortcut_all_current[k], text_color='white')
#                 else:
#                     window[f'SHORT {k}'].update(disabled=True, value='KEY NOT POSSIBLE',
#                                                 background_color='red', text_color='black')
#                     # time.sleep(delay)
#                     window[f'SHORT {k}'].update(disabled=False, value='', background_color='grey')
#                     window[f'SHORT {k}'].set_focus()
#                     # event, values = window.read()
# #                    time.sleep(2)
# #                    window[f'SHORT {k}'].update(disabled=True, value=shortcut_all_current[k],
# #                                                background_color='black', text_color='white')
#             shortcut_pygame = {k: f'pygame.K_{v}' for k, v in shortcut_all_current.items()}
#             # print(shortcut_pygame[k])
#     for k, v in value_all_current.items():
#         if f'VALUE {k}' in event:
#             value_all_current[k] = not v

