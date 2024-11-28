Posture classification🙎‍♂🙅‍♂🙆‍♂💁‍♂🙋‍♂🙇‍♂🤦‍♂🤷‍♂

🏆 안양대학교 캡스톤디자인경진대회 장려상 작품입니다.

🧬 자세 추정 -> 🧬 자세 분류 -> 📡 Fast API 까지 구현되어있습니다.

최종 결과물은 웹 페이지까지 만들어서 낙상을 감지하면 지정한 핸드폰으로 연락이 가는 웹 CCTV 페이지를 구현했습니다.

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

<details>
<summary>📂 Directory_설명</summary>
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

+ 몸의 관절 각도를 이용한 이유
  + CNN을 사용하면 대부분 분별할 수 있을 텐데 왜 다른 방법을 사용했냐 궁금해 하실수 있습니다. 이번 프로젝트는 실시간 추정 및 분류 홈페이지기 때문에 최소의 연산량으로 분류가 이루어지게 하였습니다. 그래서 MobileNet보다 연산량이 적은 MLP를 선택하였습니다. 위에서는 CNN을 하다가 구현을 못하여 MLP를 개발했다고 작성했지만 두 방법 모두 구현하고 연산량을 비교해 보았습니다. MobileNet의 인풋은 300*500을 사용하였습니다.

| 모델 | 연산량 | 시간 |
| --- | --- | --- |
| MLP | 148608 | 0~1 ms |
| MobileNetV3 Small | 205095728 | ms |
| MobileNetV3 Large | 747319952 | 34 ms |

  + 그 이외에도 여러 이유가 있습니다. 첫번째로 실험해본 좌표를 이용한 학습에서는 사람이 어디에 있는지에 따라서 학습량이 많아야하거나 아니면 전처리로 좌표들을 절대 좌표로 변환해주는 과정이 필요 합니다. 그리고 이미지를 이용하여 했을 때는 원본 이미지에서 사람의 부분을 크롭해서 사용하기엔 사람의 다양성에 영향을 너무 많이 받을거 같아서 좌표를 점과 선으로 이어서 사진으로 변경하고 점과 선만있는 이미지로 학습하였습니다. 각 클래스에서 3개의 데이터를 가지고와서 테스트해본 결과 정확도 100이라는 결과가 있었지만 전처리에서 20 ms가 걸려 너무 무겁다고 판단하였습니다.
  + 마지막으로 각도를 이용한 이유는 좌표와 다르게 위치가 변해도 각도는 동일하고, 사람들의 신체적 특성이 다르다해도 각도는 같기 떄문입니다. 정말 단순하지만 좋은 이유라고 생각합니다. 전처리에서도 좌표를 이용해서 각도계산 12번만하면 끝이나기 때문입니다. 그리고 전처리 속도도 이미지를 사용했을 때보다 빨랐습니다. 그래서 이 프로젝트에서 제가 각도를 사용하였습니다.
