# 🎯 나만의 CS & Python 퀴즈 게임

터미널 환경에서 실행되는 4지선다형 파이썬 퀴즈 콘솔 프로그램입니다.  
`state.json` 파일을 활용하여 퀴즈 목록과 최고 점수를 안전하게 보존합니다.

---

## 💡 퀴즈 주제 및 선정 이유
- **주제**: 컴퓨터 과학(CS) 기초 상식 및 Python 언어 기본 문법
- **선정 이유**: 이번 과제를 수행하면서 배운 기본 개념(자료형, 클래스, Git 명령어, JSON 처리 등)을 직접 정리하고 검증해 보기 위해 선택했습니다.

---

프로젝트 파일 구조
quiz-game/
├── main.py        # 퀴즈 게임 전체 로직 및 실행 코드
├── state.json     # 퀴즈 문제 데이터 및 최고 점수 저장 파일 (자동 생성)
├── .gitignore     # Git 추적 제외 파일 설정
└── README.md      # 프로젝트 사양서 및 설명서

---

## 🚀 실행 방법

### 개발 환경
- **Python**: Version 3.10 이상
- **외부 라이브러리**: 표준 라이브러리만 사용 (`json`, `os`, `sys`)

### 실행 명령어
```bash
# 1. 저장소 복제 (Clone)
git clone [https://github.com/dooolll00/quiz-game.git](https://github.com/dooolll00/quiz-game.git)

# 2. 프로젝트 디렉터리 이동
cd quiz-game

# 3. 프로그램 실행
python3 main.py

## 📸 미션 수행 및 실행 스크린샷

### 1. Git 커밋 이력 그래프 (`git log`)
![Git Log Graph](https://github.com/user-attachments/assets/79507655-593f-4b2a-890f-c2a90b3e50c5)

### 2. 프로그램 실행 및 결과 화면
![Game Play](https://github.com/user-attachments/assets/adebe353-f79c-4898-a29b-5c6ba4a743d6)