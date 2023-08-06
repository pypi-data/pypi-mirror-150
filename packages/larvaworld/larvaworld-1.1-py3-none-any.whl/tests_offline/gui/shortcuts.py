import PySimpleGUI as sg
import pandas as pd
import pygame as pg
import numpy as np

names = ['trajectories', 'draw_midline', 'draw_contour', 'draw_centroid', 'draw_head', 'visible_clock', 'visible_ids',
         'visible_state', 'color_behavior', 'random_colors', 'black_background']
default_value = [False, True, True, False, False, True, False, True, False, False, False]
default_key = ['P', 'M', 'C', 'E', 'H', 'T', 'TAB', 'S', 'B', 'R', 'G']

current_key = default_key

string = 'K_'
current_shortcut = [string + x for x in current_key]

sg.theme('DarkGrey13')

text_args = {'font': 'Courier 10',
             'size': (15, 1),
             'justification': 'center'}

layout_function = [

    [sg.Text("Function", font='Default 15')],

    [sg.Text(names[0], font='Default 12')],
    [sg.Text(names[1], font='Default 12')],
    [sg.Text(names[2], font='Default 12')],
    [sg.Text(names[3], font='Default 12')],
    [sg.Text(names[4], font='Default 12')],
    [sg.Text(names[5], font='Default 12')],
    [sg.Text(names[6], font='Default 12')],
    [sg.Text(names[7], font='Default 12')],
    [sg.Text(names[8], font='Default 12')],
    [sg.Text(names[9], font='Default 12')],
    [sg.Text(names[10], font='Default 12')]

]

layout_input = [
    [sg.Text("Enter New Shortcut Here", font='Default 15')],

    [sg.InputText(default_text=current_key[0], key='-SHORTCUT_TRAJECTORIES-', font=12)],
    [sg.InputText(default_text=current_key[1], key='-SHORTCUT_DRAW_MIDLINE-', font=12)],
    [sg.InputText(default_text=current_key[2], key='-SHORTCUT_DRAW_CONTOUR-', font=12)],
    [sg.InputText(default_text=current_key[3], key='-SHORTCUT_DRAW_CENTROID-', font=12)],
    [sg.InputText(default_text=current_key[4], key='-SHORTCUT_DRAW_HEAD-', font=12)],
    [sg.InputText(default_text=current_key[5], key='-SHORTCUT_VISIBLE_CLOCK-', font=12)],
    [sg.InputText(default_text=current_key[6], key='-SHORTCUT_VISIBLE_IDS-', font=12)],
    [sg.InputText(default_text=current_key[7], key='-SHORTCUT_VISIBLE_STATE-', font=12)],
    [sg.InputText(default_text=current_key[8], key='-SHORTCUT_COLOR_BEHAVIOR-', font=12)],
    [sg.InputText(default_text=current_key[9], key='-SHORTCUT_RANDOM_COLORS-', font=12)],
    [sg.InputText(default_text=current_key[10], key='-SHORTCUT_BLACK_BACKGROUND-', font=12)]

]

layout = [
    [sg.Text('Keyboard Shortcut Configuration', font='Default 20')],
    [sg.Column(layout_function), sg.Column(layout_input)],
    [sg.Button('Set to Default'), sg.Button('Close')]
]

window = sg.Window('Keyboard Shortcut Configuration', layout, default_element_size=(20, 1), element_padding=(1, 1),
                   return_keyboard_events=True, finalize=True)

while True:
    event, values = window.read()
    try:
        current_key[0] = values['-SHORTCUT_TRAJECTORIES-']
        current_key[1] = values['-SHORTCUT_DRAW_MIDLINE-']
        current_key[2] = values['-SHORTCUT_DRAW_CONTOUR-']
        current_key[3] = values['-SHORTCUT_DRAW_CENTROID-']
        current_key[4] = values['-SHORTCUT_DRAW_HEAD-']
        current_key[5] = values['-SHORTCUT_VISIBLE_CLOCK-']
        current_key[6] = values['-SHORTCUT_VISIBLE_IDS-']
        current_key[7] = values['-SHORTCUT_VISIBLE_STATE-']
        current_key[8] = values['-SHORTCUT_COLOR_BEHAVIOR-']
        current_key[9] = values['-SHORTCUT_RANDOM_COLORS-']
        current_key[10] = values['-SHORTCUT_BLACK_BACKGROUND-']
        current_shortcut = [string + x for x in current_key]
    except:
        print("Enter a new Key")

    if event == sg.WIN_CLOSED or event == 'Close':
        break

    if event == 'Set to Default':
        current_key = default_key
        current_shortcut = [string + x for x in current_key]
        print('Your settings were set to default.')
