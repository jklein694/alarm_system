# USAGE
# python3 real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel
import argparse
import time

import cv2
import imutils
import matplotlib.pyplot as plt
import numpy as np
from imutils.video import FPS
from imutils.video import VideoStream

import create_chunks as cc

# import the necessary packages
# import detection_alerts as detected

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-c", "--confidence", type=float, default=0.2,
                help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

width_loc = {}
height_loc = {}
area_dict = {}
area_per_list = []

for item in CLASSES:
    width_loc[item] = []
    height_loc[item] = []
    area_dict[item] = []

area_dict['person'].append(5000)
person_counter = 0

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()

start = time.time()

# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    # grab the frame dimensions and convert it to a blob
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                 0.007843, (300, 300), 127.5)

    # pass the blob through the network and obtain the detections and
    # predictions
    net.setInput(blob)
    detections = net.forward()

    direction = []
    area_direction = []

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the prediction

        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > args["confidence"]:
            # extract the index of the class label from the
            # `detections`, then compute the (x, y)-coordinates of
            # the bounding box for the object
            idx = int(detections[0, 0, i, 1])
            # set up alert for Person, Dog, Cat
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])

            (startX, startY, endX, endY) = box.astype("int")

            if CLASSES[idx] == 'person' or 'dog':
                width = int((endX + startX) / 2)
                height = int((endY + startY) / 2)

                area = int((endX - startX) * (endY - startY))

                center = (width, height)

                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(CLASSES[idx],
                                             confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                              COLORS[idx], 2)
                cv2.circle(frame, (width, height), 2, COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

                if CLASSES[idx] == 'person':
                    person_counter += 1

                    width_loc[CLASSES[idx]].append(width)
                    height_loc[CLASSES[idx]].append(height)

                    area = int((endX - startX) * (endY - startY))
                    area_dict[CLASSES[idx]].append(area)

                    area_per_list.append(area_dict['person'][person_counter - 1] / area_dict['person'][person_counter])


                for n in range(len(width_loc['person'])):
                    try:
                        slope = width_loc['person'][n + 10] - width_loc['person'][n]
                        direction.append(slope)
                        slope_area = area_per_list[n + 50] - area_per_list[n]
                        area_direction.append(slope_area)
                    except:
                        None

                chunks = cc.create_chunks(direction, 10)
                chunks_area = cc.create_chunks(area_direction, 30)

                average_slope = []
                average_area_slope = []
                movement = 0
                for chunk in chunks:
                    average_slope.append(np.mean(chunk))
                    movement = np.mean(chunk)

                area_movement = 0
                for chunk_area in chunks_area:
                    average_area_slope.append(np.mean(chunk_area))
                    area_movement = np.mean(chunk_area)

                lng_move_list = []
                lng_move = 0
                for index in range(len(average_area_slope)):
                    try:
                        lng_move = average_area_slope[index] - average_area_slope[index - 1]
                        lng_move_list.append(lng_move)
                    except:
                        None

                speed = np.mean([movement, area_movement])
                speed_label = "{}: {:.2f}".format('Speed: ', speed)

                if movement <= -20:
                    direction_label = 'Moving Right'
                elif movement >= 20:
                    direction_label = 'Moving Left'
                else:
                    direction_label = ''

                if lng_move > 0:
                    area_direction_label = 'Moving Away'
                elif lng_move < 0:
                    area_direction_label = 'Moving Towards'
                else:
                    area_direction_label = ''

                cv2.putText(frame, direction_label, (startX + 150, y + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

                cv2.putText(frame, area_direction_label, (startX + 150, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

                cv2.putText(frame, speed_label, (startX, y + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
            else:
                None


    # show the output frame
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

    # update the FPS counter
    fps.update()

    end = time.time()
    loop_time = end - start

    if loop_time > 15:
        counter = True
        start = time.time()



# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

direction = []

# plt.plot(average_slope)
# plt.show()
# plt.plot(average_area_slope, label='area change')
# plt.plot(lng_move_list, label='area change slope')
# plt.legend()
# plt.show()

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
