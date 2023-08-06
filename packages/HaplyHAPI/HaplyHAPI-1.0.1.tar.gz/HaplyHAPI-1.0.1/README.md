# Python Implementation of the hAPI

This is a python port of the [java implementation of the hAPI](https://gitlab.com/Haply/hAPI) .

## Installation

```bash
pip install HaplyHAPI
```

## Usage

Here’s an example of using the hAPI to control a 2diy Haply device. The example is also available in the examples folder.

In this example we will read position of the device and send a constant force.

```
from HaplyHAPI import Board, Device, Mechanisms, Pantograph
import time
import serial.tools.list_ports



CW = 0
CCW = 1

hardware_version = 3 # 2 for the metallic plate device, 3 for the newer plastic device

haplyBoard = Board
device = Device
SimpleActuatorMech = Mechanisms
pantograph = Mechanisms

com_ports = list(serial.tools.list_ports.comports())
# if only one port is available, use that one, otherwise ask the user to select the correct one
if len(com_ports) == 1:
    port = com_ports[0].device
else:
    print("Select the COM port for the Haply board:")
    for i, port in enumerate(com_ports):
        print(str(i) + ": " + port.device)
    port = com_ports[int(input())].device



def main():
    print("Starting the application!")
    haplyBoard = Board("test", port, 0)
    device = Device(5, haplyBoard)
    pantograph = Pantograph(hardware_version)
    device.set_mechanism(pantograph)

    

    #device.add_encoder(1, CCW, 240, 10978, 2)
    #device.add_encoder(2, CCW, -60, 10978, 1)
    if hardware_version == 3:
        device.add_actuator(1, CCW, 2)
        device.add_actuator(2, CCW, 1)
        device.add_encoder(1, CCW, 168, 4880, 2)
        device.add_encoder(2, CCW, 12, 4880, 1)
    else:
        device.add_actuator(1, CCW, 2)
        device.add_actuator(2, CW, 1)
        device.add_encoder(1, CCW, 241, 10752, 2)
        device.add_encoder(2, CW, -61, 10752, 1)

    device.device_set_parameters()
    i=0
    while(True):
        if(haplyBoard.data_available()):
            device.device_read_data()
            motorAngle = device.get_device_angles()
            device_position = device.get_device_position(motorAngle)
            print("Device position: " + str(device_position))
            i+=1
        forces = [0, 10]
        device.set_device_torques(forces)
        device.device_write_torques()
        time.sleep(0.001)



if __name__ == "__main__":
    main()
```



