
#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
import queue
from Q import Queue#for queue using

full1 = threading.Semaphore()
empty1 = threading.Semaphore(10)
full2 = threading.Semaphore(10)
empty2 = threading.Semaphore(10)
lock1 = threading.Lock()
lock2 = threading.Lock()
#USE THIS FOR MODIFICATIONS AND USE ANOTHER FILE TO IMPORT ALL THESE FUNCTIONS AND CREATE THREADS???
def extractFrames(fileName, jpegBuffer):#rename Buffer to jpegBuffer and FUNCTION to consumerExtract
    # Initialize frame count 
    count = 0

    # open video file
    vidcap = cv2.VideoCapture(fileName)

    # read first image
    success,image = vidcap.read()
    
    print("Reading frame {} {} ".format(count, success))
    while success:
        # get a jpg encoded frame and use imwrite to store under specific file name
        success, jpgImage = cv2.imencode('.jpg', image)

        #print('{}'.format(jpgImage))
        
        #encode the frame as base 64 to make debugging easier MIGHT NOT NEED TO ENCODE
        #jpgAsText = base64.b64encode(jpgImage)

        empty1.aquire()#release full Semaphore here(one less full cell)
        lock1.acquire()#acquire Lock here

        # add the frame to the jpegbuffer
        jpegBuffer.put(jpgImage)#default jpegBuffer.put(jpgAsText)

        lock1.release()#release Lock here
        full1.release()#increase empty semaphore(one less available cell)

        success,image = vidcap.read()
        print('Reading frame {} {}'.format(count, success))
        count += 1

    print("Frame extraction complete")


def convertGray(gpegBuffer):
    #init gray count
    count = 0
    #consumer: get color frames convert to gray frames full lock empty
    full1.acquire()
    lock1.acquire()
    jpegImg = jpegBuffer.get()
    lock1.release()
    empty.release()#empty increases becuse space is now avail. in buffer
    grayFrame = cv2.cvtColor(jpegImg, cv2.COLOR_BGR2GRAY)

    
def displayFrames(inputBuffer):
    # initialize frame count
    count = 0

    # go through each frame in the buffer until the buffer is empty
    while not inputBuffer.empty():#rename inputBuffer to gpegBuffer and extend Q class to define empty
        # get the next frame
        frameAsText = inputBuffer.get()

        # decode the frame 
        jpgRawImage = base64.b64decode(frameAsText)#IF NOT ENCODED THEN NO NEED TO DECODE

        # convert the raw frame to a numpy array
        jpgImage = np.asarray(bytearray(jpgRawImage), dtype=np.uint8)

        #AFTER THIS STEP IS WHEN TO TURN TO GRAYSCALE IN SEPARATE FUNCTION
        
        # get a jpg encoded frame
        img = cv2.imdecode( jpgImage ,cv2.IMREAD_UNCHANGED)

        print("Displaying frame {}".format(count))        

        # display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow("Video", img)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        count += 1

    print("Finished displaying all frames")
    # cleanup the windows
    cv2.destroyAllWindows()

# filename of clip to load
filename = 'clip.mp4'

# shared queue  MUST CREATE ANOTHER Q(GPEGBUFFER) AND CLASS FOR Q
extractionQueue = queue.Queue()

# extract the frames
extractFrames(filename,extractionQueue)

# display the frames
displayFrames(extractionQueue)

