# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 12:56:39 2020

@author: Simon Thorsteinsson
"""

import TimeKeeper as TimeKeeper

TK = TimeKeeper.TimeKeeper()

tz = TK.get_local_timezone()

date_str_start = '2020-08-01T12:00:00'
dt_start = TK.str2dt(date_str_start)

date_str_end = '2020-08-02T12:00:00'
dt_end = TK.str2dt(date_str_end)





TK.dt_diff_sec(dt_start, dt_end)

schedule =  TK.create_schedule(date_str_start, date_str_end, 600)

values = len(schedule)*[1]

std_plan = TK.create_std_plan(schedule, values)

