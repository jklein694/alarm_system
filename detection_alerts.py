from playsound import playsound
import cv2

def ping(intruder, frame):
    cv2.imshow("Frame", frame)

    if intruder == 'person':
        playsound('person.mp3')
    if intruder == 'dog':
        playsound('dog.mp3')
    if intruder == 'cat':
        playsound('cat.mp3')