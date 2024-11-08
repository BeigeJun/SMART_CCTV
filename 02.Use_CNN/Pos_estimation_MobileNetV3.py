import torch
import torch.nn as nn
from torchvision import models, transforms
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
from torchvision.models.detection import KeypointRCNN_ResNet50_FPN_Weights
import time

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

Skeleton_Model = models.detection.keypointrcnn_resnet50_fpn(weights=KeypointRCNN_ResNet50_FPN_Weights.DEFAULT).to(device).eval()


def _make_divisible(v, divisor=8, min_value=None):
    if min_value is None:
        min_value = divisor
    new_v = max(min_value, int(v + divisor / 2) // divisor * divisor)
    if new_v < 0.9 * v:
        new_v += divisor
    return int(new_v)


class h_swish(nn.Module):
    def __init__(self):
        super(h_swish, self).__init__()
        self.relu6 = nn.ReLU6()

    def forward(self, x):
        return x * (self.relu6(x + 3) / 6)


class inverted_residual_block(nn.Module):
    def __init__(self, i, t, o, k, s, re=False, se=False):
        super(inverted_residual_block, self).__init__()
        expansion = int(i * t)
        if re:
            nonlinear = nn.ReLU6()
        else:
            nonlinear = h_swish()
        self.se = se
        self.conv = nn.Sequential(
            nn.Conv2d(i, expansion, 1, 1),
            nn.BatchNorm2d(expansion),
            nonlinear
        )
        self.dconv = nn.Sequential(
            nn.Conv2d(expansion, expansion, k, s, k // 2, groups=expansion),
            nn.BatchNorm2d(expansion),
            nonlinear
        )
        self.semodule = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Conv2d(expansion, _make_divisible(expansion // 4), 1, 1),
            nn.ReLU(),
            nn.Conv2d(_make_divisible(expansion // 4), expansion, 1, 1),
            h_swish()
        )
        self.linearconv = nn.Sequential(
            nn.Conv2d(expansion, o, 1, 1),
            nn.BatchNorm2d(o)
        )
        self.shortcut = (i == o and s == 1)

    def forward(self, x):
        out = self.conv(x)
        out = self.dconv(out)
        if self.se:
            out *= self.semodule(out)
        out = self.linearconv(out)
        if self.shortcut:
            out += x
        return out


class mobilenetv3(nn.Module):
    def __init__(self, ver=0, w=1.0):
        super(mobilenetv3, self).__init__()
        large = [
            [1, 16, 3, 1, False, False],
            [4, 24, 3, 2, False, False],
            [3, 24, 3, 1, False, False],
            [3, 40, 5, 2, False, True],
            [3, 40, 5, 1, False, True],
            [3, 40, 5, 1, False, True],
            [6, 80, 3, 2, True, False],
            [2.5, 80, 3, 1, True, False],
            [2.4, 80, 3, 1, True, False],
            [2.4, 80, 3, 1, True, False],
            [6, 112, 3, 1, True, True],
            [6, 112, 3, 1, True, True],
            [6, 160, 5, 2, True, True],
            [6, 160, 5, 1, True, True],
            [6, 160, 5, 1, True, True]
        ]

        small = [
            [1, 16, 3, 2, False, True],
            [4, 24, 3, 2, False, False],
            [11.0 / 3.0, 24, 3, 1, False, False],
            [4, 40, 5, 2, True, True],
            [6, 40, 5, 1, True, True],
            [6, 40, 5, 1, True, True],
            [3, 48, 5, 1, True, True],
            [3, 48, 5, 1, True, True],
            [6, 96, 5, 2, True, True],
            [6, 96, 5, 1, True, True],
            [6, 96, 5, 1, True, True],
        ]

        in_channels = _make_divisible(16 * w)

        self.conv1 = nn.Sequential(
            nn.Conv2d(3, in_channels, 3, 2, 1),
            nn.BatchNorm2d(int(16 * w)),
            nn.ReLU6()
        )
        if ver == 0:
            stack = large
            last = 1280
        else:
            stack = small
            last = 1024
        layers = []

        for i in range(len(stack)):
            out_channels = _make_divisible(stack[i][1] * w)
            layers.append(
                inverted_residual_block(in_channels, stack[i][0], out_channels, stack[i][2], stack[i][3], stack[i][4],
                                        stack[i][5]))
            in_channels = out_channels
        self.stack = nn.Sequential(*layers)
        self.last = nn.Sequential(
            nn.Conv2d(in_channels, out_channels * 6, 1, 1),
            nn.BatchNorm2d(out_channels * 6),
            h_swish(),
            nn.AdaptiveAvgPool2d(1),
            nn.Conv2d(out_channels * 6, last, 1, 1),
            h_swish(),
            nn.Conv2d(last, 6, 1, 1)
        )

    def forward(self, x):
        out = self.conv1(x)
        out = self.stack(out)
        out = self.last(out)
        out = out.view(out.size(0), -1)
        return out


def preprocess_image(image):
    if isinstance(image, str):
        image = Image.open(image).convert('RGB')
    elif isinstance(image, np.ndarray):
        image = Image.fromarray(image)

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    return transform(image).unsqueeze(0).to(device)

def make_skeleton(img):
    input_img = preprocess_image(img)
    with torch.no_grad():
        out = Skeleton_Model(input_img)[0]

    keypoints = out['keypoints'][0].cpu().numpy()

    fig, ax = plt.subplots(figsize=(3, 5))

    plt.scatter(keypoints[5:17, 0], keypoints[5:17, 1], color='red', s=300)
    head_x = (keypoints[3, 0] + keypoints[4, 0]) / 2
    head_y = (keypoints[3, 1] + keypoints[4, 1]) / 2
    plt.scatter(head_x, head_y, color='red', s=500)

    ax.axis('off')
    ax.invert_xaxis()
    ax.invert_yaxis()

    shoulder_verts = keypoints[[5, 6], :2]
    shoulder_path = Path(shoulder_verts, [Path.MOVETO, Path.LINETO])
    shoulder_line = patches.PathPatch(shoulder_path, linewidth=10, facecolor='none', edgecolor='red')
    ax.add_patch(shoulder_line)
    start_time = time.time() * 1000
    for j in range(2):
        body_verts = keypoints[[5 + j, 11 + j], :2]
        body_path = Path(body_verts, [Path.MOVETO, Path.LINETO])
        body_line = patches.PathPatch(body_path, linewidth=10, facecolor='none', edgecolor='red')
        ax.add_patch(body_line)

    pelvis_verts = keypoints[[11, 12], :2]
    pelvis_path = Path(pelvis_verts, [Path.MOVETO, Path.LINETO])
    pelvis_line = patches.PathPatch(pelvis_path, linewidth=10, facecolor='none', edgecolor='red')
    ax.add_patch(pelvis_line)

    codes = [Path.MOVETO, Path.LINETO, Path.LINETO]
    for j in range(2):
        verts = keypoints[[5 + j, 7 + j, 9 + j], :2]
        path = Path(verts, codes)
        line = patches.PathPatch(path, linewidth=8, facecolor='none', edgecolor='red')
        ax.add_patch(line)

    for j in range(2):
        verts = keypoints[[11 + j, 13 + j, 15 + j], :2]
        path = Path(verts, codes)
        line = patches.PathPatch(path, linewidth=10, facecolor='none', edgecolor='red')
        ax.add_patch(line)

    plt.tight_layout()

    fig.canvas.draw()
    img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.close(fig)
    return img, start_time

def predict_pose(model, image_tensor):
    with torch.no_grad():
        output = model(image_tensor)
    _, predicted = torch.max(output, 1)
    return predicted.item()

def main():
    model = mobilenetv3().to(device)
    model.load_state_dict(
        torch.load('C:/Users/wns20/PycharmProjects/SMART_CCTV/MobileNet_Save/BackUp/Large/Bottom_Loss_Validation_MLP.pth',
                   map_location=device))
    model.eval()

    pose_names = ['Standing', 'Fallen', 'Falling', 'Sitting on chair', 'Sitting on floor', 'Sleeping']

    cap = cv2.VideoCapture(0)

    cv2.namedWindow('Real-time Pose Estimation', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Real-time Pose Estimation', 800, 600)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        skeleton_image, start_time = make_skeleton(frame_rgb)

        skeleton_image_tensor = preprocess_image(Image.fromarray(skeleton_image))
        start_time = time.time() * 1000
        pose_label = predict_pose(model, skeleton_image_tensor)
        end_time = time.time() * 1000
        print(f"prediction time : {end_time - start_time:.3f} ms")

        cv2.putText(frame, f"Pose: {pose_names[pose_label]}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Real-time Pose Estimation', frame)
        cv2.imshow('Skeleton Image', cv2.cvtColor(skeleton_image, cv2.COLOR_RGB2BGR))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()