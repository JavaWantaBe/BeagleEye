import numpy as np
import cv2
import Queue
"""
	This module is activated when motion on a large enough scale is detected and is determined to be
	moving toward the camera. This module uses two trained classifiers, one for detecting cars and
	the other for detecting the license plate from the detected car. When a car is detected a live
	video feed is sent to the module. The image is converted to a grayscale, a median blur, and then
	an adaptive threshhold to make detection easier for the xml file. The xml file will detect the
	oncoming car and draw a rectangle around it. Each rectangle drawn is then cropped and placed
	into a queue to be ran through the second stage of detection. Each image is ran through the
	second classifier that will detect the license plate. Each time the plate is detected, that
	image will be sent to the OCR module for charecter recognition.
"""

try:
	#Take the xml file from a Haar training session and apply it to the car_cascade variable
	car = cv2.CascadeClassifier('car_classifier.xml')
except:
	print "Error with cascade.xml"		#error handler if cascade.xml is not found

#cv2.VideoCapture allows you to import videos to run through your CascadeClassifier
cap = cv2.VideoCapture('IMG_0851C.mp4')

#creates a queue to store all of the detected objects
crop_q = Queue.Queue()
lpr_q = Queue.Queue()

#cap.get will aquire the width and height of the video so we can use these values for scaling
width = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)

#numRect is used to keep track of the number of objects detected to more easily identify if
#improvements are being made when tuning parameters 
numRect = 0
img_avgW = 0
img_avgH = 0

"""
	min and max size determine the maximum size of the objects that can be detected.
	we take the previously aquired width and height from cap.get and use the algorithm 
	to scale the values up from the original testing resolution

	width and height are being divided by the original test resolution 640x480 this 
	way only the initial parameters will need to be tuned and they will scale with 
	the image.
"""
minSizeH_car = int( 50 * (width/640) )
minSizeW_car = int( 50 * ( height / 480 ) )
 
maxSizeH_car = int( 1000 * ( width / 640 ) )
maxSizeW_car = int( 1000 * ( height / 480 ) )

#this print statements will display the rectangle size in the command prompt
print "Width is: " + str( width ) + "   Height is: " + str( height )
print "minSizeH: " + str(minSizeH_car) + "      minSizeW: " + str(minSizeW_car)
print "maxSizeH: " + str(maxSizeH_car) + "     maxSizeW: " + str(maxSizeW_car)

