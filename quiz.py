"""Quiz class representing an individual quiz question."""


class Quiz:
    """Represents a single quiz with options and correct answer."""

    def __init__(self, quiz_id: int, question: str, options: list, correct_answer: int):
        self.quiz_id = quiz_id
        self.question = question
        self.options = options
        self.correct_answer = correct_answer

    def display(self, number: int):
        print("-" * 40)
        print(f"[문제 {number}] {self.question}")
        for i, option in enumerate(self.options, start=1):
            print(f"  {i}. {option}")

    def check_answer(self, user_answer: int) -> bool:
        return self.correct_answer == user_answer

    def to_dict(self) -> dict:
        return {
            "id": self.quiz_id,
            "question": self.question,
            "options": self.options,
            "correct_answer": self.correct_answer,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            quiz_id=data.get("id", 1),
            question=data.get("question", ""),
            options=data.get("options", []),
            correct_answer=data.get("correct_answer", 1),
        )