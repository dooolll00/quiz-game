"""Quiz model and default quiz data."""


class Quiz:
    """Represents a single four-choice quiz question."""

    def __init__(self, quiz_id: int, question: str, options: list[str], correct_answer: int):
        self.quiz_id = quiz_id
        self.question = question
        self.options = options
        self.correct_answer = correct_answer

    @property
    def choices(self) -> list[str]:
        """Compatibility alias for code that uses the name choices."""
        return self.options

    @property
    def answer(self) -> int:
        """Compatibility alias for code that uses the name answer."""
        return self.correct_answer

    def display(self, number: int) -> None:
        """Print this quiz question and its choices."""
        print("-" * 40)
        print(f"[문제 {number}] {self.question}")
        for i, option in enumerate(self.options, start=1):
            print(f"  {i}. {option}")

    def check_answer(self, user_answer: int) -> bool:
        """Return True when the selected answer number is correct."""
        return self.correct_answer == user_answer

    def check(self, user_answer: int) -> bool:
        """Compatibility alias for check_answer."""
        return self.check_answer(user_answer)

    def to_dict(self) -> dict:
        """Convert this quiz to the JSON-serializable state schema."""
        return {
            "id": self.quiz_id,
            "question": self.question,
            "options": self.options,
            "correct_answer": self.correct_answer,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create a Quiz from current or legacy state data."""
        return cls(
            quiz_id=data.get("id", 1),
            question=data.get("question", ""),
            options=data.get("options", data.get("choices", [])),
            correct_answer=data.get("correct_answer", data.get("answer", 1)),
        )


def default_quizzes() -> list[Quiz]:
    """Return fresh default quizzes with a Python programming theme."""
    quiz_data = [
        {
            "id": 1,
            "question": "파이썬에서 리스트의 맨 끝에 값을 추가할 때 사용하는 메서드는 무엇일까요?",
            "options": ["append()", "push()", "add()", "insert_last()"],
            "correct_answer": 1,
        },
        {
            "id": 2,
            "question": "파이썬에서 주석 한 줄을 작성할 때 사용하는 기호는 무엇일까요?",
            "options": ["//", "<!-- -->", "#", "/* */"],
            "correct_answer": 3,
        },
        {
            "id": 3,
            "question": "딕셔너리에서 키와 값을 함께 반복할 때 주로 사용하는 메서드는 무엇일까요?",
            "options": ["keys()", "values()", "items()", "pairs()"],
            "correct_answer": 3,
        },
        {
            "id": 4,
            "question": "파이썬에서 예외 처리를 시작할 때 사용하는 키워드는 무엇일까요?",
            "options": ["catch", "try", "except", "error"],
            "correct_answer": 2,
        },
        {
            "id": 5,
            "question": "함수에서 값을 돌려줄 때 사용하는 키워드는 무엇일까요?",
            "options": ["return", "yield", "print", "break"],
            "correct_answer": 1,
        },
    ]
    return [Quiz.from_dict(item) for item in quiz_data]
