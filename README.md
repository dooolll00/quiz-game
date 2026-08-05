# 🎯 나만의 파이썬 퀴즈 게임

터미널에서 실행하는 4지선다형 파이썬 퀴즈 게임입니다.
사용자는 퀴즈를 풀고, 새 퀴즈를 추가하고, 퀴즈 목록과 최고 점수를 확인할 수 있습니다.

## 📌 프로젝트 주제

- **주제**: Python 기본 문법 퀴즈
- **내용**: 리스트 메서드, 주석, 딕셔너리, 예외 처리, 함수 반환 키워드 등
- **목표**: 파이썬 기초 개념을 퀴즈 게임으로 복습하기

## 📁 파일 구성

```
mission-2/
├── main.py        # 진입점: QuizGame 실행, Ctrl+C/EOF 안전 종료 처리
├── quiz.py        # Quiz 클래스(문제/선택지/정답) + 기본 퀴즈 데이터
├── quiz_game.py   # QuizGame 클래스(메뉴, 풀기/추가/목록/점수, 저장/불러오기)
├── state.json     # 데이터 파일 (퀴즈 목록 + 최고 점수, 실행 시 자동 생성)
├── README.md      # 프로젝트 문서
├── SPEC.md        # 시스템 사양서 (요구사항/아키텍처/클래스/화면/데이터 설계)
├── Python LEARNING.md    # 과제 목표(학습 내용) 정리
└── docs/screenshots/  # 제출용 스크린샷
```

## 미션 검토 및 학습 정리

## ▶️ 실행 방법
터미널에서 프로젝트 폴더로 이동한 뒤 아래 명령어를 실행합니다.
```bash
python3 main.py
```

## 기능 목록
또는 아래 명령어로도 실행할 수 있습니다.

```bash
python3 quiz_game.py
```

## 🎮 기능
1. **퀴즈 풀기**
   - 저장된 파이썬 퀴즈를 풀 수 있습니다.
   - 문제는 랜덤 순서로 출제됩니다.
   - 정답을 맞히면 점수가 올라갑니다.
  
2. **퀴즈 추가**
   - 사용자가 직접 문제와 선택지를 입력해 새 퀴즈를 추가할 수 있습니다.
   - 추가한 퀴즈는 `state.json`에 저장됩니다.

3. **퀴즈 목록**
   - 현재 저장된 퀴즈 목록을 확인할 수 있습니다.

4. **점수 확인**
   - 지금까지 기록한 최고 점수를 확인할 수 있습니다.

5. **종료**
   - 데이터를 저장하고 프로그램을 종료합니다. 

## 🧾 저장 데이터 예시

`state.json`에는 퀴즈 목록과 최고 점수가 저장됩니다.

```json
{  "quizzes": [
    {
      "id": 1,
      "question": "파이썬에서 리스트의 맨 끝에 값을 추가할 때 사용하는 메서드는 무엇일까요?",
      "options": [
        "append()",
        "push()",
        "add()",
        "insert_last()"
      ],
      "correct_answer": 1
    }
  ],
  "best_score": null
}
```

## ✅ 사용한 파이썬 개념

- 클래스
- 리스트
- 딕셔너리
- 반복문
- 조건문
- 함수
- 예외 처리
- JSON 파일 입출력
- 랜덤 출제

## 📌 Git 커밋 이력 그래프 확인 방법

터미널에서 아래 명령어를 실행하면 커밋 이력을 그래프 형태로 확인할 수 있습니다.

```bash
git log --oneline --graph --decorate --all
```
최근 커밋 몇 개만 보고 싶다면 아래처럼 개수를 제한할 수 있습니다.

```bash
git log --oneline --graph --decorate --all -10
```

예시 출력은 아래와 비슷합니다.

```text
* 4807f8a (HEAD -> work) Create clear README for quiz game
* 89af1bb Add mission files and state data
* e1bd4fa Use Python quiz defaults
* f442b1e Make quiz game directly runnable with new quizzes
```

## 📸 미션 수행 및 실행 스크린샷

### 1. Git 커밋 이력 그래프 (`git log`)
<img width="450" alt="git log graph screenshot" src="https://github.com/user-attachments/assets/6a6e50f5-dd4c-4bf1-9e59-c9a82536f6e4" />

### 2. 프로그램 실행 및 결과 화면
+<img width="350" alt="quiz game execution screenshot" src="https://github.com/user-attachments/assets/68801e0c-6125-47b4-8123-4412ec3c796c" />

