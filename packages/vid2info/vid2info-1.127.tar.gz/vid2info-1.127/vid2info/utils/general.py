from __future__ import annotations
from time import strftime, gmtime, localtime

import numpy as np

from vid2info.inference.utils import crop_bbox_from_image
from vid2info.utils.config import TIME_FORMAT


def time_as_str(time_as_seconds: float | None = None, time_format: str = TIME_FORMAT, as_locale : bool = True):
    """
    Take the time as seconds, as given by time.time(), and return it formatted as a string.

    :param time_as_seconds: float or None. The time in seconds as provided by time.time().
                If None, the current time is used.
    :param time_format: str. The format of the time. See strftime for more information. Default is "%H:%M:%S".
    :param as_locale: bool. If True, the time is given as locale-dependent string. If False, the time is given in UTC

    :return str. The formatted time.
    """
    get_time = localtime if as_locale else gmtime
    return strftime(time_format, get_time(time_as_seconds))

def iou(bbox1: tuple | list | np.ndarray, bbox2: tuple | list | np.ndarray) -> float:
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes. Bboxes are expected to be in the format (x1, y1, x2, y2).
    :param bbox1: tuple | list | np.ndarray. The first bounding box. Format (x1, y1, x2, y2).
    :param bbox2: tuple | list | np.ndarray. The second bounding box. Format (x1, y1, x2, y2).

    :return: float. The intersection over union of the two bounding boxes.
    """

    assert len(bbox1) == 4, f"The bounding box must be a list or tuple of length 4. Got {len(bbox1)}."
    assert len(bbox2) == 4, f"The bounding box must be a list or tuple of length 4. Got {len(bbox2)}."

    x1, y1, x2, y2 = bbox1
    x3, y3, x4, y4 = bbox2
    i_w = min(x2, x4) - max(x1, x3)
    i_h = min(y2, y4) - max(y1, y3)
    if (i_w <= 0 or i_h <= 0):
        return 0

    i_s = i_w * i_h
    s_1 = (x2 - x1) * (y2 - y1)
    s_2 = (x4 - x3) * (y4 - y3)
    return float(i_s) / (s_1 + s_2 - i_s)

