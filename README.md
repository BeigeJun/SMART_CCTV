Posture classification🙎‍♂🙅‍♂🙆‍♂💁‍♂🙋‍♂🙇‍♂🤦‍♂🤷‍♂

🏆 안양대학교 캡스톤디자인경진대회 장려상 작품입니다.

🧬 자세 추정 -> 🧬 자세 분류 -> 📡 Fast API 까지 구현되어있습니다.

최종 결과물은 웹 페이지까지 만들어서 낙상을 감지하면 지정한 핸드폰으로 연락이 가는 웹 CCTV 페이지를 구현했습니다.

## 📂 Contents
  - 👀 Overview
  - 📂 Directory_설명
  - 🧬 MLP의_장점
  - 🤾 낙상감지-알고리즘
  - 👋 마무리
    
------------
## 👀 Overview
 - 프로젝트 기간 : 2024/5/12 ~ 2024/11/21
 - 개발환경 : Pycham, Anaconda
 - 개발언어 : Python, Pytorch
 - 맴버 : 단독개발
> 캡스톤 디자인 1학기때 구상한 Posture_Correction의 연장선인 프로젝트입니다. 자세 추정에 관심이 많았기 때문에 처음엔 자세추정 즉, Pos Estimation을 구현을 해볼까 했었지만 아직 지식의 부족함을 느끼고 Posture Classification을 목표로 진행하였습니다. 총 5개의 방법을 사용하여 자세 분류를 시도해보았으며, 대표로 CNN과 MLP를 사용하여 자세 분류를 하였습니다.

## 📂 Directory_설명
<details>
<summary>설명</summary>
<div markdown="1">
  
+ 0.Util
  + CNN, MLP 모델을 학습하기전 데이터들을 전처리할 때 사용하는 프로그램들을 모아두었습니다.
    
+ 01.MLP_With_Coordinates
  + MLP를 사용하여 자세 분류를 한 첫번째 시도입니다.
  + 본 모델은 신체의 좌표들을 인풋으로 받아 학습을 합니다.
  + 인터넷에서 쉽게 찾아볼 수 있는 방법입니다.
    
+ 02.Use_CNN
  + 총 3가지 Image Classification 모델을 사용하여 학습 후 자세 분류를 시도하였습니다.
  + 모델은 MobileNetV3, ResNet50, GoogleNet 으로 선정하였습니다.
  + 논문을 찾아보면 많이 보이는 방법중 하나입니다. 허나 CNN을 사용하면 자세 추정 모델은 안쓰고 그 상황 전체 이미지를 사용하는것 같습니다.

+ 03.2Step_MLP
  + 어깨와 어깨의 길이와 골반과 골반의 길이를 이용하여 가까워지고 멀어지고를 판별하고 몸의 기울기가 0.3 이하 -0.3 이상이면 서있는 상태 아니면 기울어진 상태로 판단하였습니다. <- 이건 인공지능이 아니어서 바로 폐기하였습니다.
  + 이제부터 본격적으로 사용한 몸의 관절 각도를 사용하여 자세를 평가하였습니다.

+ 04.Four_MLP
  + 각도를 이용해 학습을 한 결과 처음에는 80%정도의 정확도가 나왔던걸로 기억합니다. 정확도를 높이기 위해 몇가지 가설을 세워보았습니다. 첫번째 가설로 MLP를 두번쓰면서 첫 MLP는 사람의 몸각도에 따른 클래스 분류 그리고 두번째 MLP는 자세 분류를 하면 정확도가 개선되지 않을까 였습니다. 그래서 첫 MLP에서는 3개의 Class를 분류하고 두번째 MLP는 그 Class에 맞는 동작들로만 분류를 하도록 하였습니다. 하지만 정확도는 개선되지 않아 다른 방법을 시도하게 되었습니다. 이는 05.MLP_With_Angle/5_3/ 에서 더욱 연구해보았습니다.

