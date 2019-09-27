# FacePosition.py
# Defines class FacePositioning

import cv2


class FacePositioning():
    # Defining FacePositioning class for further use

    # Start capturing camera and load the haarcascade detection data
    cap_ = cv2.VideoCapture(0)
    face_cascade_ = cv2.CascadeClassifier(
        'haarcascade_frontalface_default.xml')

    # Defining function for getting the faces in the current camera image
    # NOTE: This function does NOT close the window it makes. You'll need to import cv2.destroyAllWindows() and use it yourself.
    def getFaces(self, show_img=False):
        frame = self.cap_.read()[1]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # NOTE: The numbers inside parentheses () are minimum and maximum sizes for the
        # faces. You might want to change these depending on how far you want to be from
        # the camera and how large you want for the range of detection be.
        faces = self.face_cascade_.detectMultiScale(
            gray, 1.3, 5, 0, (30, 30), (300, 300))

        ret_faces = []

        # Handling the data of detected faces, we don't need widht and height for this
        for (x, y, w, h) in faces:
            ret_faces.append([x, y])

            # If given the show_img, show the image and draw rectangles around the faces
            if show_img:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                print("Face detected, coords=", [x, y], "size=", [w, h])

        if show_img:
            cv2.waitKey(33)
            cv2.imshow("The faces detected", frame)

        return ret_faces


if __name__ == "__main__":
    faces = FacePositioning()

    while True:
        face_coords = faces.getFaces(True)
