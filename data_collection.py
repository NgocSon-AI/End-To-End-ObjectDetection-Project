import os
import cv2
import time
import uuid

IMAGE_PATH = "CollectedImages"

labels = ["Hello", "Yes", "No", "Thanks", "IloveYou", "Please"]

number_of_images = len(labels)

for label in labels:
    img_path = os.path.join(IMAGE_PATH, label)
    os.makedirs(img_path, exist_ok=True)


    # open camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print(f"Error")
        continue

    print(f"Collecting images for {label}")
    time.sleep(5)
    for imgnum in range(number_of_images):
        ret, frame = cap.read()
        image_name = os.path.join(IMAGE_PATH, label, label + '.'+'{}.jpg'.format(str(uuid.uuid1())))
        cv2.imwrite(image_name, frame)
        cv2.imshow('frame', frame)
        time.sleep(2)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
    cap.release()
cv2.destroyAllWindows()