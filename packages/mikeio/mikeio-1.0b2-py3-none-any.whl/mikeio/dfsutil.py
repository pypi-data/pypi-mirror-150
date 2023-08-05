from typing import Iterable, List, Union
import numpy as np
import pandas as pd
from .eum import EUMType, EUMUnit, ItemInfo, TimeAxisType
from .custom_exceptions import ItemsError

from mikecore.DfsFile import DfsDynamicItemInfo, DfsFileInfo


def _valid_item_numbers(
    dfsItemInfo: List[DfsDynamicItemInfo],
    items: Union[int, List[int], List[str]] = None,
    ignore_first: bool = False,
) -> Iterable[int]:
    start_idx = 1 if ignore_first else 0
    n_items_file = len(dfsItemInfo) - start_idx
    if items is None:
        return list(range(n_items_file))

    if np.isscalar(items):
        items = [items]

    for idx, item in enumerate(items):
        if isinstance(item, str):
            items[idx] = _item_numbers_by_name(dfsItemInfo, [item], ignore_first)[0]
        elif isinstance(item, int):
            if (item < 0) or (item >= n_items_file):
                raise ItemsError(n_items_file)
        else:
            raise ItemsError(n_items_file)

    if len(np.unique(items)) != len(items):
        raise ValueError("'items' must be unique")

    assert isinstance(items, Iterable)
    assert isinstance(items[0], int)

    return items


def _valid_timesteps(dfsFileInfo: DfsFileInfo, time_steps):
    # TODO: naming: time_steps or timesteps?
    n_steps_file = dfsFileInfo.TimeAxis.NumberOfTimeSteps

    if time_steps is None:
        return list(range(n_steps_file))

    if isinstance(time_steps, int):
        time_steps = [time_steps]

    if isinstance(time_steps, str):
        parts = time_steps.split(",")
        if len(parts) == 1:
            parts.append(parts[0])  # end=start

        if parts[0] == "":
            time_steps = slice(parts[1])  # stop only
        elif parts[1] == "":
            time_steps = slice(parts[0], None)  # start only
        else:
            time_steps = slice(parts[0], parts[1])

    if isinstance(time_steps, slice):
        if dfsFileInfo.TimeAxis.TimeAxisType != TimeAxisType.EquidistantCalendar:
            # TODO: handle non-equidistant calendar
            raise ValueError(
                "Only equidistant calendar files are supported for this type of time_step argument"
            )
        start_time_file = dfsFileInfo.TimeAxis.StartDateTime
        time_step_file = dfsFileInfo.TimeAxis.TimeStep

        freq = pd.tseries.offsets.DateOffset(seconds=time_step_file)
        time = pd.date_range(start_time_file, periods=n_steps_file, freq=freq)
        if time_steps.start is None:
            time_steps_start = time[0]
        else:
            time_steps_start = pd.Timestamp(time_steps.start)
        if time_steps.stop is None:
            time_steps_stop = time[-1]
        else:
            time_steps_stop = pd.Timestamp(time_steps.stop)

        s = time.slice_indexer(time_steps_start, time_steps_stop)
        time_steps = list(range(s.start, s.stop))
    elif isinstance(time_steps[0], int):
        time_steps = np.array(time_steps)
        time_steps[time_steps < 0] = n_steps_file + time_steps[time_steps < 0]
        time_steps = list(time_steps)

        if max(time_steps) > (n_steps_file - 1):
            raise IndexError(f"Timestep cannot be larger than {n_steps_file}")
        if min(time_steps) < 0:
            raise IndexError(f"Timestep cannot be less than {-n_steps_file}")

    return time_steps


def _item_numbers_by_name(dfsItemInfo, item_names, ignore_first=False):
    """Utility function to find item numbers

    Parameters
    ----------
    dfsItemInfo : MIKE dfs ItemInfo object

    item_names : list[str]
        Names of items to be found

    Returns
    -------
    list[int]
        item numbers (0-based)

    Raises
    ------
    KeyError
        In case item is not found in the dfs file
    """
    first_idx = 1 if ignore_first else 0
    names = [x.Name for x in dfsItemInfo[first_idx:]]

    item_lookup = {name: i for i, name in enumerate(names)}
    try:
        item_numbers = [item_lookup[x] for x in item_names]
    except KeyError:
        raise KeyError(f"Selected item name not found. Valid names are {names}")

    return item_numbers


def _get_item_info(
    dfsItemInfo: List[DfsDynamicItemInfo],
    item_numbers: List[int] = None,
    ignore_first: bool = False,
) -> List[ItemInfo]:
    """Read DFS ItemInfo for specific item numbers

    Parameters
    ----------
    dfsItemInfo : List[DfsDynamicItemInfo]
    item_numbers : list[int], optional

    Returns
    -------
    list[ItemInfo]
    """
    first_idx = 1 if ignore_first else 0
    if item_numbers is None:
        item_numbers = list(range(len(dfsItemInfo) - first_idx))

    items = []
    for item in item_numbers:
        item = item + first_idx
        name = dfsItemInfo[item].Name
        eumItem = dfsItemInfo[item].Quantity.Item
        eumUnit = dfsItemInfo[item].Quantity.Unit
        itemtype = EUMType(eumItem)
        unit = EUMUnit(eumUnit)
        data_value_type = dfsItemInfo[item].ValueType
        item = ItemInfo(name, itemtype, unit, data_value_type)
        items.append(item)
    return items
