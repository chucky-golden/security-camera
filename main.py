import cv2
import time
import datetime


cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

detection = False
detection_stopped_time = None
time_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5

#prepare variables to be able to generate and save videos
frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")


while True:
    _, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = body_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) + len(bodies) > 0:
        if detection:
            time_started = False
        else:
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 20.0, frame_size)
            print("started recording")
    elif detection:
        if time_started:
            if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                time_started = False
                out.release()
                print("stop recording")
        else:
            time_started = True
            detection_stopped_time = time.time()
    if detection:
        out.write(frame)

    # for (x, y, width, height) in faces:
    #     cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)


    #you can comment this cv2.imshow out to hide the frame, and make it more legit
    #cv2.imshow("Camera", frame)

    if cv2.waitKey(1) == ord('q'):
        break


out.release()
cap.release()
cv2.destroyAllWindows()