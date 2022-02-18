import ctypes

# Change Path to dll
logidll = ctypes.cdll.LoadLibrary("E:/CARLA/carla/PythonAPI/examples/LogitechSteeringWheelSDK_8.75.30/Lib/GameEnginesWrapper/x64/LogitechSteeringWheelEnginesWrapper.dll")
springSuccess = logidll.LogiIsConnected(0)

def main():
    print(springSuccess)

if __name__ == '__main__':
    main()