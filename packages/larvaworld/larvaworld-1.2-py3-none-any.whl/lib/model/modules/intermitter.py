import os
import numpy as np
import pandas as pd

import lib.aux.dictsNlists as dNl
from lib.anal.fitting import BoutGenerator, critical_bout, exp_bout, get_exp_beta
from lib.aux import naming as nam
from lib.conf.stored.conf import loadConf
from lib.model.modules.basic import Effector



class BaseIntermitter(Effector):
    def __init__(self, locomotor=None, crawl_bouts=False, feed_bouts=False,
                 feeder_reoccurence_rate=None, feeder_reocurrence_as_EEB=True,
                 EEB_decay=1, save_to=None, EEB=0.5, **kwargs):
        super().__init__(**kwargs)
        self.locomotor = locomotor
        self.save_to = save_to
        self.crawler = locomotor.crawler if locomotor is not None else None
        self.feeder = locomotor.feeder if locomotor is not None else None
        self.turner = locomotor.turner if locomotor is not None else None
        self.EEB = EEB
        self.base_EEB = EEB
        self.cur_state = None

        self.feeder_reoccurence_rate = feeder_reoccurence_rate if feeder_reoccurence_rate is not None else self.EEB
        self.feeder_reocurrence_as_EEB = feeder_reocurrence_as_EEB
        self.crawl_bouts = crawl_bouts
        self.feed_bouts = feed_bouts

        self.EEB_decay = EEB_decay
        self.EEB_exp_coef = np.exp(-self.EEB_decay * self.dt)

        self.reset()

    def reset(self):
        self.t = 0
        self.total_t = 0
        self.ticks = 0
        self.total_ticks = 0

        self.pause_counter = 0
        self.current_pause_duration = None
        self.current_pause_ticks = None
        self.cum_pause_dur = 0
        self.pause_termination_allowed = True

        self.run_counter = 0
        self.current_run_duration = None
        self.current_run_ticks = None
        self.cum_run_dur = 0
        self.run_termination_allowed = True

        self.stridechain_counter = 0
        self.current_stridechain_length = None
        self.cum_stridechain_dur = 0
        self.current_numstrides = 0
        # self.stride_counter = 0

        self.feedchain_counter = 0
        self.current_feedchain_length = None
        self.cum_feedchain_dur = 0
        self.current_numfeeds = 0
        self.feed_counter = 0

        self.stridechain_lengths = []
        self.stridechain_durs = []
        self.feedchain_lengths = []
        self.feedchain_durs = []
        self.pause_durs = []
        self.run_durs = []
        self.feed_durs = []
        self.stride_durs = []

        self.stride_stop = False

    def step(self):
        super().count_time()
        self.update_state()
        return self.cur_state

    def generate_stridechain(self):
        pass

    def generate_pause(self):
        pass

    def disinhibit_locomotion(self):
        if np.random.uniform(0, 1, 1) >= self.EEB:
            if self.crawl_bouts:
                self.run_initiation()
                if self.crawler is not None:
                    self.crawler.start_effector()
                if self.feeder is not None:
                    self.feeder.stop_effector()
        else:
            if self.feed_bouts:
                self.current_feedchain_length = 1
                if self.feeder is not None:
                    self.feeder.start_effector()
                if self.crawler is not None:
                    self.crawler.stop_effector()
                self.cur_state = 'feed'

    def run_initiation(self) :
        self.cur_state='run'

    def inhibit_locomotion(self):
        # print('ffff')
        self.current_pause_duration = self.generate_pause()
        self.cur_state='pause'
        if self.crawl_bouts and self.crawler is not None:
            self.crawler.stop_effector()
            try :
                self.complete_iteration = False
                self.crawler.phi=0
            except :
                pass
            # self.crawler.
        if self.feed_bouts and self.feeder is not None:
            self.feeder.stop_effector()

    def update_state(self):
        self.stride_stop = False
        if self.current_stridechain_length is not None:
            if self.crawler.complete_iteration:
                self.current_numstrides += 1
                self.stride_stop = True
                # self.stride_counter += 1
                if self.current_numstrides >= self.current_stridechain_length:
                    self.register_stridechain()
                    self.inhibit_locomotion()

        elif self.current_feedchain_length is not None:
            if self.feeder.complete_iteration:
                self.current_numfeeds += 1
                self.feed_counter += 1
                if np.random.uniform(0, 1, 1) >= self.feeder_reoccurence_rate:
                    self.register_feedchain()
                    self.inhibit_locomotion()
                else:
                    self.current_feedchain_length += 1

        elif self.current_pause_duration is not None:
            if self.t > self.current_pause_duration and self.pause_termination_allowed:
                self.register_pause()
                self.disinhibit_locomotion()

        elif self.current_run_duration is not None:
            if self.t > self.current_run_duration and self.run_termination_allowed:
                self.register_run()
                self.inhibit_locomotion()

    def register_stridechain(self):
        self.stridechain_counter += 1
        self.cum_stridechain_dur += self.t
        self.stridechain_lengths.append(self.current_stridechain_length)
        self.stridechain_durs.append(self.t)
        self.t = 0
        self.current_numstrides = 0
        self.current_stridechain_length = None

    def register_feedchain(self):
        self.feedchain_counter += 1
        self.cum_feedchain_dur += self.t
        self.feedchain_lengths.append(self.current_feedchain_length)
        self.feedchain_durs.append(self.t)
        self.t = 0
        self.current_feedchain_length = None

    def register_pause(self):
        self.pause_counter += 1
        self.cum_pause_dur += self.t
        self.pause_durs.append(self.t)
        self.current_pause_duration = None
        self.t = 0


    def register_run(self):
        self.run_counter += 1
        self.cum_run_dur += self.t
        self.run_durs.append(self.t)
        self.current_run_duration = None
        self.t = 0

    def get_mean_feed_freq(self):
        try:
            f = self.feed_counter / (self.total_ticks * self.dt)
        except:
            f = self.feed_counter / self.total_t
        return f

    def build_dict(self):
        d = {}
        if self.total_t != 0:
            d[nam.cum('t')] = self.total_t
        else:
            d[nam.cum('t')] = self.total_ticks * self.dt
        d[nam.num('tick')] = self.total_ticks
        for c in ['feedchain', 'stridechain', 'pause']:
            t = nam.dur(c)
            l = nam.length(c)
            N = nam.num(c)
            cum_t = nam.cum(t)
            rt = nam.dur_ratio(c)
            d[t] = getattr(self, f'{t}s')
            d[N] = getattr(self, f'{c}_counter')
            d[cum_t] = getattr(self, cum_t)
            d[rt] = d[cum_t] / d[nam.cum('t')]
            if c in ['feedchain', 'stridechain']:
                d[l] = getattr(self, f'{l}s')
        d[nam.num('feed')] = sum(d[nam.length('feedchain')])
        d[nam.num('stride')] = sum(d[nam.length('stridechain')])
        d[nam.mean(nam.freq('feed'))] = d[nam.num('feed')] / d[nam.cum('t')]
        d[nam.mean(nam.freq('stride'))] = d[nam.num('stride')] / d[nam.cum('t')]

        return d

    def save_dict(self, path=None, dic=None):
        if dic is None:
            dic = self.build_dict()
        if path is None:
            if self.save_to is not None:
                path = self.save_to
            else:
                raise ValueError('No path to save intermittency dict')
        file = f'{path}/{self.locomotor.agent.unique_id}.txt'
        if not os.path.exists(path):
            os.makedirs(path)
        dNl.save_dict(dic, file)

    def update(self, max_refeed_rate=0.9, refeed_rate_coef=0, food_present=None, feed_success=None):
        if food_present is None:
            self.EEB *= self.EEB_exp_coef
        else:
            self.EEB = self.base_EEB
        if feed_success == 1:
            if self.feeder_reocurrence_as_EEB:
                self.feeder_reoccurence_rate = self.EEB
            else:
                self.feeder_reoccurence_rate = max_refeed_rate
        elif feed_success == -1:
            self.feeder_reoccurence_rate *= refeed_rate_coef

    @property
    def active_bouts(self):
        return self.current_stridechain_length, self.current_feedchain_length, self.current_pause_duration, self.current_run_duration

    def interrupt_locomotion(self):
        if self.current_pause_duration is None:
            if self.current_feedchain_length is not None:
                self.register_feedchain()
            elif self.current_stridechain_length is not None:
                self.register_stridechain()
            elif self.current_run_duration is not None:
                self.register_run()
            self.inhibit_locomotion()

    def trigger_locomotion(self):
        if self.current_pause_duration is not None:
            self.register_pause()
            self.disinhibit_locomotion()
