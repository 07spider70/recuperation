# -*- coding: utf-8 -*-
import codes.process as ps
from codes.plot import Plotter


#hlavny spustaci subor

ps.process_month_extern_data()
Plotter("data/data_extern_mont_temp.txt", "ext_month_temp.png").plot()

