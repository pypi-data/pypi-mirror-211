from datetime import datetime
import inspect
import time
import os


def log(input_str, ident=None):
    dt_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if ident:
        print(f"[{dt_str}] {ident} {input_str}")
    else:
        print(f"[{dt_str}] {input_str}")

def get_current_file():
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    filename = module.__file__
    log_name = os.path.basename(filename)
    return log_name
