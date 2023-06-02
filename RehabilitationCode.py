'''
this program:
1. takes video input through either a capture device (like a camera or a webcam)
    or a pre-recorded video of patients who have undergone the ________ surgery to see the 
    extent and improvement in their rehabilitation

2. outputs a .csv file having calculated the angles and the angular velocities between all 
    the major joints on their fingers and the elbow by using:
        1. the wrist as the vertex of the angle
        2. the line segment between the elbow joint and the wrist as one arm of the angle and
        3. the line segments between each of the joints and the wrist as the other arms of 
            the angle

    refer to this image to understand the parts of an angle: 
    https://d138zd1ktt9iqe.cloudfront.net/media/seo_landing_files/angles-01-1643365878.png

    refer to this image to understand how that translates to angles calculated in this program:
    ___________[insert annotated image explaining parallelisms between arm and angle]__________

    1. 1 wrist joint and 20 finger joints are detected and landmarked using 
        the mediapipe.solutions.hands class; multiple hands can be tested at once but this
        program is only meant to calculate angles and angular velocities of joints of one 
        arm at a time

        refer to this diagram of the hand joints and corresponding numbered landmarks:
        https://camo.githubusercontent.com/b0f077393b25552492ef5dd7cd9fd13f386e8bb480fa4ed94ce42ede812066a1/68747470733a2f2f6d65646961706970652e6465762f696d616765732f6d6f62696c652f68616e645f6c616e646d61726b732e706e67
    
    2. 1 elbow and 1 wrist joint are detected and landmarked using the mediapipe.solutions.pose
        class; multiple hands can be tested at once but this program is only meant to calculate
        angles and angular velocities of joints of one arm at a time

        refer to this diagram of the arm joints and the corresponding numbered landmarks:
        https://camo.githubusercontent.com/7fbec98ddbc1dc4186852d1c29487efd7b1eb820c8b6ef34e113fcde40746be2/68747470733a2f2f6d65646961706970652e6465762f696d616765732f6d6f62696c652f706f73655f747261636b696e675f66756c6c5f626f64795f6c616e646d61726b732e706e67

'''

'''
importing libraries --> this code only needs:
    1. cv2: for reading videos and putting text (fps) and drawing body landmarks
        and connections
    2. mediapipe: for detecting body landmarks
    3. time: for calculating fps
'''
import numpy as np
import cv2
import mediapipe as mp
import time
import csv

# paramter 0 in VideoCapture refers to the first video recording device on the user's computer
# this can be changed to other positive numbers depending how many cameras are connected to
# the user's computer or
# if a pre-recorded video needs to be analyzed, the pathname of the video can be input as a 
# string to the argument
cap = cv2.VideoCapture(0)

# Gets Hand landmarks and connections
mpHands = mp.solutions.hands
hands = mpHands.Hands()

# Gets Pose (for elbow, shoulder) landmarks and connections
mpPose = mp.solutions.pose
pose = mpPose.Pose()

# Helps draw landmarks and connections for Hands and Pose using OpenCV
mpDraw = mp.solutions.drawing_utils

# setting pivot joint as the number 
PIVOT = None

# initializing current and previous times to calculate frames per second (FPS)
cTime = 0
pTime = 0


csv_rows = []
elbow_lm_list = []

while True:

    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    start_time = time.time()
    stop_time = 0.0
    time_diff = 0.0
    csv_row_list = [start_time, stop_time, time_diff]


    pose_results = pose.process(imgRGB)
    # Pose drawings
    if pose_results.pose_landmarks:   
        c = 0
        for id, lm in enumerate(pose_results.pose_landmarks.landmark):
            # the following if-conditional checks if the right elbow (id 14) is in frame of video. 
            # If not, no angle or angular velocity will be calculated which makes sense because the 
            #   elbow acts as an arm to the angle when the wrist is the pivot 
            if (id == 14) and (lm.x <= 1 and lm.x >= 0) and (lm.y <=1 and lm.y >= 0):
                
                mpDraw.draw_landmarks(img, pose_results.pose_landmarks, mpPose.POSE_CONNECTIONS)

                # appending landmark of right elbow
                current_landmark = [lm.x, lm.y, lm.z]
                elbow_lm_list.append(current_landmark)
                csv_row_list.append(current_landmark)

                # multi_hand_landmarks can have two hands to landmark, thereby two handLms at max
                # this is why it is important to run a for loop to iterate through multi_hand_landmark
                hand_results = hands.process(imgRGB)
                if hand_results.multi_hand_landmarks:
                    for handLms in hand_results.multi_hand_landmarks:
                        # handLms.landmark is the Python list of all hand landmarks observed in one frame
                        for lmk in handLms.landmark:
                            current_landmark = [lmk.x, lmk.y, lmk.z]
                            csv_row_list.append(current_landmark)
                        mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                stop_time = time.time()
                csv_row_list[1] = stop_time
                time_diff = stop_time - start_time
                csv_row_list[2] = time_diff
                if len(csv_row_list) == 25:
                    csv_rows.append(csv_row_list)

