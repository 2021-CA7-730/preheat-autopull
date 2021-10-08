# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 13:31:14 2020

@author: Simon Thorsteinsson
"""

import datetime
import pandas as pd
from dateutil import tz

class TimeKeeper():
    def __init__(self):
        self.timezone = self.get_local_timezone()
    
    def get_local_timezone(self):
        return datetime.timezone(datetime.timedelta(0))
        
    def create_schedule(self, time_start, time_end, step_size):
        
        dt_start = self.str2dt(time_start)
        dt_end = self.str2dt(time_end)
        
        delta_t = self.dt_diff_sec(dt_start, dt_end)
        
        num_steps = int(delta_t/step_size)
        
        dt_end_corrected = dt_start + datetime.timedelta(seconds=num_steps*step_size)
        
        date_str_start = self.dt2str(dt_start)
        date_str_end = self.dt2str(dt_end_corrected)
        
        t_range = pd.date_range(date_str_start, date_str_end, num_steps+1)
        event_times = [pd.to_datetime(t) for t in t_range]
        return event_times    
        

    def dt_diff_sec(self, dt_start, dt_end):
        return (dt_end - dt_start).total_seconds()

    def get_local_time_str():
        local_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(0))).astimezone()
        local_time_str = local_time.strftime('%Y-%m-%dT%H:%M:%S%z')
        return local_time_str
    
    def get_now_local(self):
        return datetime.datetime.now(datetime.timezone(datetime.timedelta(0))).astimezone()
   
    def get_now_local_delay(self, delay):
        return self.get_now_local() + datetime.timedelta(seconds=delay)
    
    def dt2str(self, times, accuracy='iso'):
        ret = None
        if type(times) is list:
            ret =[self.__dt2str(dt, accuracy=accuracy) for dt in times]
        else:
            ret = self.__dt2str(times, accuracy=accuracy)
        assert(ret is not None)
        return ret
    
    def __dt2str(self, dt, accuracy='iso'):
               
        if accuracy == 'sec':
            time_str = dt.strftime('%Y-%m-%dT%H:%M:%S%z')
        elif accuracy == 'min':
            time_str = dt.strftime('%Y-%m-%dT%H:%M:00%z')
        elif accuracy == 'hour':
            time_str = dt.strftime('%Y-%m-%dT%H:00:00%z')
        elif accuracy == 'day':
            time_str = dt.strftime('%Y-%m-%dT00:00:00%z')
        elif accuracy == 'iso':
            time_str = dt.isoformat()
        else:
            raise(ValueError('The keyword {key} does not exist'.format(key=accuracy)))
        
        return time_str
    
    def str2dt(self, date_string):
        timezone = tz.tzlocal()
        dt = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
        dt = dt.replace(tzinfo=timezone)
        return dt
        
    def dt2dtoffset(self, date_string, accuracy='iso'):
        dt = self.str2dt(date_string)
        return self.dt2str(dt, accuracy=accuracy)
    
    def instant_times(self, offset, duration, num_points, accuracy='min'):
        now = get_now_local()
        time_start = now + datetime.timedelta(seconds=offset)
        time_end = time_start + datetime.timedelta(seconds=duration)
        
        time_start_str = get_time_str(time_start, accuracy=accuracy)
        time_end_str = get_time_str(time_end, accuracy=accuracy)
        
        t_range = pd.date_range(time_start_str, time_end_str, num_points)
        event_times = [pd.to_datetime(t) for t in t_range]
        return event_time
    
    def assemble_plan(self,event_times, values, operation):
        schedule = {
        "value": values,
        "startTime": event_times,
        "operation": operation,
        }
        schedule_df = pd.DataFrame(schedule)
        schedule_df.set_index("startTime", inplace=True)
        return schedule_df
    
    # create_std_plan
    # Description: 
    def create_std_plan(self, event_times, values):
        event_times_off = event_times + [event_times[-1] + datetime.timedelta(seconds=3*60)]
        #event_times_off_str = self.dt2str(event_times_off, accuracy='sec') 
        values_off = values + [values[-1]]
        operation = (len(values))*["NORMAL"] + ["OFF"]
        #event_times_off = event_times
        #values_off = values
        #operation = (len(values))*["NORMAL"]
        return self.assemble_plan(event_times_off, values_off, operation)
    
    def add_delta_to_time_string(self, date_string, seconds):
        dt = self.str2dt(date_string)
        dt_end = dt + datetime.timedelta(seconds=seconds)
        return self.dt2str(dt_end)
    
    def str_remove_tz(self, date_string):
        if ('+' in date_string):
            res = date_string.split('+')
        elif ('-' in date_string):
            res = date_string.split('-')
        return res[0]
        