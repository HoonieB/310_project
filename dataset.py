import cv2
import mediapipe as mp
import csv
import os

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

#create the file that will hold the dataset if it doesn't exist yet
csv_file = 'dataset2.csv'
if not os.path.exists(csv_file):
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)

        header = ["label"]
        for i in range(21):
            header.extend([f"x{i}", f"y{i}", f"z{i}"])
        writer.writerow(header)

#default values
current_label = None
recording_enabled = False

#the loop that starts the recording
capture = cv2.VideoCapture(0)
while True:
    ret, frame = capture.read()
    if not ret:
        continue

    flipped_frame = cv2.flip(frame, 1) #to mirror the camera feed

    rgb_image = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2RGB) #change from OpenCV colour format to RGB

    result = hands.process(rgb_image)

    #if AT LEAST one hand is detected
    if result.multi_hand_landmarks:
        #then take the first hand that has been detected
        first_hand = result.multi_hand_landmarks[0]

        mp_draw.draw_landmarks(flipped_frame, first_hand, mp_hands.HAND_CONNECTIONS)

        #adds the data to the file in a new row
        if recording_enabled and current_label is not None:

            new_row = [current_label]

            for point in first_hand.landmark:
                new_row.extend([point.x, point.y, point.z]) #add coordinates of hand to file

            with open(csv_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(new_row)

            #displays the label on the screen to make it easier to keep track of
            message = "RECORDED: " + current_label
            cv2.putText(flipped_frame, message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)
            recording_enabled = False

    if current_label is not None:
        label_text = "Label: " + current_label
        cv2.putText(flipped_frame, label_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 2)


    cv2.imshow("Gesture Recorder", flipped_frame)

    key = cv2.waitKey(1)
    key = key & 0xFF #to normalize the key code

    #q stops the recording
    if key == ord('q'):
        break
    #r takes the capture
    elif key == ord('r'):
        recording_enabled = True
    #these numbers are for the different gestures
    elif key == ord('1'):
        current_label = 'fist'
    elif key == ord('2'):
        current_label = 'gun'

capture.release()
cv2.destroyAllWindows()
