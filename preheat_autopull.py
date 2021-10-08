# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 14:14:56 2021

@author: Jan Peter Mortensen Christiansen
"""
import preheat_open as ph
import TimeKeeper
import json
TK = TimeKeeper.TimeKeeper()
ph.logging.set_logging_level("warning")

b_id = 2245
b = ph.Building(b_id)

delay = 60*60*24  # time delay in seconds
start_date = TK.get_now_local_delay(-delay)  # start time of the data query
end_date = TK.get_now_local()  # end/stop time of the data query
res = "raw"

b.load_data(start_date, end_date, res)  # load data for all sensors in building


# make list of sensors and data
sensor_names = []
sensor_data = []

# get all sensor names and data
for b_unit in b.units.values():  # check all building units
    for unit in b_unit:  # check all units in building unit
        if unit.has_data():  # check if units has any data in components
            for component in unit.components:  # check all components in unit
                # append the name of the sensor
                sensor_names.append(component.tag)
                # append the data from the sensor
                sensor_data.append(unit.data[component.name].to_frame())
        if unit.sub_units:  # check if unit has sub units
            for sub_unit in unit.sub_units:  # check all sub units in unit
                if sub_unit.has_data():  # check if sub unit has data
                    # append the name of the sensor
                    sensor_names.append(sub_unit.name)
                    # append the data from the sensor
                    sensor_data.append(sub_unit.data)
