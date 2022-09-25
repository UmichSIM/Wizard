#!/usr/bin/env python3

from sdl2 import *

if __name__ == "__main__":
    if SDL_Init(SDL_INIT_TIMER | SDL_INIT_VIDEO | SDL_INIT_JOYSTICK
                | SDL_INIT_GAMECONTROLLER | SDL_INIT_HAPTIC) < 0:
        raise RuntimeError("Failed to initialize SDL Interface")
    print(SDL_NumJoysticks())
    js = SDL_JoystickOpen(0)
    haptic = SDL_HapticOpenFromJoystick(js)
