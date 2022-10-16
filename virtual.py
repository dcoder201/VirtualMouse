#  import required modules
import cv2
import mediapipe as mp


import pyautogui

# capture video
capture = cv2.VideoCapture(0)
# calling hand detection method from mediapipe
detect_hand = mp.solutions.hands.Hands()
# for detecting landmarks on hand
draw_marks = mp.solutions.drawing_utils

y_index = 0
while True:
    #  getting each frames from captured video
    _, frame = capture.read()
    # frame flipping to get exact user side
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape
    screen_width, screen_height = pyautogui.size()
    # converting bgr to rgb for processing
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # passing converted rgb frame for hand landmark detection
    processed = detect_hand.process(rgb)
    # processing landmarks
    out = processed.multi_hand_landmarks
    # if output value is not none or if hand is detected in frame
    if out:
        # traverse through the coordinates
        for output in out:
            #  landmark coordinate values in the output frame
            draw_marks.draw_landmarks(frame, output)
            marks = output.landmark
            # traversing through ids and marks
            for num, mark in enumerate(marks):
                # marking x and y axis
                x_axis = int(mark.x*width)
                y_axis = int(mark.y*height)
                # detecting top point of index finger using id value
                if num == 8:
                    # circling around the point
                    cv2.circle(img=frame, center=(x_axis, y_axis), radius=20, color=(255, 0, 255))
                    # finding x-axis difference value from original screen size to output screen
                    x_index = screen_width/width*x_axis
                    # finding y-axis difference value from original screen size to output screen
                    y_index = screen_height/height*y_axis
                    # moving mouse pointer to the index point
                    pyautogui.moveTo(x_index, y_index)
                if num == 4:
                    # circling around the point
                    cv2.circle(img=frame, center=(x_axis, y_axis), radius=20, color=(0, 255, 255))
                    thumb_x = screen_width/width*x_axis
                    thumb_y = screen_height/height*y_axis
                    #  if index finger come closer or difference less than 50 click option is enabled
                    if(abs(thumb_y-y_index))<50:
                        pyautogui.click()
                        pyautogui.sleep(1)

    # showing frame to user
    cv2.imshow('Mouse', frame)
    cv2.waitKey(1)



