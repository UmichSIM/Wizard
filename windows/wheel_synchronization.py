# Hid programs will not work on WSL Ubuntu as WSL
# does not let programs access hid devices.
import hid
import pygame

# Good Information about forces
# http://wiibrew.org/wiki/Logitech_USB_steering_wheel

# This is the explaniation for all the write commands
# https://opensource.logitech.com/wiki/Technical_Information/

# Other places referenced
# https://github.com/libusb/hidapi
# https://github.com/apmorton/pyhidapi
# https://github.com/nightmode/logitech-g29

"""
Force Slot Usage: 
Slot 1: Constant Force
Slot 2: Friction Force
Slot 3: Spring Force (used in forceFollow)
Slot 4: Unused
"""

def initWheel(device):
    """
    device : hid.Device
        Which device to init.
    
    This function is supposed to initialize the wheel.
    It may not be necessary, as the program works fine
    without it.
    """
    barr = bytearray([0x00, 0xf8, 0x0a, 0x00, 0x00, 0x00, 0x00, 0x00])
    device.write(bytes(barr))
    barr = bytearray([0x00, 0xf8, 0x09, 0x05, 0x01, 0x01, 0x00, 0x00])
    device.write(bytes(barr))

def setRange(device, range = 900):
    """
    device : hid.Device
        Which device to set range.
    range : int
        270 <= range <= 900, sets
        range of the wheel
    """
    if(range < 270):
        range = 270
    if(range > 900):
        range = 900
    
    range1 = range & 0x00ff
    range2 = (range & 0xff00) >> 8
    device.write(bytes(bytearray([0x00, 0xf8, 0x81, range1, range2, 0x00, 0x00, 0x00])))

def autoCenter(device, center):
    """
    device : hid.Device
        Which device to set range.
    center: bool
        Set true to turn on autocenter.
    """
    if(center):
        device.write(bytes(bytearray([0x00, 0x14, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])))
        device.write(bytes(bytearray([0x00, 0xfe, 0x0d, 0x07, 0x07, 0xff, 0x00, 0x00, 0x00])))
    else:
        device.write(bytes(bytearray([0x00, 0xf5, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])))

def forceOff(device, slot = 0):
    """
    device : hid.Device
        Which device to modify force.
    slot : 1 byte hex
        Each bit of the hex refers to
        which force slot (1-4) to modify.
    
    Turns off the forces playing on the
    specified slot, or muliple slots.
    """

    slot = str(slot)
    if slot == '0':
        slot = 0xf3
    else:
        slot = int('0x'+str(slot)+'3',16)

    device.write(bytes(bytearray([0x00, slot, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])))

def forceConstant(device, force):
    """
    device : hid.Device
        Which device to modify force.
    force : float
        0 <= force <= 1. 0.5 is no
        constant force. force < 0.5
        is left force. force > 0.5
        is right force
    
    Applies a constant force left or right
    """
    if(force == 0.5):
        forceOff(device, 1)
        return

    force = round(abs(force-1)*255)

    #write needs a binary string, not a list
    data = [0x00, 0x11, 0x00, force, 0x00, 0x00, 0x00, 0x00]
    barr = bytearray(data)

    device.write(bytes(barr))

def forceFriction(device, friction = 0):
    # Actually Damper force
    if(friction == 0):
        forceOff(device, 2)
        return
    
    friction = round(friction*7)
    device.write(bytes(bytearray([0x00, 0x21, 0x02, friction, 0x00, friction, 0x00, 0x00])))

def forceFollow(device, center):
    """
    device : hid.Device
        Which device to apply force to.
    center : float
        the result of joystick.axis(0)

    Uses High-Resolution Spring Force
    """
    #print((center+1)/2)
    #print(int((center+1)/2 * 255))

    d1 = int(round((center+1)/2 * 255))
    if(d1 < 0):
        d1 = 0
    d2 = int(round((center+1)/2 * 255))
    if(d2 > 255):
        d2 = 255

    #print(d1)
    #print(d2)
        
    s = 0x00

    device.write(bytes(bytearray([0x00, 0x41, 0x0b, d1, d2, 0x99, s, 0xff])))

if __name__ == "__main__":
    #find device
    vid = 0x046d	# Vendor ID is Logitech
    pid = 0xc24f	# Product ID for G29

    # enumerate looks through all hid devices for those that match parameters
    devices = hid.enumerate(vid,pid)

    #look for devices with usage_page == 1 or interface_number == 0
    devices = list(filter(lambda device: device['interface_number'] == 0 
                          and device['usage_page'] == 1, devices))

    wheelOne = hid.Device(None, None, None, devices[0]['path'])
    wheelTwo = hid.Device(None, None, None, devices[1]['path'])

    #initWheel(wheelOne)
    #initWheel(wheelTwo)
    
    pygame.init()
    pygame.joystick.init()
    pygame.joystick.Joystick(0).init()
    joy2 = pygame.joystick.Joystick(0)
    pygame.joystick.Joystick(1).init()
    joy1 = pygame.joystick.Joystick(1)
    
    autoCenter(wheelOne, False)
    autoCenter(wheelTwo, False)

    forceOff(wheelOne)
    forceOff(wheelTwo)
    
    forceFriction(wheelOne, 0.0)
    forceFriction(wheelTwo, 0.0)
    
    state = 0
    while True:
        # autocenter command repeat needed for some reason
        # or else it will automatically turn on again
        # likely because of pygame
        autoCenter(wheelOne, False)
        autoCenter(wheelTwo, False)
        for event in pygame.event.get():
            #print((joy1.get_axis(0)+1)*127.5)
            #print(joy2.get_axis(0))
            if(joy1.get_button(1)):
                break

            if(state == 0):
                if(joy2.get_button(0)):
                    state = 1
                    forceOff(wheelTwo)
                else:
                    forceFollow(wheelTwo, joy1.get_axis(0))
            else:
                if(joy1.get_button(0)):
                    state = 0
                    forceOff(wheelOne)
                else:
                    forceFollow(wheelOne, joy2.get_axis(0))
        else:
            continue
        break

    wheelOne.close()
    wheelTwo.close()