from typing import Any

from kivy import Config
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader

from tests.kivy_gui.gui.aux.functions import window_size

Config.set('graphics', 'width', window_size[0])
Config.set('graphics', 'height', window_size[1])


class LarvaworldGui(App):
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        # from tests.kivy_gui.gui.tabs.analysis_tab import AnalysisTab
        # from tests.kivy_gui.gui.tabs.batch_tab import BatchTab
        # from tests.kivy_gui.gui.tabs.env_tab import EnvTab
        # from tests.kivy_gui.gui.tabs.essay_tab import EssayTab
        # from tests.kivy_gui.gui.tabs.life_tab import LifeTab
        # from tests.kivy_gui.gui.tabs.import_tab import ImportTab
        # from tests.kivy_gui.gui.tabs.sim_tab import SimTab
        # from tests.kivy_gui.gui.tabs.intro_tab import IntroTab
        # from tests.kivy_gui.gui.tabs.tutorial_tab import TutorialTab
        # from tests.kivy_gui.gui.tabs.video_tab import VideoTab
        # from tests.kivy_gui.gui.tabs.model_tab import ModelTab
        # from tests.kivy_gui.gui.tabs.settings_tab import SettingsTab
        # cls.tab_dict = {
        # 'introduction': (IntroTab, None, None),
        # 'larva-model': (ModelTab, 'Model', 'model_conf'),
        # 'life-history': (LifeTab, 'Life', 'life'),
        # 'environment': (EnvTab, 'Env', 'env_conf'),
        # 'simulation': (SimTab, 'Exp', 'exp_conf'),
        # 'batch-run': (BatchTab, 'Batch', 'batch_conf'),
        # 'essay': (EssayTab, 'Essay', 'essay_conf'),
        # 'import': (ImportTab, 'Group', None),
        # 'analysis': (AnalysisTab, None, None),
        # 'videos': (VideoTab, None, None),
        # 'tutorials': (TutorialTab, None, None),
        # 'settings': (SettingsTab, None, None)
        # }
        cls.tab_dict = {
            'introduction': (None, None),
            'larva-model': ('Model', 'model_conf'),
            'life-history': ('Life', 'life'),
            'environment': ('Env', 'env_conf'),
            'simulation': ('Exp', 'exp_conf'),
            'batch-run': ('Batch', 'batch_conf'),
            'essay': ('Essay', 'essay_conf'),
            'import': ('Group', None),
            'analysis': (None, None),
            'videos': (None, None),
            'tutorials': (None, None),
            'settings': (None, None)
        }
        # cls.tabgroups = {
        #     'introduction': ['introduction'],
        #     'models': ['larva-model', 'life-history'],
        #     'environment': ['environment'],
        #     'data': ['import', 'analysis'],
        #     'simulations': ['simulation', 'batch-run', 'essay'],
        #     'resources': ['tutorials', 'videos'],
        #     'settings': ['settings'],
        # }
        return App.__new__(cls)

    def __init__(self, tabs=None, **kwargs):
        super().__init__(**kwargs)
        if tabs is None:
            tabs = list(self.tab_dict.keys())
        self.tabs = tabs

    def build(self):
        cs, ds, gs = {}, {}, {}
        # dic = {}
        # for n in tabs:
        #     ii = self.tab_dict[n]
        #     ts[n] = ii[0](name=n, gui=self, conftype=ii[1])
        #     l, c, d, g = ts[n].build()
        #     cs.update(c)
        #     ds.update(d)
        #     gs.update(g)
        #     dic[n] = sg.Tab(n, l, background_color=self.background_color, key=f'{n} TAB')
        #     ls.append(dic[n])
        #
        # tab_kws = {'font': ("Helvetica", 13, "normal"), 'selected_title_color': 'darkblue', 'title_color': 'grey',
        #            'tab_background_color': 'lightgrey'}
        #
        # l_tabs = sg.TabGroup([ls], key='ACTIVE_TAB', tab_location='topleft', **tab_kws)
        #
        # l0 = [[sg.Pane([sg.vtop(l_tabs), sg.vbottom(self.terminal)], handle_size=30)]]
        # return l0, cs, ds, gs, ts
        tp = TabbedPanel(do_default_tab=False)
        for n in self.tabs:
            kws = {'name': n, 'gui': self, 'conftype': self.tab_dict[n][0], 'dtype': self.tab_dict[n][1]}
            th = TabbedPanelHeader(text=n)
            tp.add_widget(th)
            if n == 'introduction':
                from tests.kivy_gui.gui.tabs.intro_tab import IntroTab
                func = IntroTab
            elif n == 'videos':
                from tests.kivy_gui.gui.tabs.video_tab import VideoTab
                func = VideoTab
            elif n == 'settings':
                from tests.kivy_gui.gui.tabs.settings_tab import SettingsTab
                func = SettingsTab
            else :
                func = None
            if func is not None :
                th.content, c, d, g = func(**kws).build()
                cs.update(c)
                ds.update(d)
                gs.update(g)

        return tp


if __name__ == "__main__":
    # from tests.kivy_gui.gui.aux.gui import LarvaworldGui

    # larvaworld_gui = LarvaworldGui(tabs=['videos'])
    larvaworld_gui = LarvaworldGui()
    larvaworld_gui.run()
