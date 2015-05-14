import numpy as np
import cv2
import Queue

try:
	#Take the xml file from a Haar training session and apply it to the plate_cascade variable
	plate_cascade = cv2.CascadeClassifier('cascade.xml')
except:
	print "Error with cascade.xml"		#error handler if cascade.xml is not found

#cv2.VideoCapture allows you to import videos to run through your CascadeClassifier
cap = cv2.VideoCapture('IMG_0851C.mp4')

#creates a queue to store all of the detected objects
crop_q = Queue.Queue()

#cap.get will aquire the width and height of the video so we can use these values for scaling
width = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)

#numRect is used to keep track of the number of objects detected to more easily identify if
#improvements are being made when tuning parameters 
numRect = 0

"""
	min and max size determine the maximum size of the objects that can be detected.
	we take the previously aquired width and height from cap.get and use the algorithm 
	to scale the values up from the original testing resolution

	width and height are being divided by the original test resolution 640x480 this 
	way only the initial parameters will need to be tuned and they will scale with 
	the image.
"""
minSizeH = int( 30 * (width/640) )
minSizeW = int( 30 * ( height / 480 ) )
 
maxSizeH = int( 60 * ( width / 640 ) )
maxSizeW = int( 60 * ( height / 480 ) )

#this print statements will display the rectangle size in the command prompt
print "Width is: " + str( width ) + " Height is: " + str( height )
print "minSizeH: " + str(minSizeH) + " minSizeW: " + str(minSizeW )
print "maxSizeH: " + str(maxSizeH) + " maxSizeW: " + str(maxSizeW )

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
	plates = plate_cascade.detectMultiScale(
		gray, 
		scaleFactor=1.1, 
		minNeighbors=20,
		minSize=(minSizeH, minSizeW),
		maxSize=(maxSizeH, maxSizeW),
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
	
	for (x,y,w,h) in plates:
		cv2.rectangle(gray,(x,y),(x+w,y+h),(176,23,255),2)
		crop_img = gray[y:y+h, x:x+w]
		
		numRect = numRect + 1	

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
	cv2.imshow('Plate Detection',gray)
	cv2.imshow('cropped image',crop_img)

	#puts the cropped image onto the queue 
	crop_q.put(crop_img)

	cv2.waitKey(10)

	#this prints the number of rectangles detecting but only if divisible by 13 to keep the data stream small
	if not numRect % 13:
		print str(numRect)
		
print "the loop is broken"
print str(crop_q.qsize())

cv2.destroyAllWindows()
numRect = 0

while not crop_q.empty():
	numRect = numRect + 1
	crop_img = crop_q.get()

	cv2.imshow('second detection', crop_img)

cv2.destroyAllWindows()

print str(numRect)
