window_size = (2000, 1200)

def col_size(x_frac=1.0, y_frac=1.0, win_size=None):
    if win_size is None:
        win_size = window_size
    return int(win_size[0] * x_frac), int(win_size[1] * y_frac)

def get_disp_name(name) -> str:
    n = "%s%s" % (name[0].upper(), name[1:])
    n = n.replace('_', ' ')
    return n