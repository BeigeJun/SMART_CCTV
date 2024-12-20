import cv2
import torch
from torchvision import models, transforms
import numpy as np
import torch.nn as nn
from collections import Counter
from tkinter import messagebox

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

keypoint_model = models.detection.keypointrcnn_resnet50_fpn(pretrained=True).to(device).eval()
# cap = cv2.VideoCapture('C:/Users/wns20/PycharmProjects/SMART_CCTV/05.MLP_With_Angle/5_5/TestVideo/DangerSleep.mp4')
cap = cv2.VideoCapture('C:/Users/wns20/Desktop/z.mp4')


def preprocess(image):
    transform = transforms.Compose([
        transforms.ToTensor()
    ])
    return transform(image).unsqueeze(0).to(device)

def show_message():
    messagebox.showinfo("경고", "낙상이 감지 되었습니다!")

class MLP(nn.Module):
    def __init__(self, input_size, num_classes):
        super(MLP, self).__init__()
        self.relu = nn.ReLU()
        self.fc1 = nn.Linear(input_size, 64)
        self.fc2 = nn.Linear(64, 128)
        self.fc3 = nn.Linear(128, 256)
        self.fc4 = nn.Linear(256, 256)
        self.fc5 = nn.Linear(256, 128)
        self.fc6 = nn.Linear(128, 64)
        self.fc7 = nn.Linear(64, num_classes)
        self.dropout1 = nn.Dropout(p=0.2)
        self.dropout2 = nn.Dropout(p=0.3)
        self.dropout3 = nn.Dropout(p=0.4)
        self.dropout4 = nn.Dropout(p=0.5)
        self.dropout5 = nn.Dropout(p=0.5)

    def forward(self, x):
        out = self.dropout1(x)
        out = self.fc1(out)
        out = self.relu(out)
        out = self.dropout2(out)
        out = self.fc2(out)
        out = self.relu(out)
        out = self.dropout3(out)
        out = self.fc3(out)
        out = self.relu(out)
        out = self.dropout4(out)
        out = self.fc4(out)
        out = self.relu(out)
        out = self.dropout3(out)
        out = self.fc5(out)
        out = self.relu(out)
        out = self.dropout2(out)
        out = self.fc6(out)
        out = self.relu(out)
        out = self.dropout1(out)
        out = self.fc7(out)
        return out


first_mlp_model = MLP(input_size=12, num_classes=6)
first_mlp_model.load_state_dict(torch.load('Bottom_Loss_Validation_MLP.pth'))
first_mlp_model = first_mlp_model.to(device).eval()


def make_angle(point1, point2):
    if point1[0] - point2[0] != 0:
        slope = (point1[1] - point2[1]) / (point1[0] - point2[0])
    else:
        slope = 0
    return slope


First_MLP_label_map = {0: 'FallDown', 1: 'FallingDown', 2: 'Sit_chair', 3: 'Sit_floor', 4: 'Sleep', 5: 'Stand'}

Label_List = []

boolHumanCheck = False
nNotDetected = 0
while cap.isOpened():
    ret, frame = cap.read()
    boolFallCheck = False
    if not ret:
        break

    input_tensor = preprocess(frame)
    with torch.no_grad():
        outputs = keypoint_model(input_tensor)

    for i in range(len(outputs)):
        output = outputs[i]
        scores = output['scores'].cpu().numpy()
        high_scores_idx = np.where(scores > 0.95)[0]
        print(len(high_scores_idx))
        if len(high_scores_idx) > 0:
            keypoints = output['keypoints'][high_scores_idx[0]].cpu().numpy()
            keypoint_scores = output['keypoints_scores'][high_scores_idx[0]].cpu().numpy()
            boxes = output['boxes'][high_scores_idx[0]].cpu().numpy()
            check_count = 0
            for idx, kp_score in enumerate(keypoint_scores):
                if kp_score < 0.9:
                    check_count += 1
            if check_count < 2:
                angles = []
                angles.append(make_angle(keypoints[5], keypoints[6]))  # 왼쪽 어깨 -> 오른쪽 어깨
                angles.append(make_angle(keypoints[5], keypoints[7]))  # 왼쪽 어깨 -> 왼쪽 팔꿈치
                angles.append(make_angle(keypoints[7], keypoints[9]))  # 왼쪽 팔꿈치 -> 왼쪽 손목
                angles.append(make_angle(keypoints[6], keypoints[8]))  # 오른쪽 어깨 -> 오른쪽 팔꿈치
                angles.append(make_angle(keypoints[8], keypoints[10]))  # 오른쪽 팔꿈치 -> 오른쪽 손목
                angles.append(make_angle(keypoints[5], keypoints[11]))  # 왼쪽 어깨 -> 왼쪽 골반
                angles.append(make_angle(keypoints[6], keypoints[12]))  # 오른쪽 어깨 -> 오른쪽 골반
                angles.append(make_angle(keypoints[11], keypoints[12]))  # 왼쪽 골반 -> 오른쪽 골반
                angles.append(make_angle(keypoints[11], keypoints[13]))  # 왼쪽 골반 -> 왼쪽 무릎
                angles.append(make_angle(keypoints[13], keypoints[15]))  # 왼쪽 무릎 -> 왼쪽 발목
                angles.append(make_angle(keypoints[12], keypoints[14]))  # 오른쪽 골반 -> 오른쪽 무릎
                angles.append(make_angle(keypoints[14], keypoints[16]))  # 오른쪽 무릎 -> 오른쪽 발목

                angles_tensor = torch.tensor(angles, dtype=torch.float32).unsqueeze(0).to(device)
                with torch.no_grad():
                    prediction = first_mlp_model(angles_tensor)
                    _, predicted_label = torch.max(prediction, 1)
                First_Label = First_MLP_label_map[predicted_label.item()]

                if len(Label_List) >= 10:
                    Label_List.pop(0)
                Label_List.append(predicted_label.item())
                if len(Label_List) >= 10:
                    if Label_List[9] == 0:

                        counterBefore = Counter(Label_List[0:11])
                        most_common_count_Before = counterBefore.most_common(1)[0][1]
                        counterBeforeLabel = counterBefore.most_common(1)[0][0]

                        if most_common_count_Before > 8 and counterBeforeLabel == 1:
                            box_color = (0, 0, 255)
                            boolFallCheck = True
                            Label_List.clear()

                        elif 1 in Label_List and nNotDetected >= 2:
                            box_color = (0, 0, 255)
                            boolFallCheck = True
                            Label_List.clear()

                        else:
                            box_color = (0, 255, 100)
                    else:
                        box_color = (0, 255, 0)

                    x1, y1, x2, y2 = map(int, boxes)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)

                    (label_width, label_height), baseline = cv2.getTextSize(First_Label, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                    cv2.rectangle(frame, (x1, y1 - label_height - baseline), (x1 + label_width, y1), box_color, cv2.FILLED)
                    cv2.putText(frame, First_Label, (x1, y1 - baseline), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    boolHumanCheck = True
                    nNotDetected = 0
            else:
                boolHumanCheck = False
                if nNotDetected < 5:
                    nNotDetected += 1
        if nNotDetected < 5:
            nNotDetected += 1
        print(nNotDetected)
    cv2.imshow('frame', frame)
    if boolFallCheck == True:
        show_message()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()