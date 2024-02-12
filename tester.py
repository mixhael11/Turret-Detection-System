import threading

import cv2
import serial, time
import numpy as np

arduino = serial.Serial('com4', 9600, timeout=0.1)

time.sleep(1)

# Load YOLO
net = cv2.dnn.readNet("A:\opencvpython\yolov3.weights", "A:\opencvpython\yolov3.cfg")
cap = cv2.VideoCapture(0)
cv2.CAP_PROP_BUFFERSIZE
classes = []
with open("A:\opencvpython\coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Assuming 'cap' is the virtual camera feed initialized elsewhere in your code
cv2.namedWindow('OBS Output', cv2.WINDOW_NORMAL)

while True:
    # Read a frame from the virtual camera feed
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame from the virtual camera feed.")
        break

    # Get the height and width of the frame
    height, width, _ = frame.shape

    # Convert the frame to a blob for the YOLO model
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    # Set the input for the YOLO network
    net.setInput(blob)

    # Get the output layer names
    output_layer_names = net.getUnconnectedOutLayersNames()

    # Run forward pass to get the output from the output layer
    outputs = net.forward(output_layer_names)

    # Loop through the outputs
    frame_width = 320
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 2:  # Class ID 2 corresponds to cars in COCO dataset
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                if 0 < x < 220:
                    arduino.write("go clockwise".encode('utf-8'))
                if 220 < x < 285:
                    arduino.write("stop".encode('utf-8'))
                if 285 < x < 1000:
                    arduino.write("go counter".encode('utf-8'))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Display the frame with detected cars
    cv2.imshow('OBS Output', frame)

    # Check for keyboard input
    key = cv2.waitKey(1) & 0xFF

    # Perform actions based on the key pressed
    if key == ord('q'):
        print("Exiting the loop.")
        break
    elif key == ord('s'):
        print("Save the frame or perform some action.")

# Release the virtual camera feed and close the OpenCV window
cap.release()
cv2.destroyAllWindows()