#

class Intermitter(BaseIntermitter):
    def __init__(self, pause_dist=None, stridechain_dist=None, run_dist= None, run_mode='stridechain',**kwargs):
        super().__init__(**kwargs)
        if pause_dist.range is None and stridechain_dist.range is None:
            conf=loadConf('None.200_controls', 'Ref').bout_distros
            pause_dist=conf.pause
            stridechain_dist=conf.stride

        if run_mode=='stridechain' :
            if stridechain_dist is not None :
                self.stridechain_dist = BoutGenerator(**stridechain_dist, dt=1)
                self.run_dist = None
            else :
                run_mode = 'run'
        if run_mode=='run' :
            if run_dist is not None :
                self.run_dist = BoutGenerator(**run_dist, dt=self.dt)
                self.stridechain_dist = None
            else :
                raise ValueError ('None of stidechain or run distribution exist')
        self.pause_dist = BoutGenerator(**pause_dist, dt=self.dt)
        self.disinhibit_locomotion()

    def generate_stridechain(self):
        return self.stridechain_dist.sample()

    def generate_run(self):
        return self.run_dist.sample()

    def run_initiation(self):
        if self.stridechain_dist is not None:
            self.current_stridechain_length = self.stridechain_dist.sample()
            self.current_numstrides = 0
        elif self.run_dist is not None:
            self.current_run_duration = self.run_dist.sample()
            # self.cur_run_dur = 0
        self.cur_state = 'run'
        # self.locomotor.crawler.effector = True

    def generate_pause(self):
        return self.pause_dist.sample()