# Controlling and displaying frames per second (FPS)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 10)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



for csv_row in csv_rows:

    angles = []

    elbow_lm = np.array(csv_row[3])
    wrist_lm = np.array(csv_row[4])
    arm_vector = elbow_lm - wrist_lm
    for hand_lm in csv_row[5:]:
        hand_lm = np.array(hand_lm)
        joint_vector = hand_lm - wrist_lm

        # joint angle in degrees
        joint_angle = np.arccos(np.dot(arm_vector, joint_vector)/(np.linalg.norm(arm_vector) * np.linalg.norm(joint_vector)))
        joint_angle *= (180/np.pi)
        angles.append(joint_angle)

    # appending angles and angular_velocity to csv_rows
    for j in angles:
        csv_row.append(j)

angular_velocities = []

for i in range(1, len(csv_rows)):
    angular_velocities_row = []
    angle_row = np.array(csv_rows[i][25:]) - np.array(csv_rows[i-1][25:])
    angular_velocities_row = angle_row / csv_rows[i][2]
    angular_velocities_row = list(angular_velocities_row)
    angular_velocities.append(angular_velocities_row)

del csv_rows[0]

for i in range(len(csv_rows)):
    csv_rows[i] += angular_velocities[i]

# opening a .csv file to write landmarks, angles and angular velocities into
# TODO: check if landmarks.csv exists, if not create it in the same directory as this program
with open('landmarks.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # 65 columns
    writer.writerow([
                     'start_time', 'stop_time', 'time_diff',
                     'r_elbow_lm', 
                     'r_wrist_lm', 
                     'r_hand_1_lm', 'r_hand_2_lm', 'r_hand_3_lm', 'r_hand_4_lm', 'r_hand_5_lm', 'r_hand_6_lm', 'r_hand_7_lm', 'r_hand_8_lm', 'r_hand_9_lm', 'r_hand_10_lm', 'r_hand_11_lm', 'r_hand_12_lm', 'r_hand_13_lm', 'r_hand_14_lm', 'r_hand_15_lm', 'r_hand_16_lm', 'r_hand_17_lm', 'r_hand_18_lm', 'r_hand_19_lm', 'r_hand_20_lm',
                     'r_hand_1_a',  'r_hand_2_a', 'r_hand_3_a', 'r_hand_4_a', 'r_hand_5_a', 'r_hand_6_a', 'r_hand_7_a', 'r_hand_8_a', 'r_hand_9_a', 'r_hand_10_a', 'r_hand_11_a', 'r_hand_12_a', 'r_hand_13_a', 'r_hand_14_a', 'r_hand_15_a', 'r_hand_16_a', 'r_hand_17_a', 'r_hand_18_a', 'r_hand_19_a', 'r_hand_20_a',
                     'r_hand_1_av',  'r_hand_2_av', 'r_hand_3_av', 'r_hand_4_av', 'r_hand_5_av', 'r_hand_6_av', 'r_hand_7_av', 'r_hand_8_av', 'r_hand_9_av', 'r_hand_10_av', 'r_hand_11_av', 'r_hand_12_av', 'r_hand_13_av', 'r_hand_14_av', 'r_hand_15_av', 'r_hand_16_av', 'r_hand_17_av', 'r_hand_18_av', 'r_hand_19_av', 'r_hand_20_av'
                     ])
    for csv_row in csv_rows:
        writer.writerow(csv_row)