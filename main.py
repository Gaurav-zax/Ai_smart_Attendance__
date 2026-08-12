import cv2
import csv
import os
from datetime import datetime
from attendance import mark_attendance



# Unknown face folder

unknown_folder = "unknown_faces"


if not os.path.exists(unknown_folder):

    os.makedirs(unknown_folder)



# Duplicate attendance control

marked_students = set()



# Haar Cascade

face_cascade = cv2.CascadeClassifier(
    "haarcascade_frontalface_default.xml"
)



# Recognizer

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read(
    "trainer/trainer.yml"
)



# Students load

names = {}


with open("students.csv","r") as file:


    reader = csv.DictReader(file)


    for row in reader:


        names[int(row["Student_ID"])] = row["Student_Name"]





# Camera

camera = cv2.VideoCapture(0)


print("AI Face Recognition Started")



unknown_saved = False



while True:


    ret, frame = camera.read()


    if not ret:

        print("Camera not detected")
        break



    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )



    faces = face_cascade.detectMultiScale(
        gray,
        1.3,
        5
    )



    for (x,y,w,h) in faces:



        student_id, confidence = recognizer.predict(
            gray[y:y+h,x:x+w]
        )



        confidence_percent = round(
            100-confidence
        )


        if confidence_percent < 0:

            confidence_percent = 0


        if confidence_percent > 100:

            confidence_percent = 100





        if confidence < 70:



            name = names.get(
                student_id,
                "Unknown"
            )


            color = (0,255,0)


            status = "Known"



            if student_id not in marked_students:


                mark_attendance(
                    student_id,
                    name
                )


                marked_students.add(
                    student_id
                )



        else:



            name = "UNKNOWN PERSON"


            color = (0,0,255)


            status = "Unknown"



            # Screenshot save once

            if not unknown_saved:


                time = datetime.now().strftime(
                    "%H-%M-%S"
                )


                path = os.path.join(
                    unknown_folder,
                    f"unknown_{time}.jpg"
                )


                cv2.imwrite(
                    path,
                    frame
                )


                print(
                    "Unknown face saved:",
                    path
                )


                unknown_saved = True






        cv2.rectangle(
            frame,
            (x,y),
            (x+w,y+h),
            color,
            2
        )



        cv2.putText(
            frame,
            name,
            (x,y-35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            color,
            2
        )



        cv2.putText(
            frame,
            f"Confidence: {confidence_percent}%",
            (x,y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )



        cv2.putText(
            frame,
            status,
            (x,y+h+25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )




    cv2.imshow(
        "AI Smart Attendance Camera",
        frame
    )



    if cv2.waitKey(1) & 0xFF == ord("q"):

        break




camera.release()

cv2.destroyAllWindows()