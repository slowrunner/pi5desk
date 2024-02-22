#!/usr/bin/env python3

# Alan's Hello World for Oak-D-Lite sensor

"""
PURPOSE: Demonstrates basic program flow for using the Oak-D-Lite sensor
         with and without image transfer

BACKGROUND:  Everyone likes to visualize what a sensor is seeing and interpreting
             but in fact a robot can usually do without the images.

             This program will show how to extract essential meta-data results
             for input to a robot control algorithm such as a "Follow Me Behavior"

ANALYSIS:
  - Displaying the result window with OpenCV on RaspberryPi 5
    - Processor Load: 5min ave 0.87 = 22%    Temp: 66degC  (no throttling)
    - Average FPS: 29.9
    - Average Detections: 29.9 collections per second

  - Transferring but not Displaying the result on RaspberryPi 5
    - Processor Load: 5min ave 0.72 = 18%    Temp: 66degC  (no throttling)
    - Average FPS: 29.9
    - Average Detections: 29.9 collections per second

  - Displaying the result window with OpenCV on RaspberryPi 3B+
    - Processor Load average: 2.3 to 3.0  Temp: 65degC  (soft temp limit, no throttling)
    - Average FPS: 29.9
    - Average Detections: 29.9 collections per second

  - Transferring the image and result but not displaying the image
    - Processor Load 0.8 Temp: 54degC
    - Average FPS: 29.9
    - Average Detections: 29.9 collections per second

Ref: https://docs.luxonis.com/projects/api/en/latest/tutorials/hello_world/

"""

import numpy as np   # used to manipulate the data returned by depthai 
import cv2           # opencv is used to manipulate video stream
import depthai       # control and access the Oak-D-Lite cameras, processes, and results
import blobconverter # compile and download MyriadX neural network blobs
import time

# Define Constants
BBOX_COLOR_RED = (255, 0, 0)
BBOX_LINE_WIDTH = 2  # pixels


# Define a pipeline

pipeline = depthai.Pipeline()

# Add a ColorCamera node and specify the preview output size
# (300x300 to match mobilnet-ssd input size)

cam_rgb = pipeline.create(depthai.node.ColorCamera)
cam_rgb.setPreviewSize(300, 300)
cam_rgb.setInterleaved(False)

# Define a MobileNetDetectionNetwork node

detection_nn = pipeline.create(depthai.node.MobileNetDetectionNetwork)

# Set path of the NN model blob that will be converted and downloaded
# detection_nn.setBlobPath("/path/to/model.blob")

detection_nn.setBlobPath(blobconverter.from_zoo(name='mobilenet-ssd', shaves=6))
detection_nn.setConfidenceThreshold(0.5)

# Connecct the color camera preview output to the neural network input

cam_rgb.preview.link(detection_nn.input)

# Define two XLinkOut nodes to move image and result data from the sensor to the host/this program

xout_rgb = pipeline.create(depthai.node.XLinkOut)
xout_rgb.setStreamName("rgb")
cam_rgb.preview.link(xout_rgb.input)

xout_nn = pipeline.create(depthai.node.XLinkOut)
xout_nn.setStreamName("nn")
detection_nn.out.link(xout_nn.input)

# Initialize the Oak-D-Lite device and start it

# For USB3 transfers
with depthai.Device(pipeline) as device:

# For USB2 transfers
# with depthai.Device(pipeline, usb2Mode=True) as device:

    # === Define Host Side Queues to receive the sensor streams

    q_rgb = device.getOutputQueue("rgb")
    q_nn  = device.getOutputQueue("nn")

    # Define variables to hold one frame and the results for that frame

    frame = None
    detections = []

    # Define frameNorm helper
    # neural net bounding box results will be float {0..1} of frame width or height
    # (if image has 300px width and nn returns x_min of 0.2 the coordiate is 0.2x300 or 60px)

    def frameNorm(frame, bbox):
        normVals = np.full(len(bbox), frame.shape[0])
        normVals[::2] = frame.shape[1]
        return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)

    # Totals for average FPS
    total_time = 0
    total_frames = 0
    total_detections = 0

    # record start time
    start = time.time()

    # Main host-side Loop
    while True:

        # Fetch latest result from nn and camera nodes
        in_rgb = q_rgb.tryGet()
        in_nn  = q_nn.tryGet()

        # if got an image frame, transform it into an OpenCV frame
        if in_rgb is not None:
            frame = in_rgb.getCvFrame()
            total_frames += 1

        # if got neural net result(s) for this frame take out of the queue
        if in_nn is not None:
            detections = in_nn.detections
            total_detections += 1



        # Display frame results on frame
        # For no display case uncomment next line
        # frame = None

        if frame is not None:
            for detection in detections:
                bbox = frameNorm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), BBOX_COLOR_RED, BBOX_LINE_WIDTH)
            cv2.imshow("preview", frame)


        # Terminate if user presses 'q' key
        if cv2.waitKey(1) == ord('q'):
            break

        # limit spin to 30fps
        # time.sleep(0.03333)

        # Terminate after 5 minutes
        if (time.time()-start) > 300:
            break

    # record time when done
    done = time.time()
    total_time = done - start

    ave_fps = total_frames / total_time
    ave_detections = total_detections / total_time
    print("time: {:<5.1f} detections: {} ave detections: {:<5.1f} per sec,   ave fps: {:<5.1f}".format(total_time, total_detections, ave_detections, ave_fps))

