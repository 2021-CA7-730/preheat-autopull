# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 14:14:56 2021

@author: Jan Peter Mortensen Christiansen
"""
import preheat_open as ph
import TimeKeeper
TK = TimeKeeper.TimeKeeper()
# %% monkey patch logging functions to mute the console output
VERBOSE = False


def info(self, msg: str, *args, **kwargs) -> None:
    if VERBOSE:
        self._get_logger().info(msg, *args, **kwargs)


ph.logging.Logging.info = info

# %%
b_id = 2245
b = ph.Building(b_id)

delay = 60*60*1  # time delay in seconds
start_date = TK.get_now_local_delay(-delay)
end_date = TK.get_now_local()
res = "raw"

b.load_data(start_date, end_date, res)


# make list of sensors and actuators
sensor_names = []
for b_unit in b.units.values():
    for unit in b_unit:
        if unit.components:
            for component in unit.components:
                sensor_names.append(component.tag)
        if unit.sub_units:
            for sub_unit in unit.sub_units:
                sensor_names.append(sub_unit.name)
