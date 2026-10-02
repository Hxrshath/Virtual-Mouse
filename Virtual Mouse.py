import math
import time
import cv2
import mediapipe as mp
import numpy as np
import pyautogui

# ----------------------------- Settings (tune these) -----------------------------
CAM_INDEX = 0            # change to 1 if you have an external webcam
CAM_W, CAM_H = 640, 480  # camera resolution
FRAME_MARGIN = 100       # border (pixels) of the camera frame that is "dead"; hand moves inside the box
SMOOTHING = 6            # higher = smoother but slower cursor (try 4 - 9)
CLICK_RATIO = 0.25       # index-middle tip distance / palm size below this = click
SCROLL_RATIO = 0.45      # above this (with two fingers up) = scroll mode
CLICK_COOLDOWN = 0.35    # seconds between clicks
RIGHT_CLICK_COOLDOWN = 0.6
SCROLL_SPEED = 60        # higher = faster scroll
# ----------------------------------------------------------------------------------

pyautogui.FAILSAFE = False   
pyautogui.PAUSE = 0         

SCREEN_W, SCREEN_H = pyautogui.size()

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Landmark ids
WRIST, INDEX_MCP = 0, 5
MIDDLE_MCP = 9
INDEX_TIP, MIDDLE_TIP = 8, 12
FINGER_TIPS = [8, 12, 16, 20]  
FINGER_PIPS = [6, 10, 14, 18]


def fingers_up(lm):
    return [1 if lm[t].y < lm[p].y else 0 for t, p in zip(FINGER_TIPS, FINGER_PIPS)]


def dist(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def main():
    cap = cv2.VideoCapture(CAM_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_H)
    if not cap.isOpened():
        print("Could not open the webcam. Check CAM_INDEX or close other apps using the camera.")
        return

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.6,
    )

    prev_x, prev_y = pyautogui.position()
    last_click = 0.0
    last_right_click = 0.0
    prev_scroll_y = None
    prev_time = time.time()

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        frame = cv2.flip(frame, 1)  
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        cv2.rectangle(frame, (FRAME_MARGIN, FRAME_MARGIN),
                      (w - FRAME_MARGIN, h - FRAME_MARGIN), (255, 0, 255), 2)

        mode = "NO HAND"

        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]
            lm = hand.landmark
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            up = fingers_up(lm)                     
            palm_size = dist(lm[WRIST], lm[MIDDLE_MCP]) or 1e-6
            now = time.time()

            index_only = up == [1, 0, 0, 0]
            two_up = up == [1, 1, 0, 0]
            three_up = up == [1, 1, 1, 0]
            open_palm = up == [1, 1, 1, 1]

            if index_only:
                mode = "MOVE"
                prev_scroll_y = None
                x_px = lm[INDEX_TIP].x * w
                y_px = lm[INDEX_TIP].y * h

                target_x = np.interp(x_px, (FRAME_MARGIN, w - FRAME_MARGIN), (0, SCREEN_W))
                target_y = np.interp(y_px, (FRAME_MARGIN, h - FRAME_MARGIN), (0, SCREEN_H))

                cur_x = prev_x + (target_x - prev_x) / SMOOTHING
                cur_y = prev_y + (target_y - prev_y) / SMOOTHING
                cur_x = min(max(cur_x, 1), SCREEN_W - 2)
                cur_y = min(max(cur_y, 1), SCREEN_H - 2)

                pyautogui.moveTo(cur_x, cur_y)
                prev_x, prev_y = cur_x, cur_y
                cv2.circle(frame, (int(x_px), int(y_px)), 10, (0, 255, 0), cv2.FILLED)

            elif two_up:
                gap = dist(lm[INDEX_TIP], lm[MIDDLE_TIP]) / palm_size
                if gap < CLICK_RATIO:
                    mode = "LEFT CLICK"
                    prev_scroll_y = None
                    if now - last_click > CLICK_COOLDOWN:
                        pyautogui.click()
                        last_click = now
                    cx = int((lm[INDEX_TIP].x + lm[MIDDLE_TIP].x) / 2 * w)
                    cy = int((lm[INDEX_TIP].y + lm[MIDDLE_TIP].y) / 2 * h)
                    cv2.circle(frame, (cx, cy), 12, (0, 0, 255), cv2.FILLED)
                elif gap > SCROLL_RATIO:
                    mode = "SCROLL"
                    y_now = lm[INDEX_TIP].y
                    if prev_scroll_y is not None:
                        delta = prev_scroll_y - y_now      
                        if abs(delta) > 0.004:             
                            pyautogui.scroll(int(delta * SCREEN_H * SCROLL_SPEED / 100))
                    prev_scroll_y = y_now
                else:
                    mode = "READY"
                    prev_scroll_y = None

            elif three_up:
                mode = "RIGHT CLICK"
                prev_scroll_y = None
                if now - last_right_click > RIGHT_CLICK_COOLDOWN:
                    pyautogui.rightClick()
                    last_right_click = now

            elif open_palm:
                mode = "PAUSE"
                prev_scroll_y = None
                prev_x, prev_y = pyautogui.position()

            else:
                mode = "IDLE"
                prev_scroll_y = None

        fps = 1.0 / max(time.time() - prev_time, 1e-6)
        prev_time = time.time()
        cv2.putText(frame, f"Mode: {mode}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("Virtual Mouse (press q to quit)", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    hands.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
