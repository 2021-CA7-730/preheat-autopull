# Monkey patch load data method to fix the "raw" time res bug
import preheat_open as ph
from typing import List, Union
from preheat_open.data import load_model_data


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


ph.Unit.load_data = load_data

print("Monkey patched preheat_open.Unit.load_data()")
