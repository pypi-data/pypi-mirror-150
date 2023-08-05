import time
from datetime import datetime
from robertcommonbasic.basic.cls.utils import function_thread

def test1(p1, p2):
    count = 10
    while count > 0:
        print(f"{datetime.now()} {p1} {p2}")
        time.sleep(1)
        count = count - 1

def test_function_thread():
    function_thread(test1, 2, 3, p1='1', p2='2').start()

test_function_thread()