+ 05.MLP_With_Angle
  + 이 디렉토리에 제가 테스트해본 핵심이 있다고 생각합니다. 우선 대표적으로 RNN, LSTM, 중간 Input 추가, 자동 학습 기능 이렇게 4가지 입니다. 이중 RNN과 LSTM은 얕은 지식을 가지고 했기때문에 나중에 공부를 더 해보고 다시 시도해볼 예정입니다. 중간 Input추가는 말 그대로 신경망 중간에 Input을 추가하는 방법이었습니다. 저는 낙상 감지 CCTV라는 주제로 진행하였기떄문에 사람의 몸 기울기에 정답이 있을거라고 예상했습니다. 그래서 첫 인풋에 몸의 기울기 추가, 중간부분에 추가 등 여러부분에 추가를 해보면서 테스트를 해보았습니다. 결과는 그렇게 좋지않아 다시 처음과 같이 중간에 Input을 추가하지 않는 형태로 진행하였습니다. 자동학습은 06.Find_The_Best에서 다루겠습니다.

+ 06.Find_The_Best
  + 이름 그대로 최고의 모델을 찾는 과정이었습니다. 은닉층의 개수를 변경해가면서 전에 학습이 완료된 모델보다 더 좋은 성능을 낼 수 있는 모델이 있는지 궁금하였습니다. 그래서 2,3,4,5,6 개수의 은닉층을 갖는 모델들을 각각 학습을 하면서, 하나의 모델을 하나의 노드수로 진행하지않고 여러 노드수를 사용해 학습을 각각했습니다. 예를 들어서 은닉층이 두개인 모델의 경우 입력층 - 은닉층 - 은닉층 - 출력층 구조일 텐데 은닉층을 3,3 을 넣어보고 5,5 도 넣어보고 7,7 도 넣는다는 말입니다. 이걸 단일 학습으로 하자니 학교나 회사에 있을 때 학습이 끝날때 시간이 아깝덜라고요. 이때 한 모델당 반나절 정도 걸렸습니다. 그래서 엑셀에 원하는 레이어수와 optimizer, DropOut 을 작성해주면 제가 작성한 모델 구조를 전부 학습을 시켜주는 시스템을 구축하였습니다. 한번 학습을 걸고 이틀 뒤나 사흘뒤에 확인하니 정말 편했던것 같습니다. 이때 은닉층은 늘어날 수록 성능이 좋았으며, 특히 입력층 - 64 - 128 - 256 - 256 - 128 - 64 - 출력층, Adam, DorpOut = 0.2(층 사이마다 다 넣었습니다.) 이 95%의 성능을 보여주어서 발표때 이 모델을 사용하였습니다. 

+ 07.Final_Model
  + 마지막으로 작품에 사용할 모델을 어떤식으로 사용할지 틀을 잡았습니다. 낙상감지는 여러명일 경우 트레이싱 기능이 없기때문에 신뢰도가 없다고 생각하여 1인모드와 다인모드로 나눠서 만들어봤습니다. 1인모드는 낙상감지를 지원하는것에 반해 다인모드는 낙상모드가 가능하지만 1인모드와 다른점은 알고리즘 적용이 아닌 자세 분류 후 특정 자세에 낙상 판정을 하는게 다릅니다. 다른 기능으로는 시크릿 모드라고 frame값을 0으로 채워서 검은 화면 위에 키포인트만 보이게 해보았습니다.

+ 08.Apply_FastAPI 
  + 최종 모델 및 알고리즘들을 FastApi에 적용하였습니다.

</div>
</details>

------------

## 🧬 MLP의_장점

