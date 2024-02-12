import time
import cv2
import serial

arduino = serial.Serial('com4', baudrate=115200, timeout=0.1)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

car_cascade = cv2.CascadeClassifier("A:\haarcascade_car.xml")

counter_goright = 0
counter_goleft = 0
counter_stop = 0

def send_command(command):
    arduino.write(command.encode('utf-8'))
    time.sleep(0.1)
    print(f"Sent command: {command}")
    return True


while True:
    ret, frame = cap.read()

    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(25, 25))

    frame_width = 320


    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        print("wrote")
        print(x)

        center_area = (190, 320)

        if center_area[0] < x < center_area[1]:
            counter_stop += 1
            counter_goright = 0
            counter_goleft = 0
            if counter_stop >= 15:
                print("wrote stop")
                send_command("stop")
                counter_goright = 0
                counter_stop = 0
                counter_goleft = 0

        elif x >= center_area[0]:
            counter_goright += 1
            counter_stop = 0
            counter_goleft = 0
            if counter_goright >= 15:
                send_command("right")
                counter_goright = 0
                counter_stop = 0
                counter_goleft = 0
        elif x <= center_area[1]:
            counter_goleft += 1
            counter_stop = 0
            counter_goright = 0
            if counter_goleft >= 15:
                send_command("left")
                counter_goright = 0
                counter_stop = 0
                counter_goleft = 0

    # Display the frame
    cv2.imshow('Car Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release the video capture object and close the window
cap.release()
cv2.destroyAllWindows()
