#!/usr/bin/env python
import evdev
import asyncio
from evdev import ecodes, InputDevice, ff
import config
from linux.drivers.BaseWheel import BaseWheel

class G920(BaseWheel):
    def __init__(self,ev_name):
        self.ev_name = ev_name
        # register events
        self.ev_key_event  = {
            288:self.__key_a_handler,
            289:self.__key_b_handler,
            290:self.__key_x_handler,
            291:self.__key_y_handler,
            292:self.__key_rshift_handler,
            293:self.__key_lshift_handler,
            294:self.__key_menu_handler,
            295:self.__key_view_handler,
            296:self.__key_rsb_handler,
            297:self.__key_lsb_handler,
            298:self.__key_xbox_handler,
        }
        self.ev_abs_event  = {
            0: self.__abs__steer_handler,
            1: self.__abs_acc_handler,
            2: self.__abs_brake_handler,
            5: self.__abs_clutch_handler,
            16: self.__abs_pad_handler,
            17: self.__abs_pad_handler,
        }
        # TODO: Change connection type
        self.ev:evdev.InputDevice = InputDevice(evdev.list_devices()[0])
        self.__init()


    def __key_xbox_handler(self,event):
        pass


    def __key_lsb_handler(self,event):
        pass


    def __key_rsb_handler(self,event):
        pass


    def __key_view_handler(self,event):
        pass


    def __key_menu_handler(self,event):
        pass


    def __key_a_handler(self,event):
        pass


    def __key_b_handler(self,event):
        pass


    def __key_x_handler(self,event):
        pass


    def __key_y_handler(self,event):
        pass


    def __key_lshift_handler(self,event):
        """
        handler for left paddle shift on G920
        """
        pass


    def __key_rshift_handler(self,event):
        """
        handler for right paddle shift on G920
        """
        pass


    def __abs__steer_handler(self,event):
        """
        handler for the steering wheel input on G920
        """
        pass


    def __abs_acc_handler(self,event):
        """
        handler for the accelerator input
        """
        pass


    def __abs_brake_handler(self,event):
        """
        handler for the brake input
        """
        pass


    def __abs_clutch_handler(self,event):
        """
        handler for the clutch input
        """
        pass


    def __abs_pad_handler(self,event):
        """
        handler for the directional pad
        c:16 val:-1 -> left
        c:16 val:1 -> right
        c:17 val:-1 -> up
        c:17 val:1 -> down
        """
        pass



if __name__ == "__main__":
    rw = G920(config.wheel1_name)
    asyncio.ensure_future(rw.events_handler())
    loop = asyncio.get_event_loop()
    loop.run_forever()
