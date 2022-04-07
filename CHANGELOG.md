# TODOS and Changelog

## TODOS

+ [x] figure out why screenshots in _out
+ [x] try to use `poetry` to manage the environments
+ [x] encapsulate a vehicle class
+ [ ] figure out how to change driver without any side effect
  + currently the switch is achieved by modifying `VehiclePhysicalControl`, which will cause vehicle to reinitialize and stop...

## Changelog

+ 22.04.07
  + use the second server to synchronize wheel
+ 22.03.19
  + add function to properly terminate the program
  + add G27 support, the spring force is not supported
+ 22.03.18
  + add spring force that maintain the racing wheel at certain position
  + add wheel follow when the agent is not in control
  + update apis for racing wheels
+ 22.03.16
  + add poetry to manage packages and environments
  + rename linux folder to wizard
+ 22.03.11
  + switch to multi-client
  + TODO: make the control switching smoother
+ 22.02.19
  + Complete most of the changes, wait for testing
+ 22.02.15
  + starting splitting the files
  + create virtual classes for wheel driver
