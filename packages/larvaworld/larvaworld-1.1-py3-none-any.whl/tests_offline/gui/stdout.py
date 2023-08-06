import remi.gui as gui
from remi import start, App
import sys

try:
    from io import StringIO
except:
    from cStringIO import StringIO

stdout_string_io = StringIO()
sys.stdout = stdout_string_io


class MyApp(App):
    def idle(self):
        stdout_string_io.seek(0)
        lines = stdout_string_io.readlines()
        lines.reverse()
        self.stdout_text_input_widget.set_text("".join(lines))

    def main(self):
        # creating a container VBox type, vertical (you can use also HBox or Widget)
        main_container = gui.VBox(width=300, height=200, style={'margin': '0px auto'})

        print("test")

        self.stdout_text_input_widget = gui.TextInput(singleline=False, width="100%", height="100%")
        self.stdout_text_input_widget.attributes['disabled'] = 'true'

        bt_do_a_print = gui.Button("do a print")
        bt_do_a_print.onclick.connect(self.do_a_print)

        main_container.append([self.stdout_text_input_widget, bt_do_a_print])
        # returning the root widget
        return main_container

    def do_a_print(self, emitter):
        print("this print will be appended to the textInput widget")


if __name__ == "__main__":
    start(MyApp, start_browser=True)