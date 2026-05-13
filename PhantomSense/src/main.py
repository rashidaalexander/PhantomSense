
import cv2
import time
import numpy as np

print("\n[ PhantomSense ]")
print("Initializing security perimeter...\n")

cap = cv2.VideoCapture(0)

ret, frame1 = cap.read()
ret, frame2 = cap.read()

motion_counter = 0

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)

    contours, _ = cv2.findContours(
        dilated,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )

    motion_detected = False

    for contour in contours:
        if cv2.contourArea(contour) < 1200:
            continue

        motion_detected = True
        x, y, w, h = cv2.boundingRect(contour)

        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0,255,0), 2)

    if motion_detected:
        motion_counter += 1
        risk_score = round(min(99.0, 70 + motion_counter * 2.4), 1)

        print(f"[ ALERT ] Motion detected | Risk Score: {risk_score}")

        cv2.putText(
            frame1,
            "MOTION DETECTED",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

    cv2.imshow("PhantomSense", frame1)

    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(10) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
