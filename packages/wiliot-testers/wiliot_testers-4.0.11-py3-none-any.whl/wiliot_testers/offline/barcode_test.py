from time import time, sleep, perf_counter_ns
import sys
import glob
import serial
import traceback
import os
from datetime import datetime
from wiliot_testers.test_equipment import BarcodeScanner
global scan_timeout


scan_time = 500

scanner = BarcodeScanner(write_to_log=True, timeout=str(scan_time))

t_i = datetime.now()
dt = 0
while dt < 60:
    sleep(0.1)
    results = scanner.scan_ext_id()
    print(results)
    dt = (datetime.now() - t_i).total_seconds()
scanner.close_port()


