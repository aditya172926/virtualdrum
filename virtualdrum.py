import numpy as np
import time
import cv2
from pygame import mixer


def state_machine(sumation,sound):

	# Check if blue color object present in the ROI 	
	yes = (sumation) > Hat_thickness[0]*Hat_thickness[1]*0.8

	# If present play the respective instrument.
	if yes and sound==1:
		drum_clap.play()
		
	elif yes and sound==2:
		drum_snare.play()
		time.sleep(0.001)

def ROI_analysis(frame, sound):
	

	# converting the image into HSV
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	# generating mask for 
	mask = cv2.inRange(hsv, bluelow, blueup)
	
	# Calculating the nuber of white pixels depecting the blue color pixels in the ROI
	sumation = np.sum(mask)
	
	# Function that decides to play the instrument or not.
	state_machine(sumation,sound)
	return mask


Verbsoe = False

# importing the audio files
mixer.init()
drum_clap = mixer.Sound('drum1.wav')
drum_snare = mixer.Sound('hat1.ogg')


# HSV range for detecting blue color 
bluelow = (80,150,10)
blueup = (120,255,255)

# Frame accusition from webcam/ usbcamera 
camera = cv2.VideoCapture(0)
ret,frame = camera.read()
H,W = frame.shape[:2]

kernel = np.ones((7,7),np.uint8)

# reading the image of Hat and snare for augmentation.
Hat = cv2.resize(cv2.imread('Hat.jpg'),(200,100),interpolation=cv2.INTER_CUBIC)
Snare = cv2.resize(cv2.imread('Snare.jpg'),(200,100),interpolation=cv2.INTER_CUBIC)


# Setting the ROI area for blue color detection
Hat_center = [np.shape(frame)[1]*2//8,np.shape(frame)[0]*6//8]
Snare_center = [np.shape(frame)[1]*6//8,np.shape(frame)[0]*6//8]

Hat_thickness = [200,100]
Hat_top = [Hat_center[0]-Hat_thickness[0]//2,Hat_center[1]-Hat_thickness[1]//2]
Hat_btm = [Hat_center[0]+Hat_thickness[0]//2,Hat_center[1]+Hat_thickness[1]//2]

Snare_thickness = [200,100]
Snare_top = [Snare_center[0]-Snare_thickness[0]//2,Snare_center[1]-Snare_thickness[1]//2]
Snare_btm = [Snare_center[0]+Snare_thickness[0]//2,Snare_center[1]+Snare_thickness[1]//2]


time.sleep(1)

while True:
	
	# grab the current frame
	ret, frame = camera.read()
	frame = cv2.flip(frame,1)

	if not(ret):
		break
    
	# Selecting ROI corresponding to snare
	snare_ROI = np.copy(frame[Snare_top[1]:Snare_btm[1],Snare_top[0]:Snare_btm[0]])
	mask = ROI_analysis(snare_ROI,1)

	# Selecting ROI corresponding to Hat
	Hat_ROI = np.copy(frame[Hat_top[1]:Hat_btm[1],Hat_top[0]:Hat_btm[0]])
	mask = ROI_analysis(Hat_ROI,2)

	# A writing text on an image.
	cv2.putText(frame,'Project: Air Drums',(10,30),2,1,(20,20,20),2)
    
	# Display the ROI to view the blue colour being detected
	if Verbsoe:
		# Displaying the ROI in the Image
		frame[Snare_top[1]:Snare_btm[1],Snare_top[0]:Snare_btm[0]] = cv2.bitwise_and(frame[Snare_top[1]:Snare_btm[1],Snare_top[0]:Snare_btm[0]],frame[Snare_top[1]:Snare_btm[1],Snare_top[0]:Snare_btm[0]], mask=mask[Snare_top[1]:Snare_btm[1],Snare_top[0]:Snare_btm[0]])
		frame[Hat_top[1]:Hat_btm[1],Hat_top[0]:Hat_btm[0]] = cv2.bitwise_and(frame[Hat_top[1]:Hat_btm[1],Hat_top[0]:Hat_btm[0]],frame[Hat_top[1]:Hat_btm[1],Hat_top[0]:Hat_btm[0]],mask=mask[Hat_top[1]:Hat_btm[1],Hat_top[0]:Hat_btm[0]])
    
	# Augmenting the instruments in the output frame.
	else:
		# Augmenting the image of the instruments on the frame.
		frame[Snare_top[1]:Snare_btm[1],Snare_top[0]:Snare_btm[0]] = cv2.addWeighted(Snare, 1, frame[Snare_top[1]:Snare_btm[1],Snare_top[0]:Snare_btm[0]], 1, 0)
		frame[Hat_top[1]:Hat_btm[1],Hat_top[0]:Hat_btm[0]] = cv2.addWeighted(Hat, 1, frame[Hat_top[1]:Hat_btm[1],Hat_top[0]:Hat_btm[0]], 1, 0)
    
    
	cv2.imshow('Output',frame)
	key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, stop the loop
	if key == ord("e"):
		break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
