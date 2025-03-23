import sys
import cv2
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage

import supervision as sv
from PIL import Image
from rfdetr import RFDETRBase
from rfdetr.util.coco_classes import COCO_CLASSES

model = RFDETRBase()

class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                detections = model.predict(frame, threshold=0.5)
                annotated_image = frame.copy()

                labels = [
                    f"{COCO_CLASSES[class_id]} {confidence:.2f}"
                    for class_id, confidence
                    in zip(detections.class_id, detections.confidence)
                ]
                annotated_image = sv.BoxAnnotator().annotate(annotated_image, detections)
                annotated_image = sv.LabelAnnotator().annotate(annotated_image, detections, labels)

                Image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
    
    def stop(self):
        self.ThreadActive = False
        self.quit()

class Worker2(QThread):
    ImageUpdate = pyqtSignal(QImage)
    
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
    
    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(self.filepath)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                detections = model.predict(frame, threshold=0.5)
                annotated_image = frame.copy()
                labels = [
                    f"{COCO_CLASSES[class_id]} {confidence:.2f}"
                    for class_id, confidence
                    in zip(detections.class_id, detections.confidence)
                ]
                annotated_image = sv.BoxAnnotator().annotate(annotated_image, detections)
                annotated_image = sv.LabelAnnotator().annotate(annotated_image, detections, labels)

                Image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
    
    def stop(self):
        self.ThreadActive = False
        self.quit()