# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 14:14:56 2021

@author: Jan Peter Mortensen Christiansen
"""
import preheat_open as ph
import TimeKeeper
TK = TimeKeeper.TimeKeeper()
# %%

VERBOSE = False


def info(self, msg: str, *args, **kwargs) -> None:
    if VERBOSE:
        self._get_logger().info(msg, *args, **kwargs)


ph.logging.Logging.info = info

# %% hent building

b_id = 2245
b = ph.Building(b_id)
