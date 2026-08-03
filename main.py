import json
import os
import sys


# ==========================================
# 1. 공통 입력 및 예외 처리 함수
# ==========================================
def read_int(prompt: str, min_val: int, max_val: int) -> int:
    """공백 제거, 숫자 변환, 범위 검사를 모두 처리하는 공통 입력 함수"""
    while True:
        try:
            raw = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print(
                "\n\n⚠️ 사용자에 의해 프로그램이 중단되었습니다. 안전하게 종료합니다."
            )
            sys.exit(0)

        if raw == "":
            print(
                f"⚠️ 빈 입력입니다. {min_val}~{max_val} 사이의 숫자를 입력해 주세요."
            )
            continue
        try:
            num = int(raw)
        except ValueError:
            print(f"⚠️ 올바른 숫자를 입력해 주세요. ({min_val}~{max_val})")
            continue
        if not (min_val <= num <= max_val):
            print(
                f"⚠️ 허용 범위를 벗어났습니다. {min_val}~{max_val} 사이의 숫자를 입력해 주세요."
            )
            continue
        return num


# ==========================================
# 2. Quiz 클래스 정의
# ==========================================
class Quiz:

    def __init__(self, question: str, choices: list, answer: int):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, number: int):
        print("-" * 40)
        print(f"[문제 {number}] {self.question}")
        for i, choice in enumerate(self.choices, start=1):
            print(f"  {i}. {choice}")

    def check_answer(self, user_answer: int) -> bool:
        return self.answer == user_answer

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data.get("question", ""),
            data.get("choices", data.get("options", [])),
            data.get("answer", data.get("correct_answer", 1)),
        )


# ==========================================
# 3. 기본 퀴즈 데이터 정의
# ==========================================
def get_default_quizzes() -> list:
    return [
        Quiz(
            "파이썬(Python)의 창시자는 누구일까요?",
            [
                "Guido van Rossum",
                "Linus Torvalds",
                "James Gosling",
                "Bjarne Stroustrup",
            ],
            1,
        ),
        Quiz(
            "파이썬에서 변경 불가능(Immutable)한 순서형 데이터 타입은?",
            ["List", "Dictionary", "Tuple", "Set"],
            3,
        ),
        Quiz(
            "Git에서 현재 작업 영역을 저장소에 기록하는 명령어는?",
            ["git add", "git commit", "git push", "git checkout"],
            2,
        ),
        Quiz(
            "JSON 표준 인코딩 방식은 무엇일까요?",
            ["EUC-KR", "ASCII", "UTF-8", "UTF-16"],
            3,
        ),
        Quiz(
            "파이썬 클래스 인스턴스 자신을 가리키는 첫 번째 매개변수 이름은?",
            ["this", "self", "cls", "super"],
            2,
        ),
    ]


# ==========================================
# 4. QuizGame 클래스 정의
# ==========================================
class QuizGame:
    STATE_FILE = "state.json"

    def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.load_state()

    def load_state(self):
        if not os.path.exists(self.STATE_FILE):
            self.quizzes = get_default_quizzes()
            self.save_state()
            return

        try:
            with open(self.STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
            self.best_score = data.get("best_score")

            if not self.quizzes:
                self.quizzes = get_default_quizzes()
        except Exception:
            self.quizzes = get_default_quizzes()
            self.best_score = None
            self.save_state()

    def save_state(self):
        try:
            data = {
                "quizzes": [q.to_dict() for q in self.quizzes],
                "best_score": self.best_score,
            }
            with open(self.STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except OSError:
            pass

    def play_quiz(self):
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        correct = 0

        for i, quiz in enumerate(self.quizzes, start=1):
            quiz.display(i)
            user_ans = read_int("\n정답 입력 (1-4): ", 1, 4)

            if quiz.check_answer(user_ans):
                print("✅ 정답입니다!")
                correct += 1
            else:
                print(f"❌ 틀렸습니다. (정답: {quiz.answer}번)")

        total = len(self.quizzes)
        score = round((correct / total) * 100) if total > 0 else 0

        print("\n========================================")
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")

        if self.best_score is None or score > self.best_score:
            print("🎉 축하합니다! 새로운 최고 점수입니다!")
            self.best_score = score
            self.save_state()
        print("========================================")

    def _read_text(self, prompt: str) -> str:
        while True:
            try:
                text = input(prompt).strip()
            except (KeyboardInterrupt, EOFError):
                sys.exit(0)
            if not text:
                print("⚠️ 빈 입력은 허용되지 않습니다.")
                continue
            return text

    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = self._read_text("문제를 입력하세요: ")
        choices = [self._read_text(f"선택지 {i}: ") for i in range(1, 5)]
        answer = read_int("정답 번호 (1-4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()
        print("\n✅ 새로운 퀴즈가 성공적으로 추가되었습니다!")

    def show_quiz_list(self):
        if not self.quizzes:
            print("\n📋 등록된 퀴즈가 없습니다.")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"[{i}] {quiz.question}")
        print("-" * 40)

    def show_score(self):
        print("\n========================================")
        if self.best_score is None:
            print("🏆 아직 퀴즈를 풀지 않았습니다.")
        else:
            print(f"🏆 현재 최고 점수: {self.best_score}점")
        print("========================================")

    def run(self):
        while True:
            print("\n========================================")
            print("        🎯 나만의 퀴즈 게임 🎯")
            print("========================================")
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록")
            print("4. 점수 확인")
            print("5. 종료")
            print("========================================")

            choice = read_int("선택 (1-5): ", 1, 5)

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quiz_list()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                print("\n👋 게임을 종료합니다.")
                self.save_state()
                break


def main():
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()