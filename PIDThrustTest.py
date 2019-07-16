from DroneController import droneCont
import time
drone = droneCont("10.0.0.32")
drone.moveRaw(1500,1500,1500,900)
drone.arming()
time.sleep(5)
drone.moveRaw(1500,1500,1500,1200)
time.sleep(1)
drone.disarm()
