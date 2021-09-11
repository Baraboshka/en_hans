from typing import BinaryIO
import numpy as np
from keras.models import load_model
import cv2

class CVEmotionRecognizer:
    
    def get_video_emotion(self, video_path: BinaryIO):
        self.video = video_path
        
        xception = load_model('final_xception.h5')
        xception.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        cap = cv2.VideoCapture(self.video)

        fin_pred = np.empty((0,7), float)

        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            # Our operations on the frame come here


            # Display the resulting frame

            new_frame = cv2.resize(frame,(48,48))
            gray_image = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
            y = np.expand_dims(gray_image, axis=-1)
            y = np.expand_dims(y, axis=0)
            pred = xception.predict(y)
            print(pred)
            fin_pred = np.append(fin_pred,pred,axis=0)

            if cv2.waitKey(1) == ord('q'):
                break


        f_pred = fin_pred.sum(axis=0)

        dic = { 0: "Angry",
           1: "Disgust",
           2:"Fear",
           3:"Happy",
           4:"Sad",
           5:"Surprise",
           6:"Neutral"}

        emotion = dic[np.where(f_pred == f_pred.max())[0][0]]

        return emotion