+ MLP를 사용한 이유
  + CNN을 사용하면 대부분 분별할 수 있을 텐데 왜 다른 방법을 사용했냐 궁금해 하실수 있습니다. 이번 프로젝트는 실시간 추정 및 분류 홈페이지기 때문에 최소의 연산량으로 분류가 이루어지게 하였습니다. 그래서 MobileNet보다 연산량이 적은 MLP를 선택하였습니다. 위에서는 CNN을 하다가 구현을 못하여 MLP를 개발했다고 작성했지만 두 방법 모두 구현하고 연산량을 비교해 보았습니다. MobileNet의 Input은 224 * 224, 300 * 500을 사용하였습니다. 마지막 표를 참고해주시면 감사하겠습니다.

  + 그 이외에도 여러 이유가 있습니다. 첫번째로 실험해본 좌표를 이용한 학습에서는 사람이 어디에 있는지에 따라서 학습량이 많아야하거나 아니면 전처리로 좌표들을 절대 좌표로 변환해주는 과정이 필요 합니다. 그리고 이미지를 이용하여 했을 때는 원본 이미지에서 사람의 부분을 크롭해서 사용하기엔 사람의 다양성에 영향을 너무 많이 받을거 같아서 좌표를 점과 선으로 이어서 사진으로 변경하고 점과 선만있는 이미지로 학습하였습니다. 각 클래스에서 3개의 데이터를 가지고와서 테스트해본 결과 정확도 100이라는 결과가 있었지만 전처리에서 16 ms가 걸려 너무 무겁다고 판단하였습니다.
 
  + 또한 실시간 분류를 할 때 MobileNet은 Input 300 * 500 기준은 누움 자세를 분류하지 못하였고 224 * 224는 넘어짐 자세 분류하는데 낮은 정확도를 보였습니다. 반면 MLP는 모든 자세를 잘 잡아 냈습니다.
    
  + 마지막으로 각도를 이용한 이유는 좌표와 다르게 위치가 변해도 각도는 동일하고, 사람들의 신체적 특성이 다르다해도 각도는 같기 떄문입니다. 정말 단순하지만 좋은 이유라고 생각합니다. 전처리에서도 좌표를 이용해서 각도계산 12번만하면 끝이나기 때문입니다. 그리고 전처리 속도도 이미지를 사용했을 때보다 빨랐습니다. 그래서 이 프로젝트에서 제가 각도를 사용하였습니다.

| 모델 |Input | 연산량 | 전처리 시간 | 분류 시간 |
| --- | --- | --- | --- |
| MLP | 12 | 148608 | 1 ms | 0.9 ms |
| MobileNetV3 Small | 224 * 224 | 67,337,440 | 16 ms | 6 ms |
| MobileNetV3 Large | 224 * 224 | 244,009,376 | 16 ms | 7 ms |
| MobileNetV3 Small | 300 * 500 | 205,095,728 | 16 ms | 7 ms |
| MobileNetV3 Large | 300 * 500 | 205,095,728 | 16 ms | 9 ms |

------------

## 🤾 낙상감지-알고리즘
+ 낙상에는 정말 많은 종류가 있습니다. 그중 저희는 넘어지는 장면을 잡아내는것을 목표로 하였습니다. 서있음, 의자에 앉음, 바닥에 앉음, 휘청거림, 넘어짐, 누움 이렇게 6가지 종류로 학습을 진행하였으며 중요하게 생각한 종류는 휘청거림, 넘어짐, 누움 이 세가지였습니다. 낙상을 할 때 보이는 자세이기 때문입니다. 그래서 저는 나머지 3가지 자세는 평상시, 낙상과 관련된 자세는 주의가 필요한 상황으로 나눠야한다고 생각하였습니다. 제가 잡아낼수있는 낙상은 두가지이며 하나는 천천히 균형을 잃으며 넘어지는 경우와 하나는 어디에 걸려 넘어지는 경우입니다. 이렇게 두개인 이유는 이 낙상감지 CCTV는 고령의 노인분들을 타겟으로 개발을 진행하였기 때문입니다.

+ 천천히 균형을 잃고 넘어지는 경우
  + 저는 배열을 이용해 총 10번의 감지를 저장하였습니다. 시간의 순서대로 하나씩 넣고 10개가 넘으면 맨 앞을 버리는 식으로 저장을 하였습니다. 그리고 10번째 자세가 넘어짐 혹은 누움 상태일 때 앞에 저장해둔 자세들을 평가합니다. 9개중 7개 이상이 휘청거림 라벨이면 이를 낙상으로 판단하고 알림을 울립니다.
+ 밑 표는 낙상으로 감지 안했을 때의 배열입니다.

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 휘청거림 | 의자에 앉음 | 휘청거림 | 바닥에 앉음 | 바닥에 앉음 | 휘청거림 | 바닥에 앉음 | 바닥에 앉음 | 휘청거림 | 넘어짐 |

