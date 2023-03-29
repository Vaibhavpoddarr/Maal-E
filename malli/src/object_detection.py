#!/usr/bin/python3

import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import String

class ObjectDetectorNode:
    def __init__(self):
        rospy.init_node('object_detector_node', anonymous=True)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber('/camera/image_raw', Image, self.image_callback)
        self.image_pub = rospy.Publisher('/object_detected/image_processed', Image, queue_size=10)

    def run_object_detection(self,image):
        model = cv2.dnn.readNet("./yolo_malle_last.weights",
                                "./yolo_malle.cfg")
        classes = ["ripe","unripe"]

        img = image.copy()
        img = cv2.resize(img, (800, 500))
        height, width, _ = img.shape
        ln = model.getLayerNames()
        ln = [ln[i[0]-1] for i in model.getUnconnectedOutLayers()]

        # converting before feeding to yolo model
        blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), swapRB=True, crop=False)
        model.setInput(blob)

        # getting last layer output
        Layer_out = model.forward(ln)

        # prediction
        boxes = []
        confidences = []
        class_ids = []

        for output in Layer_out:
            for detection in output:
                score = detection[5:]
                class_id = np.argmax(score)
                confidence = score[class_id]
                if confidence > 0.70:
                    box = detection[0:4] * np.array([width, height, width, height])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append((float(confidence)))
                    class_ids.append(class_id)

        # method for bounding boxes
        # index method
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        font = cv2.FONT_HERSHEY_PLAIN
        colors = np.random.uniform(0, 255, size=(len(boxes)))
        results = []

        # drawing
        if (len(indexes)) > 0.85:
            for i in indexes.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                label = str(classes[class_ids[i]])
                confidence = str(round(confidences[i], 2))
                color = colors[i]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label + "  " + confidence, (x, y - 5), font, 1, (0, 0, 0), 2)
                results.append(label)

    return img

    def image_callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        detected_frame=self.run_object_detection(cv_image)

        # Run object detection on the image frame using OpenCV
        # Replace this code with your own object detection algorithm
       

        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(detected_frame, "bgr8"))
        except CvBridgeError as e:
            print(e)

if __name__ == '__main__':
    try:
        node = ObjectDetectorNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
