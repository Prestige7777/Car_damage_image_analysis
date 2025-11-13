# 🚗 차량 손상 AI 분석 시스템

AI 기반 차량 손상 부위 자동 감지 및 분석 웹 애플리케이션

![Python](https://img.shields.io/badge/Python-3.10-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.18.0-orange)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green)

## 📋 프로젝트 소개

차량 사진 한 장으로 손상 부위를 자동으로 감지하고 분석하는 AI 시스템입니다.
EfficientNetB0 기반의 딥러닝 모델을 사용하여 32가지 손상 유형을 인식합니다.

### 주요 기능

- 🎯 **정확한 손상 감지**: 32가지 차량 손상 유형 자동 인식
- ⚡ **빠른 분석**: 몇 초 만에 분석 완료
- 📸 **간편한 사용**: 드래그 앤 드롭으로 이미지 업로드
- 📊 **시각화**: 손상 부위별 신뢰도를 프로그레스 바로 표시
- 📱 **반응형 디자인**: 모바일/태블릿/데스크톱 모두 지원

## 🛠️ 기술 스택

### Backend
- **Python 3.10**
- **Flask 3.1.2** - 웹 프레임워크
- **TensorFlow 2.18.0** - 딥러닝 프레임워크
- **Keras 3** - 모델 구축 및 학습
- **EfficientNetB0** - 베이스 모델

### Frontend
- **HTML5 / CSS3**
- **JavaScript (Vanilla)**
- **Google Fonts (Noto Sans KR)**

### AI Model
- **Architecture**: EfficientNetB0 + Custom Classifier
- **Input Size**: 224x224x3
- **Output**: 32 classes (Multi-label classification)
- **Threshold**: 20% confidence

## 📦 설치 방법

### 1. 저장소 클론

```bash
git clone https://github.com/your-username/car-damage-analysis.git
cd car-damage-analysis
```

### 2. 가상환경 생성 및 활성화

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

## 🚀 실행 방법

### 개발 서버 실행

```bash
flask run --host=0.0.0.0 --port=5000
```

또는

```bash
python app.py
```

브라우저에서 `http://localhost:5000` 접속

## 📁 프로젝트 구조

```
car-damage-analysis/
├── app.py                          # Flask 메인 애플리케이션
├── requirements.txt                # Python 의존성 패키지
├── README.md                       # 프로젝트 문서
├── .gitignore                      # Git 무시 파일 목록
│
├── model/                          # AI 모델 관련 파일
│   ├── detect_damage.py           # 모델 로드 및 예측 로직
│   ├── damage_model_REBUILT.keras # 학습된 모델 파일
│   └── class_names (1).json       # 클래스 이름 정의
│
├── static/                         # 정적 파일
│   ├── style.css                  # 스타일시트
│   ├── uploads/                   # 업로드된 이미지 저장
│   └── results/                   # 분석 결과 이미지 저장
│
└── templates/                      # HTML 템플릿
    ├── index.html                 # 메인 페이지
    └── result.html                # 결과 페이지
```

## 🎨 주요 화면

### 메인 페이지
- 드래그 앤 드롭 이미지 업로드
- 이미지 미리보기
- 주요 기능 소개

### 결과 페이지
- 분석된 이미지 표시
- 감지된 손상 부위 목록
- 신뢰도 프로그레스 바
- 분석 결과 활용 팁

## 🔧 환경 변수

필요한 경우 `.env` 파일을 생성하여 설정:

```env
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
```

## 📊 모델 정보

### 입력
- **이미지 크기**: 224x224 픽셀
- **채널**: RGB (3채널)
- **전처리**: EfficientNet 표준 전처리

### 출력
- **클래스 수**: 32개
- **출력 형식**: Multi-label (여러 손상 동시 감지 가능)
- **활성화 함수**: Sigmoid
- **임계값**: 0.2 (20%)

### 성능
- **베이스 모델**: EfficientNetB0 (사전 학습)
- **추가 레이어**: Dense(128) + Dropout(0.5) + Dense(32)

## 🤝 기여 방법

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 👥 개발자

- **Your Name** - [GitHub](https://github.com/your-username)

## 🙏 감사의 말

- TensorFlow 및 Keras 팀
- EfficientNet 논문 저자들
- Flask 커뮤니티

## 📞 문의

프로젝트에 대한 질문이나 제안사항이 있으시면 이슈를 등록해주세요.

---

⭐ 이 프로젝트가 도움이 되셨다면 Star를 눌러주세요!