+ 밑 표는 낙상으로 감지 했을 때의 배열입니다.

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 휘청거림 | 휘청거림 | 휘청거림 | 휘청거림 | 휘청거림 | 휘청거림 | 휘청거림 | 바닥에 앉음 | 바닥에 앉음 | 넘어짐 |

+ 어디에 걸려 넘어지는 경우
  + 이 경우 키포인트 모델이 감지를 못하는 경우가 정말 많습니다. 99%는 넘어지는과정을 잡지 못하였습니다. 그래서 잡지 못하는 프레임의 수를 확인하여 이 문제를 해결하였습니다. 모델이 돌아가는데 사람의 형태를 찾지 못한 수를 확인하고 그 횟수가 5번이 되면 다음 사람의 키포인트를 잡고 분류를 하였을 때 넘어짐 혹은 누움 상태이면 낙상으로 판단하고 알람을 울립니다.
+ 밑 표는 낙상으로 감지 안했을 때의 배열입니다.
    
| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 서있음 | 서있음 | 서있음 | X | 서있음 | 서있음 | X | X | 서있음 | 넘어짐 |

+ 밑 표는 낙상으로 감지 했을 때의 배열입니다.
    
| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 서있음 | 서있음 | 서있음 | X | X | X | X | X | X | 넘어짐 |

| 시연 |
| --- |
| 평상시 | 낙상 상황 1 |
| ![Nomal](https://github.com/user-attachments/assets/3fff9815-2ca4-4871-8f0a-b77a07264409) | ![FallDown1](https://github.com/user-attachments/assets/462ec677-2d69-4ca7-a7b8-388a9cff02fa) |
| 낙상 상황 2 | 낙상 상황 3 |
| ![FallDown2](https://github.com/user-attachments/assets/899a7788-1098-4b92-b86e-852a9c6c0161) | ![FallDown3](https://github.com/user-attachments/assets/3f16039c-d52b-4124-8c33-4e254dccf751) |
| 낙상 상황 4 |  |
| ![FallDown4](https://github.com/user-attachments/assets/400ad929-b9f6-4977-9b0d-aa3e680024e7) |  |

###결과

 두가지 방법으로 낙상을 감지하였지만 대부분 두번째에 소개한 방법으로 감지를 많이 한 것 같습니다. keypointrcnn_resnet50_fpn의 정확성은 좋지만 사람이 빠르게 움직이면 감지를 잘 못하는 경향이있어 그런것 같습니다. 그리고 평상시 영상과 낙상 영상을 구별을 하긴 하지만 정확도가 70% 정도 되는 것 같습니다.

------------
 
## 👋 마무리
+ 정말 이번 프로젝트는 간단한 모델을 이용해서 높은 정확도를 만들어 보려했던 도전이었습니다. 낙상감지 보다는 자세 분류에 신경을 많이 썼던 것 같습니다.
+ 또한 배운점도 매우 많습니다. 데이터를 전처리 하는 과정에서 더 편하게 하는 Util도 만들었고, 자동 학습 기능도 만들어 보면서 편리함을 추구하는 법을 알게 되었습니다. 뿐만 아니라 Image Classification에 여러가지 모델이 있다는 것도 부끄럽지만 이번 기회에 제대로 알게 되었습니다.
+ 위는 제가 구현하면서 배운점이라면 이제는 도전하고 싶은 점입니다. LSTM을 이용하여 자세 "예측"을 해보고 싶습니다. 그래서 RNN부터 천천히 공부해볼 예정입니다.
+ 그리고 이런 위급 상황 감지 CCTV에는 Anomaly Detection이 많이 사용 된다는 것을 알았습니다. 이 네트워크도 공부후 구현에 도전할 예정입니다.
+ 대학교를 다니면서 해봤던 팀 프로젝트는 계획이 주로 평가 대상이었고 구현을 많이 본적이 없어서 아쉬웠는데 마지막 캡스톤 디자인 경진대회 덕분에 졸업전 프로젝트 다운 프로젝트를 했습니다. 
