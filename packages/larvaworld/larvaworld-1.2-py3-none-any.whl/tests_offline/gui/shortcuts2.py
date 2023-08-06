import copy

import PySimpleGUI as sg
import pandas as pd
import pygame as pg
import numpy as np

shortcut_defaults = {
    # 'trajectory_dt' : ['MINUS', 'PLUS'],
    'trajectories': 'p',
    'focus_mode': 'f',
    'draw_centroid': 'e',
    'draw_head': 'h',
    'draw_midline': 'm',
    'draw_contour': 'c',
    'visible_clock': 't',
    'visible_ids': 'TAB',
    'visible_state': 'sigma',
    'color_behavior': 'b',
    'random_colors': 'r',
    'black_background': 'g',
    'larva_collisions': 'y',
    # 'zoom' : ,
    'snapshot #': 'i',
    # 'odorscape #' : 'o'
}

shortcut_current = copy.deepcopy(shortcut_defaults)

# names = ['trajectories', 'draw_midline', 'draw_contour', 'draw_centroid', 'draw_head', 'visible_clock', 'visible_ids',
#          'visible_state', 'color_behavior', 'random_colors', 'black_background']
default_value = [False, True, True, False, False, True, False, True, False, False, False]
# default_key = ['P', 'M', 'C', 'E', 'H', 'T', 'TAB', 'S', 'B', 'R', 'G']


sg.theme('DarkGrey13')

text1_args = {'font': 'Courier 10',
              'size': (18, 1),
              'justification': 'center'}

text2_args = {'font': 'Courier 10',
              'size': (10, 1),
              'justification': 'center'}

layout_function = [
    [sg.Text("FUNCTION", **text1_args), sg.Text("SHORTCUT", **text2_args)],
    *[[sg.Text(k, **text1_args),
       sg.InputText(default_text=v, key=f'SHORT {k}', disabled=True, disabled_readonly_background_color='black',
                    **text2_args), sg.Button('Edit', k=f'EDIT {k}')] for k, v in shortcut_defaults.items()],
]

layout = [
    # [sg.Text('Keyboard Shortcuts', font='Default 15')],
    [sg.Column(layout_function)],
    [sg.Button('Reset defaults'), sg.Button('Close')]
]

window = sg.Window('Keyboard Shortcuts', layout, default_element_size=(20, 1), element_padding=(1, 1),
                   return_keyboard_events=True, finalize=True)

while True:
    event, values = window.read()
    print(values)
    if event == sg.WIN_CLOSED or event == 'Close':
        break
    elif 'EDIT' in event:
        k = event.split()[-1]
        window[f'SHORT {k}'].update(disabled=False, value='')
        window[f'SHORT {k}'].set_focus()

    elif event == 'Reset defaults':
        for k, v in shortcut_defaults.items():
            window[f'SHORT {k}'].update(disabled=True, value=v)
        print('Your settings were set to default.')

    else:
        for k in list(shortcut_current.keys()):
            new_v = values[f'SHORT {k}']
            if new_v != '':
                if new_v == shortcut_current[k]:
                    window[f'SHORT {k}'].update(disabled=True)
                elif new_v not in list(shortcut_current.values()):
                    window[f'SHORT {k}'].update(disabled=True)
                    shortcut_current[k] = new_v
                else :
                    window[f'SHORT {k}'].update(disabled=False, value='')
                    window[f'SHORT {k}'].set_focus()
