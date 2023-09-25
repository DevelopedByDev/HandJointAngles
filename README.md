# HandJointAngles

This program:
1. takes video input through either a capture device (like a camera or a webcam)
    or a pre-recorded video of patients who have undergone a medial nerve reinnervation surgery to see the 
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
