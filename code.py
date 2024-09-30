import cv2
import numpy as np

def get_contour_center(contour):
    m = cv2.moments(contour)
    cx = -1
    cy = -1
    if (m['m00'] != 0):
        cx = int(m['m10'] / m['m00'])
        cy = int(m['m01'] / m['m00'])
    return cx , 

def get_qunter (x,y, imageSize):
    if ( x <= imageSize[1]// 2 and y <= imageSize[0] // 2):
        return 1
    elif ( x >= imageSize[1] // 2 and y <= imageSize[0] // 2):
        return 2
    elif ( x <= imageSize[1] // 2 and y >= imageSize[0] // 2):
        return 3
    elif ( x >= imageSize[1] // 2 and y >= imageSize[0] // 2):
        return 4
    

cap = cv2.VideoCapture('test.mp4')

while (cap.isOpened()):
    ret, frame = cap.read()

    if ret == True :
        hsv_img = cv2.cvtColor (frame, cv2.COLOR_BGR2HSV)
        l_val = np.array([29 , 99 , 57])
        u_val = np.array([40 , 255 , 255])

        binary_img = cv2.inRange ( hsv_img , l_val , u_val )
        final = cv2.bitwise_and(frame , frame , mask = binary_img)

        contours , hierarchy = cv2.findContours(binary_img.copy(),
                                                cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_SIMPLE)
        
        filtered_contours = []
        for c in contours : 
            area = cv2.contourArea(c)
            if area > 500 :
                filtered_contours.append(c)
        
        if len(filtered_contours) == 0:
            print ('no tennis ball found')
        else:
            for c in filtered_contours:
                ((x , y) , radius) = cv2.minEnclosingCircle(c)
                # cv2.drawContours(frame, [c], -1, (150, 250, 150), 1)
                cv2.drawContours(final, [c], -1, (150, 250, 150), 1)
                cx , cy = (int(x) , int(y))

                # cv2.circle(frame, (cx , cy), (int)(radius), (0,0,255), 1)
                cv2.circle(final, (cx , cy), (int)(radius), (0,0,255), 1)

        qunter = get_qunter(cx , cy ,final.shape)
        font = cv2.FONT_HERSHEY_SIMPLEX
        final = cv2.putText(final , str(qunter) , (20, 55) , font , 2.2 , (0 , 255 , 255) , 2 ,  cv2.LINE_AA )
        org = cv2.putText(frame , str(qunter) , (20, 55) , font , 2.2 , (0 , 255 , 255) , 2 ,  cv2.LINE_AA )

        cv2.imshow('original' , org)
        cv2.imshow('final' , final)
        
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
