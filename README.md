osture classification🙎‍♂🙅‍♂🙆‍♂💁‍♂🙋‍♂🙇‍♂🤦‍♂🤷‍♂
------------
🏆 안양대학교 캡스톤디자인경진대회 장려상 작품입니다.

🧬 자세 추정 -> 🧬 자세 분류 -> 📡 Fast API 까지 구현되어있습니다.

최종 결과물은 웹 페이지까지 만들어서 낙상을 감지하면 지정한 핸드폰으로 연락이 가는 웹 CCTV 페이지를 구현했습니다.

------------
## 📂 Contents
  - [👀 Overview](#Overview)
  - [📂 Directory_설명](#Directory_설명)
------------
## 👀 Overview
 - 프로젝트 기간 : 2024/5/12 ~ 2024/11/21
 - 개발환경 : Pycham, Anaconda, FastApi
 - 개발언어 : Python, Pytorch
 - 맴버 : 단독개발
> 캡스톤 디자인 1학기때 구상한 Posture_Correction의 연장선인 프로젝트입니다. 자세 추정에 관심이 많았기 때문에 처음엔 자세추정 즉, Pos Estimation을 구현을 해볼까 했었지만 아직 지식의 부족함을 느끼고 Posture Classification을 목표로 진행하였습니다. 총 5개의 방법을 사용하여 자세 분류를 시도해보았으며, 대표로 CNN과 MLP를 사용하여 자세 분류를 하였습니다.
------------
## 📂 Directory_설명
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

+ 몸의 관절 각도를 이용한 이유
> 이 위의 내용이 초창기 내용이고 아래 내용부터 실제 사용한 모델 및 정확도를 높이기 위해 실험해본 내용입니다. CNN을 사용하면 대부분 분별할 수 있을 텐데 왜 다른 방법을 사용했냐 궁금해 하실수 있는데 제가 Model을 Save 하지 않고 다른 모델을 불러오면서 실시간 자세 분류를 하려고하다보니 되는 모델도 안되는 모델이라 생각해서 다른방법을 생각하게 되었습니다. 01 디렉토리는 좌표를 이용하여 자세를 분류하였습니다. 하지만 제가 만든 모델이지만 정말 사용불가할만큼 성능이 좋지 않았습니다. 왜인지 생각을 해보았는데 아마 한 화면으로 앞, 뒤, 옆 모든 모습을 판단해야하기 합니다. 한 화면이란 제약 사항은 같은 자세이지만 앞, 뒤, 옆의 좌표는 다르게 만듭니다. 이렇게 생각을 했기 때문에 다음 시도는 카메라를 두개를 써보자~ 였습니다. 그래서 시도해본것이 3D_Pos 프로젝트입니다. 카메라를 두개를 사용하여 앞, 옆을 촬영을 하면서 3차원 공간에 띄워보았습니다. 결과는 잘 나왔지만 이번 자세 분류 프로젝트는 실시간 낙상감지 CCTV를 목표로 하기 때문에 두번의 Kepoint Detection 연산은 너무 무겁다고 생각하여 포기하였습니다. 그 다음으로 나오게 된 생각이 좌표를 사용하는 것은 동일하나 좌표와 좌표를 선으로 이어 사람 모양으로 만든 다음 그 선들간의 각도를 이용하여 학습을 해보자였습니다. 이 생각은 꽤나 괜찮은 생각이었다고 생각합니다. 각도를 이용하면 좌표를 사용했을때 에러사항들을 잡을 수 있었기 때문입니다. 좌표는 말그대로 사람 몸의 관절 또는 특정부위의 좌표이기 때문에 사람의 체형에 따라 다른 값이 나오게 됩니다. 하지만 각도를 이용하면 체형이 달라도 같은 값으로 학습하고 모두에게 적용할 수 있습니다. 예를 들어 성인이 서있을 때 팔과 다리는 전부 180도를 유지할겁니다. 아이를 생각해봅시다. 아이 또한 서있을 때 팔 다리 전부 180도를 유지합니다. 반면 좌표로 학습을 하게 된다면 이를 위해 전처리를 한다고 하여도 제약이 있을 것으로 예상됩니다. 그래서 저는 신체 각도를 이용하여 자세 분류를 하였습니다.

+ 04.Four_MLP
  + 각도를 이용해 학습을 한 결과 처음에는 80%정도의 정확도가 나왔던걸로 기억합니다. 정확도를 높이기 위해 몇가지 가설을 세워보았습니다. 첫번째 가설로 MLP를 두번쓰면서 첫 MLP는 사람의 몸각도에 따른 클래스 분류 그리고 두번째 MLP는 자세 분류를 하면 정확도가 개선되지 않을까 였습니다. 그래서 첫 MLP에서는 3개의 Class를 분류하고 두번째 MLP는 그 Class에 맞는 동작들로만 분류를 하도록 하였습니다. 하지만 정확도는 개선되지 않아 다른 방법을 시도하게 되었습니다. 이는 05.MLP_With_Angle/5_3/ 에서 더욱 연구해보았습니다.

+ 05.MLP_With_Angle
  + 이 디렉토리에 제가 테스트해본 핵심이 있다고 생각합니다. 우선 대표적으로 RNN, LSTM, 중간 Input 추가, 자동 학습 기능 이렇게 4가지 입니다. 이중 RNN과 LSTM은 얕은 지식을 가지고 했기때문에 나중에 공부를 더 해보고 다시 시도해볼 예정입니다. 중간 Input추가는 말 그대로 신경망 중간에 Input을 추가하는 방법이었습니다. 저는 낙상 감지 CCTV라는 주제로 진행하였기떄문에 사람의 몸 기울기에 정답이 있을거라고 예상했습니다. 그래서 첫 인풋에 몸의 기울기 추가, 중간부분에 추가 등 여러부분에 추가를 해보면서 테스트를 해보았습니다. 결과는 그렇게 좋지않아 다시 처음과 같이 중간에 Input을 추가하지 않는 형태로 진행하였습니다.
  +  또 다른 하나 자동 학습인경우는 여러 모델을 Hidden Layer의 노드의 개수와 Learninn Rate, Optimizer를 먼저 Exel 파일에 작성해두면 그에 맞는 모델을 학습하고 최대 Accuracy, 최소 Loss일때 모델들을 각각 저장해줍니다. 이때 Tarin과 Validation 기준으로 총 4개의 모델이 저장이되고 학습동안 그려지는 그래프도 같이 저장이 되도록 하였습니다.
