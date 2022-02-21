import depthai as dai

devices = dai.Device.getAllAvailableDevices()

for dev in devices:
    print(f'name: {dev.desc.name}, ({dev.getMxId()}) state: {dev.state}')