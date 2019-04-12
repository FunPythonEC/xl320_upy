from xl320 import *
import time
dxl=xl320(baudrate=1000000, serialid=0)
dxl.set_control_mode(1,1)
while True:
    dxl.goal_speed(1,500)
    time.sleep(3)
    dxl.goal_speed(1,1500)
    time.sleep(3)
