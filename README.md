# 🚗 Car Damage Analysis  
AI 기반 차량 파손 이미지 인식 및 사고 수리 견적 산출 프로그램  
딥러닝 모델을 활용해 차량 이미지를 분석하고, 파손 부위를 자동으로 감지하여 예상 수리 견적을 산출하는 Flask 웹 애플리케이션입니다.

---

## 📘 프로젝트 개요  

**Car Damage Analysis**는 차량 사고 이미지 한 장으로 손상 부위를 자동 인식하고 예상 수리 견적을 제시하는 AI 기반 웹 서비스입니다.  

EfficientNetB0 모델을 활용하여 다양한 조명, 각도, 배경 조건에서도 일관된 예측 성능을 보이도록 설계했으며,  
데이터 전처리 → 모델 학습 → 추론 → Flask 웹 연동까지 하나의 엔드투엔드(End-to-End) 파이프라인으로 구현했습니다.  

이 프로젝트는 단순한 이미지 분류를 넘어서 정비소 견적 데이터와 연동 가능한 **실제 사고 견적 시스템**을 목표로 합니다.  

---

## ⚙️ 기술 스택  

- **언어:** Python  
- **프레임워크:** Flask  
- **딥러닝:** TensorFlow, Keras (EfficientNetB0)  
- **데이터 처리:** Pandas, NumPy  
- **시각화:** Matplotlib  
- **프론트엔드:** HTML5, CSS3, JavaScript  
- **개발 환경:** Virtualenv, Git, VSCode  

---

## 💡 주요 기능  

1. **AI 손상 부위 인식**  
   - CNN 모델이 차량 이미지를 분석하여 파손 부위를 자동 감지  

2. **수리 견적 산출**  
   - 손상 부위별 평균 단가를 기반으로 견적을 계산  

3. **웹 기반 인터페이스**  
   - 사용자가 직접 이미지를 업로드하고 결과를 실시간 확인 가능  

4. **시각적 결과 표시**  
   - 파손 부위 예측 결과를 이미지와 함께 직관적으로 제공  

5. **모듈화 구조**  
   - Flask MVC 구조 기반으로 유지보수성과 확장성을 강화  

---

## 🗂️ 프로젝트 구조  

```plaintext
car_damage_analysis/
│
├── app.py                  # Flask 메인 서버
│
├── model/
│   ├── detect_damage.py    # 모델 로드 및 예측 함수
│   └── trained_model.h5    # 학습된 EfficientNetB0 모델
│
├── static/
│   ├── css/                # 스타일시트
│   └── uploads/            # 업로드된 이미지 저장 폴더
│
├── templates/
│   ├── index.html          # 메인 업로드 페이지
│   ├── result.html         # 예측 결과 페이지
│
├── utils/
│   └── preprocess.py       # 이미지 전처리 및 스케일링 함수
│
├── requirements.txt
└── README.md
```
---
## 🚀 실행 방법

### 1️⃣ 저장소 클론

```git clone https://github.com/Prestige7777/car-damage-analysis.git
cd car-damage-analysis
```

### 2️⃣ 가상환경 생성 및 활성화
```python -m venv venv
venv\Scripts\activate   # (Windows)
source venv/bin/activate   # (macOS/Linux)
```

### 3️⃣ 패키지 설치
```
pip install -r requirements.txt
```

### 4️⃣ Flask 서버 실행
```
python app.py
```

#### ✅ 실행 후 브라우저에서 아래 주소로 접속

```
http://127.0.0.1:5000
```
---

## 🧠 모델 개요

- 모델 구조: EfficientNetB0 (ImageNet 사전학습 기반)

- 입력 크기: 224 × 224 RGB

- 출력 클래스: 차량 손상 부위 및 손상 종류

- 성능 지표: AUC 약 0.90

- 학습 데이터: 실제 사고 차량 이미지 + 증강(Augmentation)

EfficientNetB0 모델은 경량 구조와 높은 정확도를 동시에 달성하여, 차량 파손 이미지와 같은 복잡한 입력에서도 안정적인 분류 성능을 제공합니다.

---
## 📈 향후 개선 계획

- YOLOv8 기반 손상 영역 감지 기능 추가

- 정비소 견적 데이터베이스 연동

- 반응형 UI 및 모바일 환경 지원

- 클라우드 서버 (Render / AWS EC2) 배포

---
## 👨‍💻 개발자 정보

- 이름: 프레스티지 (Prestige)
- 역할: Full-stack / AI Developer
- 담당: 모델 학습, Flask 연동, 웹 구축

GitHub: https://github.com/Prestige7777

키워드: AI / Computer Vision / Automotive / Flask / Deep Learning

---
## 🏁 라이선스

이 프로젝트는 MIT License를 따릅니다.
연구 및 학습 목적이라면 자유롭게 수정 및 재사용이 가능합니다.



## 🚀 “한 장의 이미지로 사고를 진단하는 시대, Car Damage Analysis가 시작합니다.”
