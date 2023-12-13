import cv2
from face_utils import read_images

path_to_training_images = './data/at'
training_image_size = (200, 200)
names, training_images, training_labels = read_images(path_to_training_images, training_image_size)
# model = cv2.face.EigenFaceRecognizer_create()
model = cv2.face.LBPHFaceRecognizer_create()
model.train(training_images, training_labels)

face_cascade = cv2.CascadeClassifier(f'{cv2.data.haarcascades}haarcascade_frontalface_default.xml')

camera = cv2.VideoCapture(0)

while (cv2.waitKey(1) == -1):
    success, frame = camera.read()
    if success:
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(120,120))
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            if roi_gray.size == 0:
                continue
            # EigenFaceRecognizer needs image resize
            # roi_gray = cv2.resize(roi_gray, training_image_size)
            label, confidence = model.predict(roi_gray)
            text = '%s, confidence=%.2f' % (names[label], confidence)
            cv2.putText(frame, text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('Face Detection', frame)