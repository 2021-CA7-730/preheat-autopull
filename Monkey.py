# Monkey patch load data method to fix the "raw" time res bug
import preheat_open as ph
from typing import List, Union
from preheat_open.data import load_model_data
import datetime
import pandas as pd
import TimeKeeper


def load_data(
    self,
    start_date,
    end_date,
    time_resolution: str = "minute",
    components: Union[List, None] = None,
    **kwargs,
) -> None:
    self._warn_if_data_is_loaded()
    self.data = load_model_data(
        self.get_all_component_ids(components=components),
        start_date,
        end_date,
        time_resolution,
    )
    if "raw" != time_resolution:
        self._ensure_continuity_of_data(time_resolution)


def patch_Unit_load_data():
    ph.Unit.load_data = load_data
    print("Monkey patched preheat_open.Unit.load_data()")


def create_schedule(self, time_start, time_end, step_size):
    delta_t = self.dt_diff_sec(time_start, time_end)
    num_steps = int(delta_t/step_size)
    dt_end_corrected = time_start + \
        datetime.timedelta(seconds=num_steps*step_size)
    date_str_start = self.dt2str(time_start)
    date_str_end = self.dt2str(dt_end_corrected)
    t_range = pd.date_range(date_str_start, date_str_end, num_steps+1)
    event_times = [pd.to_datetime(t) for t in t_range]
    return event_times


def patch_TimeKeeer_create_schedule():
    TimeKeeper.create_schedule = create_schedule
    print("Monkey patched TimeKeeper.create_schedule()")
