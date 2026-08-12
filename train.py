import cv2
import os
import numpy as np
from PIL import Image


# Dataset folder
path = "dataset"


# Face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()


detector = cv2.CascadeClassifier(
    "haarcascade_frontalface_default.xml"
)


def getImagesAndLabels(path):

    imagePaths = [
        os.path.join(path, f)
        for f in os.listdir(path)
    ]

    faceSamples = []
    ids = []

    for imagePath in imagePaths:

        PIL_img = Image.open(
            imagePath
        ).convert("L")

        img_numpy = np.array(
            PIL_img,
            "uint8"
        )


        filename = os.path.split(imagePath)[-1]

        id = int(
            filename.split(".")[1]
        )


        faces = detector.detectMultiScale(
            img_numpy
        )


        for (x, y, w, h) in faces:

            faceSamples.append(
                img_numpy[y:y+h, x:x+w]
            )

            ids.append(id)


    return faceSamples, ids



print("\nTraining faces...")

faces, ids = getImagesAndLabels(path)


recognizer.train(
    faces,
    np.array(ids)
)


recognizer.write(
    "trainer/trainer.yml"
)


print("\nTraining Completed!")
print("Total faces:", len(np.unique(ids)))