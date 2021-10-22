# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 14:14:56 2021

@author: Jan Peter Mortensen Christiansen
"""
import Monkey
import os
import pandas as pd
import preheat_open as ph
import TimeKeeper
Monkey.patch_Unit_load_data()  # monkey patch preheat_open.Unit.load_data()
ph.logging.set_logging_level("warning")  # set logging level to warning
TK = TimeKeeper.TimeKeeper()  # make TimeKeeper object to handle datetimes and schedules

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


# %% create directory for data


data_dir = "data"
if not os.path.isdir(data_dir):
    os.mkdir(data_dir)
    print("Created directory: "+data_dir)

# %%


# set up building
b_id = 2245
b = ph.Building(b_id)


# make datetimes for data interval
end_date = TK.get_now_local()  # when to start the query
qu_interval = 60*60*24*7  # time interval of the query
start_date = TK.get_now_local_delay(-qu_interval)  # when to stop the query
resolutions = ["raw", "minute", "hour"]  # resolutions to queue

for res in resolutions:
    # get data for given res
    [sensor_names, sensor_data] = get_data_from_building_object(b, start_date, end_date, res)

    data = pd.DataFrame()  # make dataframe for saving
    data.index.name = "TIME"  # change the name of the index to TIME
    for (name, sensor) in zip(sensor_names, sensor_data):
        data[name] = sensor  # merge the sensor names and data into dataframe

    if data.empty:
        print('No data for resolution "'+res+'" in interval')
    else:
        # split data
        split_data = []  # create list to hold multiple dataframes
        for day in set(data.index.day):
            split_data.append(data[data.index.day == day])  # split data into days

        # check if there are old data for each day
        for day in split_data:
            dirname = data_dir+"/"+day.index[0].strftime("%Y-%m-%d")  # directory name for the day
            filename = dirname+"/"+res+".csv"  # filename for the given resolution
            data_exists = os.path.isfile(filename)  # check if a file exists for the day and resolution

            # load old data
            old_data = pd.DataFrame()  # create DataFrame for existing data
            new_data = pd.DataFrame()  # create DataFrame for new data
            new_set = False
            if data_exists:
                old_data = pd.read_csv(filename, index_col=day.index.name)  # read existing data from file
                if not old_data.empty:  # check if file did include data
                    new_data = day[day.index > old_data.index[-1]]  # filter only data after the last timestamp in file
                    new_set = not(bool(len(day.columns) == len(old_data.columns)))  # are there added or missing columns

            # make directory
            if not os.path.isdir(dirname):  # check if directory exists
                os.mkdir(dirname)  # create directory
                print("Created directory: "+dirname)

            # save new data
            if data_exists:
                if new_data.empty:
                    print("No new data for "+dirname[len(data_dir)+1::]+" at time resolution "+res)
                else:
                    new_data.to_csv(filename, mode="a", header=new_set)  # append data to existig file
                    print(str(len(new_data))+" line"+["", "s"][len(new_data) > 1]+" appended to "+filename)
            else:
                day.to_csv(filename)  # create new file with data
                print(str(len(day))+" line"+["", "s"][len(day) > 1]+" saved to "+filename)
