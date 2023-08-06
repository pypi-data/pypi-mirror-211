import time
import random
from typing import Tuple


def get_time_string(time_obj):
    sec_decimal = str(time_obj).split(".")[1]
    time_info = time.localtime(time_obj)
    return (
        f"{time_info.tm_hour:02d}:"
        f"{time_info.tm_min:02d}:"
        f"{time_info.tm_sec}.{sec_decimal}"
    )


def calculate_fps(start_time, fps_avg_frame_count) -> Tuple[str, str]:
    fps = 15.0 + random.uniform(0.0, 1.5)
    end_time = 1 / fps + start_time
    return get_time_string(start_time), get_time_string(end_time)
