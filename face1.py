### Imports ###################################################################

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import os


### Setup #####################################################################


# Setup the camera
camera = PiCamera()
camera.resolution = ( 320, 240 )
camera.framerate = 60
rawCapture = PiRGBArray( camera, size=( 320, 240 ) )

# Load a cascade file for detecting faces
face_cascade = cv2.CascadeClassifier( '/home/pi/haarcascade_frontalcatface.xml' ) 

t_start = time.time()
fps = 0


### Main ######################################################################

# Capture frames from the camera
for frame in camera.capture_continuous( rawCapture, format="bgr", use_video_port=True ):

    image = frame.array

    # Use the cascade file we loaded to detect faces
    gray = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
    faces = face_cascade.detectMultiScale( gray )

    print ("Found " + str( len( faces ) ) + " face(s)")

    # Draw a rectangle around every face and move the motor towards the face
    for ( x, y, w, h ) in faces:

        cv2.rectangle( image, ( x, y ), ( x + w, y + h ), ( 100, 255, 100 ), 2 )
        cv2.putText( image, "Face No." + str( len( faces ) ), ( x, y ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )

        tx = x + w/2
        ty = y + h/2

       
    # Calculate and show the FPS
    fps = fps + 1
    sfps = fps / ( time.time() - t_start )
    cv2.putText( image, "FPS : " + str( int( sfps ) ), ( 10, 10 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )    

    # Show the frame
    cv2.imshow( "Frame", image )
    cv2.waitKey( 1 )

    # Clear the stream in preparation for the next frame
    rawCapture.truncate( 0 )