"""Console quiz game implemented in a single main.py file."""

import json
import os
import sys


class Quiz:
    """Represents one four-choice quiz question."""

    def __init__(self, question: str, choices: list[str], answer: int):
        self.question = question
        self.choices = choices
        self.answer = answer
        
    def display(self, number: int) -> None:
        """Print this quiz question and its choices."""
        print("-" * 40)
        print(f"[문제 {number}] {self.question}")
        for index, choice in enumerate(self.choices, start=1):
            print(f"  {index}. {choice}")

    def check_answer(self, user_answer: int) -> bool:
        """Return True when the selected answer number is correct."""
        return self.answer == user_answer

    def to_dict(self) -> dict:
        """Convert this quiz to the JSON-serializable state schema."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create a Quiz from current or legacy state data."""
        return cls(
            question=data.get("question", ""),
            choices=data.get("choices", data.get("options", [])),
            answer=data.get("answer", data.get("correct_answer", 1)),
        )


class QuizGame:
    """Manage menus, quiz play, score tracking, and state persistence."""

     STATE_FILE = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "state.json"
    )

    def __init__(self, state_file: str = STATE_FILE):
        self.state_file = state_file
        self.quizzes: list[Quiz] = []
        self.best_score: int | None = None
        self.load_state()

    def read_int(self, prompt: str, min_value: int, max_value: int) -> int | None:
        """Read a number, validating blank, non-number, range, Ctrl+C, and EOF cases."""
        while True:
            try:
                raw_value = input(prompt).strip()
            except (KeyboardInterrupt, EOFError):
                print("\n\n⚠️ 입력이 중단되었습니다. 현재 데이터를 저장하고 안전하게 종료합니다.")
                self.save_state()
                return None

            if raw_value == "":
                print(f"⚠️ 빈 입력입니다. {min_value}~{max_value} 사이의 숫자를 입력해 주세요.")
                continue

            try:
                number = int(raw_value)
            except ValueError:
                print(f"⚠️ 잘못된 입력입니다. {min_value}~{max_value} 사이의 숫자를 입력하세요.")
                continue

            if not (min_value <= number <= max_value):
                print(f"⚠️ 허용 범위를 벗어났습니다. {min_value}~{max_value} 사이의 숫자를 입력해 주세요.")
                continue

            return number

    def read_text(self, prompt: str) -> str | None:
        """Read non-empty text, returning None when the input stream is interrupted."""
        while True:
            try:
                text = input(prompt).strip()
            except (KeyboardInterrupt, EOFError):
                print("\n\n⚠️ 입력이 중단되었습니다. 현재 데이터를 저장하고 안전하게 종료합니다.")
                self.save_state()
                return None

            if not text:
                print("⚠️ 빈 입력은 허용되지 않습니다.")
                continue

            return text

    def get_default_quizzes(self) -> list[Quiz]:
        """Return at least five default quizzes about CS, Python, Git, and JSON."""
        return [
            Quiz(
                "파이썬(Python)의 창시자는 누구일까요?",
                ["Guido van Rossum", "Linus Torvalds", "James Gosling", "Bjarne Stroustrup"],
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
                "JSON 데이터를 파이썬 dict로 읽을 때 주로 사용하는 표준 라이브러리는?",
                ["csv", "json", "pickle", "sqlite3"],
                2,
            ),
            Quiz(
                "파이썬 클래스 인스턴스 자신을 가리키는 첫 번째 매개변수 이름은?",
                ["this", "self", "cls", "super"],
                2,
            ),
        ]

    def load_state(self) -> None:
        """Load quizzes and score from UTF-8 JSON, falling back to defaults when needed."""
        if not os.path.exists(self.state_file):
            print("📂 저장 파일이 없어 기본 퀴즈 데이터를 생성합니다.")
            self.quizzes = self.get_default_quizzes()
            self.save_state()
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.quizzes = [Quiz.from_dict(item) for item in data.get("quizzes", [])]
            self.best_score = data.get("best_score")

            if not self.quizzes:
                print("⚠️ 저장된 퀴즈가 없어 기본 퀴즈 데이터로 복구합니다.")
                self.quizzes = self.get_default_quizzes()
                self.save_state()
            else:
                print(
                    f"📂 저장된 데이터를 불러왔습니다. "
                    f"(퀴즈 {len(self.quizzes)}개, "
                    f"최고점수 {self.best_score if self.best_score is not None else '없음'})"
                )
        except (json.JSONDecodeError, OSError, TypeError) as error:
            print(f"⚠️ 저장 파일을 읽을 수 없어 기본 데이터로 복구합니다: {error}")
            self.quizzes = self.get_default_quizzes()
            self.best_score = None
            self.save_state()

    def save_state(self) -> None:
        """Save quizzes and best score to project-root state.json using UTF-8."""
        try:
            data = {
                "quizzes": [quiz.to_dict() for quiz in self.quizzes],
                "best_score": self.best_score,
            }
            with open(self.state_file, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError as error:
            print(f"⚠️ 저장 중 오류가 발생했습니다: {error}")

    def play_quiz(self) -> None:
        """Ask every saved quiz and update the best score when the result improves."""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        correct_count = 0

        for index, quiz in enumerate(self.quizzes, start=1):
            quiz.display(index)
            user_answer = self.read_int("\n정답 입력 (1-4): ", 1, 4)
            if user_answer is None:
                return

            if quiz.check_answer(user_answer):
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                print(f"❌ 틀렸습니다. (정답: {quiz.answer}번)")

        total_count = len(self.quizzes)
        score = round((correct_count / total_count) * 100)
        print("\n========================================")
        print(f"🏆 결과: {total_count}문제 중 {correct_count}문제 정답! ({score}점)")

        if self.best_score is None or score > self.best_score:
            print("🎉 새로운 최고 점수입니다!")
            self.best_score = score
            self.save_state()
        print("========================================")

    def add_quiz(self) -> None:
        """Collect a new quiz from user input and persist it immediately."""
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = self.read_text("문제를 입력하세요: ")
        if question is None:
            return

        choices = []
        for index in range(1, 5):
            choice = self.read_text(f"선택지 {index}: ")
            if choice is None:
                return
            choices.append(choice)

        answer = self.read_int("정답 번호 (1-4): ", 1, 4)
        if answer is None:
            return

        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()
        print("\n✅ 퀴즈가 추가되었습니다!")

    def show_quiz_list(self) -> None:
        """Print saved quiz questions without revealing answers."""
        if not self.quizzes:
            print("\n📋 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"[{index}] {quiz.question}")
        print("-" * 40)

    def show_score(self) -> None:
        """Print the best score or a first-play 안내 message."""
        print("\n========================================")
        if self.best_score is None:
            print("🏆 아직 퀴즈를 풀지 않았습니다.")
        else:
            print(f"🏆 최고 점수: {self.best_score}점")
        print("========================================")

    def run(self) -> None:
        """Display the menu loop until the user chooses to exit or input ends."""
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

            choice = self.read_int("선택 (1-5): ", 1, 5)
            if choice is None:
                break

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



def main() -> None:
    """Create and run the quiz game."""
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()
