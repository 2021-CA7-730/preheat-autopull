# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 14:14:56 2021

@author: Jan Peter Mortensen Christiansen
"""
import os
import pandas as pd
import datetime as dt
import preheat_open as ph
import TimeKeeper
TK = TimeKeeper.TimeKeeper()  # make TimeKeeper object to handle datetimes and schedules
ph.logging.set_logging_level("warning")  # set logging level to warning

# %% function definitions


def get_data_from_building_object(b, start_date, end_date, res):
    b.clear_data()  # clear old data
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

    return [sensor_names, sensor_data]

# %%


# set up building
b_id = 2245
b = ph.Building(b_id)


# make data directory for today
# create directory for time in data not for when data was pulled
dirname = TK.get_now_local().strftime("%Y-%m-%d")
if not os.path.isdir(dirname):
    # create directory
    os.mkdir(dirname)
    print("Directory created: "+dirname)


# make datetimes for data interval
now = TK.get_now_local()  # datetime now
delay = 60*60*24
start_date = TK.get_now_local_delay(-delay)
day_start = dt.datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=now.tzinfo)  # start time of the data query

end_date = now  # end/stop time of the data query
resolutions = ["raw", "minute", "hour"]  # resolutions to queue

for res in resolutions:

    # get data for given res
    [sensor_names, sensor_data] = get_data_from_building_object(b, start_date, end_date, res)
    # make dataframe for saving
    data = pd.DataFrame()
    data.index.name = "TIME"
    for (name, sensor) in zip(sensor_names, sensor_data):
        data[name] = sensor

    # data = [data[data.index < day_start], data[data.index >= day_start]]
    # for data in data:
    #     if not data.empty:
    #         date = data.index[-1].strftime("%Y-%m-%d")

    filename = dirname+"/"+res+".csv"  # filename for the given resolution
    DATA_EXISTS = os.path.isfile(filename)

    # load old data
    old_data = pd.DataFrame()
    new_data = pd.DataFrame()
    if DATA_EXISTS:
        old_data = pd.read_csv(filename, index_col=data.index.name)
        if not old_data.empty:
            # add missing timestamps
            old_time = old_data.index[-1]
            # new_data = dem der ikke er i old_data
            new_data = data[data.index > old_time]
            # add missing columns
            for column in list(old_data.columns):
                if column not in list(data.columns):
                    new_data[column] = old_data[column]

    if not DATA_EXISTS:
        data.to_csv(filename)
        print(str(len(data))+" line"+["", "s"][len(data) > 1]+" added to "+filename)
    else:
        if new_data.empty:
            print("no new data for time resolution "+res)
        else:
            # save resolution data
            new_data.to_csv(filename, mode="a", header=False)
            print(str(len(new_data))+" line"+["", "s"][len(new_data) > 1]+" appended to "+filename)