#a never ending while loop that runs the duration of the video
while True:

	#takes each frame and puts it int the img variable for transformations and detection
	ret, img = cap.read()

	#this will break the loop when the video feed is finished
	if ret == 0:
		break

	#not a necessary bit of code, img.shape allows you to rotate your videos if needed
	rows,cols,useless = img.shape

	if not ret:
		continue

	"""
		cvtColor: 	transforms each frame and changes it into a gray scale image which makes 
					detection more precise.

		medianBlur:	This function applies a overall blur to the image, its strength is determined
					by the number following the image (gray) you want to blur. This will smooth out
					jagged edges in the image and make edges easier to detect and much smoother

		adaptiveThreshold:	applies a ADAPTIVE_THRESH_GAUSSIAN_C which converts the image into
							a black and white image and helps reduce "noise" and improve detection
							the last two values are used to adjust the blotches and determine the 
							minimum size that "noise" can be

		GaussianBlur/threshold:	The GaussinaBlur makes the image a black and white with a lot of 
								"noise". The threshold function will completely eliminate "noise"
								but only works with certain lighting, which is why it is commented out
	"""

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	gray = cv2.medianBlur(gray,1)
	gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,35,19)
	#gray = cv2.GaussianBlur(gray,(5,5),0)
	#ret1, gray = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	#these two function perform the actual rotation of your image using the img.shape function
	#the -90 is the actual rotation in degrees, + is counter clockwise and - is clockwise
	rot = cv2.getRotationMatrix2D((cols/2,rows/2),-90,1)
	gray = cv2.warpAffine(gray,rot,(cols,rows))

	gray = (255-gray)

	"""
		These parameters will define the boxs which surround detected objects, if your results are not 
		the ones you desire, tune these parameters for a more precise detection.

		scaleFactor:	Parameter specifying how much the image size is reduced at each image scale.
						scaleFactor must be greater than 1 or you will get an error. If the video is running 
						increase the scaleFactor to speed up the video.

		minNeighbors:	Parameter specifying how many neighbors each candidate rectangle should have to retain it.
						increase this parameter if you are seeing a mass number of rectangles in a small area and
						it will reduce the number of rectangles output and improve performance.

		min/max Size:	Defines the min and max possible object size. Using the algorithm above it is much easier
						to tune this and will yield more accurate results if tuned for the size of the object you 
						are trying to detect.
	"""
	car_detect = car.detectMultiScale(
		gray, 
		scaleFactor=1.3,
		minNeighbors=20,
		minSize=(minSizeH_car, minSizeW_car),
		maxSize=(maxSizeH_car, maxSizeW_car),
		flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

	"""
		this statement returns the x,y,w,h values of the picture which is the x,y coordinate of the object
		detected and the width and height of that object defining the rectangle to go around it.

		cv2.rectangle:	Takes the values returned and does the drawing of the rectangle, the numbers at the 
						end define the actual box that is being drawn. The first 3 are for color in a BGR value
						and the last number is the thickness for the box.

		crop_img:	will take the coordinates (x,y,w,h) of the rectangle being drawn and will crop the image 
					inside the rectangle. y coordinate has to come before the x for accurate cropping.

		numRect:	I use numRect to keep track of the number of objects detected. When you are tuning your 
					your parameters this number will tell you if the modifications are yielding positive or 
					negative results making tuning easier
	"""
	
	for (x,y,w,h) in car_detect:
		#cv2.rectangle(gray,(x,y),(x+w,y+h),(176,23,255),2)
		cropped_img = gray[y:y+h, x:x+w]
		numRect = numRect + 1
		img_avgH = img_avgH + h
		img_avgW = img_avgW + w

		#puts the cropped image onto the queue
		crop_q.put(cropped_img)

	"""
		I am using the imshow function to display the cropped image and to see everything the xml file is 
		detecting. This will allow you to see what your program is doing in real time as its happening.

		'Plate Detection': 	will create a window that will display the rectangles as they are being drawn
							so you can see how accurate your xml file is and allows you to adjust parameters
							more accurately.

		'cropped image':	Will show you the images inside of the rectangle. More than likely it will be to 
							fast and to frequent to be able to see the images, so it is really only there as
							a visual acknowledgement that the cropping is actually happening.
	"""
	cv2.imshow('Plate Detection', gray)
	cv2.imshow('cropped image', cropped_img)

	cv2.waitKey(10)

print "Vehicles Detected: " + str(numRect)
print "Images in Queue:   " + str(crop_q.qsize())
print "--------------------"
print "| Starting Stage 2 |"
print "--------------------"

cv2.destroyAllWindows()

plate_cascade = cv2.CascadeClassifier('cascade.xml')

img_avgH = img_avgH / numRect
img_avgW = img_avgW / numRect

minSizeH_veh = int( 30 * (img_avgW/ 640) )
minSizeW_veh = int( 30 * (img_avgH/ 480 ) )

maxSizeH_veh = int( 60 * (img_avgW/ 640 ) )
maxSizeW_veh = int( 60 * (img_avgH/ 480 ) )

stage2_img = 0
numRect = 0

while not crop_q.empty():
	crop_img = crop_q.get()

	plates = plate_cascade.detectMultiScale(
		crop_img,
		scaleFactor=1.1,
		minNeighbors=20,
		#minSize=(),
		#maxSize=(),
		flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

	for (x,y,w,h) in plates:
		#cv2.rectangle(gray,(x,y),(x+w,y+h),(176,23,255),2)
		stage2_img = crop_img[y:y+h, x:x+w]
		numRect = numRect + 1
		lpr_q.put(stage2_img)

	cv2.imshow('second detection', stage2_img)
	cv2.waitKey(50)

#print "minSizeH_veh:" + str(minSizeH_veh) + "     minSizeW_veh: " + str(minSizeW_veh)
#print "maxSizeH_veh:" + str(maxSizeH_veh) + "     maxSizeW_veh: " + str(maxSizeW_veh)

print "Number of Plates:  " + str(numRect)
print "OCR ready images:  " + str(lpr_q.qsize())

cv2.destroyAllWindows()

while not lpr_q.empty():
	ocr_image = lpr_q.get()
	cv2.imshow('OCR IMAGES FUUUUUUCK', ocr_image)

	cv2.waitKey(300)
