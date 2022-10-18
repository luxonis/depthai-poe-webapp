#!/usr/bin/env python3

import depthai as dai
import time
from string import Template
from pathlib import Path
import os
import sys
import argparse

SCRIPT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
dist_path = SCRIPT_DIRECTORY + '/../dist'

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("--flash", help="Flash the webapp to a discovered PoE device", action="store_true")
parser.add_argument("--save", help="Specify the path where to save the created DepthAI Application Package")
parser.add_argument("--compress", help="Specify whether compress and reduce the size of the DepthAI Application Package", action="store_true")
args = parser.parse_args()

# Check if flash mode
mode = None
if args.flash is True:
    mode = 'flash'
if args.save is not None:
    mode = 'save'

# Specify port number
port_number = 8080
if mode != None:
    port_number = 80

# Read the template
with open(SCRIPT_DIRECTORY + '/' + 'python_device_server.py', 'r') as file:
    template = str(file.read())
    code = str(template)

# Perform the substitution
code = template.replace("_PORT_NUMBER", str(port_number))

# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - color camera
cam = pipeline.create(dai.node.ColorCamera)
camLeft = pipeline.create(dai.node.MonoCamera)
camRight = pipeline.create(dai.node.MonoCamera)
# VideoEncoder
jpeg = pipeline.create(dai.node.VideoEncoder)
jpeg.setDefaultProfilePreset(cam.getFps(), dai.VideoEncoderProperties.Profile.MJPEG)
jpeg.setQuality(50)
jpegLeft = pipeline.create(dai.node.VideoEncoder)
jpegLeft.setDefaultProfilePreset(camLeft.getFps(), dai.VideoEncoderProperties.Profile.MJPEG)
jpegLeft.setQuality(50)
jpegRight = pipeline.create(dai.node.VideoEncoder)
jpegRight.setDefaultProfilePreset(camRight.getFps(), dai.VideoEncoderProperties.Profile.MJPEG)
jpegRight.setQuality(50)

# Add SystemLogger node
sys = pipeline.create(dai.node.SystemLogger)

# Script node
script = pipeline.create(dai.node.Script)
script.setProcessor(dai.ProcessorType.LEON_CSS)
script.setScript(code)

# Connections
cam.video.link(jpeg.input)
camLeft.out.link(jpegLeft.input)
camRight.out.link(jpegRight.input)
jpeg.bitstream.link(script.inputs['color'])
jpegLeft.bitstream.link(script.inputs['left'])
jpegRight.bitstream.link(script.inputs['right'])
script.inputs['color'].setQueueSize(1)
script.inputs['left'].setQueueSize(1)
script.inputs['right'].setQueueSize(1)
script.inputs['color'].setBlocking(False)
script.inputs['left'].setBlocking(False)
script.inputs['right'].setBlocking(False)
script.inputs['sys'].setQueueSize(1)
script.inputs['sys'].setBlocking(False)
sys.out.link(script.inputs['sys'])

# Load dist folder to Assets
glob = list(Path(dist_path).glob('**/*'))
for file in glob:
    if file.is_file():
        relative_file = os.path.relpath(file, dist_path)
        key = relative_file
        # script.getAssetManager().set(key, str(file))
        pipeline.getAssetManager().set(key, str(file))
        print(f'Loaded: {key} @ {file}')

# Search for first available PoE device
devices = dai.Device.getAllAvailableDevices()
device_info = None
for dev_info in devices:
    if dev_info.protocol == dai.X_LINK_TCP_IP:
        device_info = dev_info

# Connect to a PoE device with pipeline
if device_info is not None or mode == 'save':
    # Ask if for confirmation if flash mode
    if mode == 'flash':
        print(f"Are you sure you want to flash device '{device_info.getMxId()}' (compress: {args.compress})")
        print(f"Type 'y' and press enter to proceed, otherwise exits: ")
        if input() != 'y':
            print("Prompt declined, exiting...")
            exit(-1)
        with dai.DeviceBootloader(device_info) as bl:
            # Create a progress callback lambda
            progress = lambda p : print(f'Flashing progress: {p*100:.1f}%')
            (success, msg) = bl.flash(progress, pipeline, args.compress, 'depthai-poe-webapp-v0.1')
            print(f'Success: {success}, message: {msg}')
    elif mode == 'save':
        dai.DeviceBootloader.saveDepthaiApplicationPackage(args.save, pipeline, args.compress, 'depthai-poe-webapp-v0.1')
        print(f'Saved DepthAI Application Package to: {args.save}')
    else:
        print(f"Connecting to device '{device_info.getMxId()}'")
        with dai.Device(pipeline, device_info) as device:
            device.setLogLevel(dai.LogLevel.INFO)
            device.setLogOutputLevel(dai.LogLevel.INFO)
            device.setSystemInformationLoggingRate(0.0)
            while not device.isClosed():
                time.sleep(1)
else:
    print('No devices found')