class OfflineIntermitter(Intermitter):
    def __init__(self, register_bouts=True, crawl_freq=10 / 7, feed_freq=2.0, **kwargs):
        super().__init__(**kwargs)
        self.register_bouts = register_bouts
        self.crawl_freq = crawl_freq
        self.feed_freq = feed_freq
        self.crawl_ticks = np.round(1 / (crawl_freq * self.dt)).astype(int)
        self.feed_ticks = np.round(1 / (feed_freq * self.dt)).astype(int)

    def step(self):
        super().count_ticks()
        t = self.ticks
        self.stride_stop = False
        if self.current_stridechain_length and t >= self.current_crawl_ticks:
            self.current_numstrides += 1
            # self.stride_counter += 1
            self.stride_stop = True
            if self.current_numstrides >= self.current_stridechain_length:
                self.register('stride')
                self.current_numstrides = 0
                self.current_stridechain_length = None
                self.current_pause_ticks = int(self.generate_pause() / self.dt)
                self.inhibit_locomotion()
        elif self.current_feedchain_length and t >= self.current_feed_ticks:
            self.feed_counter += 1
            if np.random.uniform(0, 1, 1) >= self.feeder_reoccurence_rate:
                self.register('feed')
                self.current_feedchain_length = None
                self.current_pause_ticks = int(self.generate_pause() / self.dt)
                self.inhibit_locomotion()
            else:
                self.current_feedchain_length += 1
        elif self.current_pause_ticks and t > self.current_pause_ticks:
            self.register('pause')
            self.current_pause_ticks = None
            self.disinhibit_locomotion()

    def disinhibit_locomotion(self):
        if np.random.uniform(0, 1, 1) >= self.EEB:
            if self.crawl_bouts:
                self.current_stridechain_length = self.generate_stridechain()
        else:
            if self.feed_bouts:
                self.current_feedchain_length = 1

    def inhibit_locomotion(self):
        pass

    def register(self, bout):
        if self.register_bouts:
            t = self.ticks
            dur = t * self.dt
            if bout == 'feed':
                self.feedchain_counter += 1
                self.cum_feedchain_dur += dur
                self.feedchain_lengths.append(self.current_feedchain_length)

            elif bout == 'stride':
                self.stridechain_counter += 1
                self.cum_stridechain_dur += dur
                self.stridechain_lengths.append(self.current_stridechain_length)

            elif bout == 'pause':
                self.pause_counter += 1
                self.cum_pause_dur += dur
                self.pause_durs.append(dur)

        self.reset_ticks()

    @property
    def current_crawl_ticks(self):
        return (self.current_numstrides + 1) * self.crawl_ticks

    @property
    def current_feed_ticks(self):
        return self.current_feedchain_length * self.feed_ticks


