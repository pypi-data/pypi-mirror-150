import cv2
from queue import Queue
import _thread


class YOLOv4:
    def __init__(self, classesFile, modelConfiguration, modelWeights, confThreshold=0.5, cuda=False):
        # Initialize the parameters
        self.confThreshold = confThreshold  #Confidence threshold
        self.nmsThreshold = 0.4   #Non-maximum suppression threshold
        self.inpWidth = 416       #Width of network's input image
        self.inpHeight = 416      #Height of network's input image
        self.inputQueue = Queue(maxsize=1)
        self.outputQueue = Queue(maxsize=1)
        self.outs = None

        # Load names of classes
        self.classes = None
        with open(classesFile, 'rt') as f:
            self.classes = f.read().rstrip('\n').split('\n')

        self.net = cv2.dnn.readNet(modelConfiguration, modelWeights)
        if cuda:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
        else:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        self.net = cv2.dnn_DetectionModel(self.net)
        self.net.setInputParams(size=(416, 416), scale=1 / 255, swapRB=True)

        _thread.start_new_thread(self.process_frame, ())


    # Remove the bounding boxes with low confidence using non-maxima suppression
    def detect(self, frame, draw=True):
        detected = []
        if self.inputQueue.empty():
            self.inputQueue.put(frame)

        outs = self.outs
        if not self.outputQueue.empty():
            outs = self.outputQueue.get()
            self.outs = outs
        if outs is None:
            outs = self.outs
        if outs is None:
            return detected

        classIds = []
        confidences = []
        boxes = []

        for i in range(len(outs[0])):
            classid = outs[0][i]
            score = outs[1][i]
            box = outs[2][i]
            classIds.append(classid)
            confidences.append(score)
            boxes.append(box)

        for i in range(len(classIds)):
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]

            label = '%.2f' % confidences[i]
            if self.classes:
                assert (classIds[i] < len(self.classes))
                if hasattr(classIds[i], '__len__') and len(classIds[i]) > 0:
                    label = '%s:%s' % (self.classes[classIds[i][0]], label)
                else:
                    label = '%s:%s' % (self.classes[classIds[i]], label)
            if draw:
                self.draw_label(frame, label, left, top, width, height)
            detected.append((label, left, top, width, height))
        return detected

    def draw_label(self, frame, label, left, top, width, height):
        cv2.rectangle(frame, (left, top), (left + width, top + height), (0, 0, 255), 2)
        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        top = max(top, labelSize[1])
        cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    def process_frame(self):
        while True:
            if not self.inputQueue.empty():
                frame = self.inputQueue.get()
                detections = self.net.detect(frame, self.confThreshold, self.nmsThreshold)
                self.outputQueue.put(detections)