class NengoIntermitter(OfflineIntermitter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_stridechain_length = self.generate_stridechain()

    def disinhibit_locomotion(self):
        if np.random.uniform(0, 1, 1) >= self.EEB:
            self.crawler.set_freq(self.crawler.default_freq)
            if self.feeder is not None:
                self.feeder.set_freq(0)
            self.current_stridechain_length = self.generate_stridechain()
        else:
            if self.feeder is not None:
                self.feeder.set_freq(self.feeder.default_freq)
            self.crawler.set_freq(0)
            self.current_feedchain_length = 1

    def inhibit_locomotion(self):
        self.crawler.set_freq(0)
        if self.feeder is not None:
            self.feeder.set_freq(0)


class BranchIntermitter(BaseIntermitter):
    def __init__(self,pause_dist=None, stridechain_dist=None,sample=None,beta=None,c=0.7,sigma=1, **kwargs):
        super().__init__(**kwargs)
        if beta is not None :
            self.beta=beta
        elif sample is not None :
            from lib.conf.stored.conf import loadRef
            d = loadRef(sample)
            l_run = d.load_aux('distro', nam.length('stridechain'))
            self.beta = get_exp_beta(l_run)
        else :
            self.beta=0.15
        self.c=c
        self.sigma=sigma
        self.stridechain_min, self.stridechain_max = stridechain_dist['range']
        self.pau_min, self.pau_max = (np.array(pause_dist['range'])/self.dt).astype(int)
        self.disinhibit_locomotion()

    def generate_stridechain(self):
        return exp_bout(beta=self.beta, tmax=self.stridechain_max, tmin=self.stridechain_min)

    def generate_pause(self):
        return critical_bout(c=self.c, sigma=self.sigma, N=1000, tmax=self.pau_max, tmin=self.pau_min)*self.dt


class FittedIntermitter(OfflineIntermitter):
    def __init__(self, sample_dataset, **kwargs):
        sample = loadConf(sample_dataset, 'Ref')
        stored_conf = {
            'crawl_freq': sample['crawl_freq'],
            'feed_freq': sample['feed_freq'],
            'dt': sample['dt'],
            'stridechain_dist': sample['stride']['best'],
            'pause_dist': sample['pause']['best'],
            'feeder_reoccurence_rate': sample['feeder_reoccurence_rate'],
        }
        stored_conf.update(kwargs)
        stored_conf['crawl_bouts'] = True if stored_conf['crawl_freq'] is not None else False
        stored_conf['feed_bouts'] = True if stored_conf['feed_freq'] is not None else False
        # print(kwargs)
        super().__init__(**stored_conf)


def get_EEB_poly1d(sample=None, dt=None, **kwargs):
    if sample is not None:
        if type(sample) == str:
            sample = loadConf(sample, 'Ref')
        kws = sample['intermitter']
    else:
        kws = kwargs
    if dt is not None:
        kws['dt'] = dt

    EEBs = np.arange(0, 1.05, 0.05)
    ms = []
    for EEB in EEBs:
        inter = OfflineIntermitter(EEB=EEB, register_bouts=False, **kws)
        max_ticks = int(60 * 60 / inter.dt)
        while inter.total_ticks < max_ticks:
            inter.step()
        ms.append(inter.get_mean_feed_freq())
    z = np.poly1d(np.polyfit(np.array(ms), EEBs, 5))
    return z


def get_best_EEB(deb, sample):
    z = np.poly1d(sample['EEB_poly1d'])
    if type(deb) == dict:
        s = deb['feed_freq_estimate']
    else:
        s = deb.fr_feed
    return np.clip(z(s), a_min=0, a_max=1)


def get_EEB_time_fractions(sample=None, dt=None, **kwargs):
    if sample is not None:
        if type(sample) == str:
            sample = loadConf(sample, 'Ref')
        kws = sample['intermitter']
    else:
        kws = kwargs
    if dt is not None:
        kws['dt'] = dt

    rts = {f'{q} ratio': nam.dur_ratio(p) for p, q in
           zip(['stridechain', 'pause', 'feedchain'], ['crawl', 'pause', 'feed'])}
    EEBs = np.round(np.arange(0, 1, 0.02), 2)
    data = []
    for EEB in EEBs:
        inter = OfflineIntermitter(EEB=EEB, **kws)
        max_ticks = int(1 * 60 * 60 / inter.dt)
        while inter.total_ticks < max_ticks:
            inter.step()
        dic = inter.build_dict()
        ffr = inter.get_mean_feed_freq()
        entry = {'EEB': EEB, **{k: np.round(dic[v], 2) for k, v in rts.items()}, nam.mean(nam.freq('feed')): ffr}
        data.append(entry)
    df = pd.DataFrame.from_records(data=data)
    return df


if __name__ == "__main__":
    from lib.stor.larva_dataset import LarvaDataset

    sample = 'None.200_controls'
    sample = loadConf(sample, 'Ref')
    d = LarvaDataset(sample['dir'])
    d.config['EEB_poly1d'] = get_EEB_poly1d(**d.config['intermitter']).c.tolist()
    d.save_config()
