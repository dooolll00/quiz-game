"""QuizGame class for managing quiz state and game logic."""

import json
import os
from quiz import Quiz


class QuizGame:
    """Manages quiz game state, including quizzes and best score."""

    def __init__(self, state_file="state.json"):
        self.state_file = state_file
        self.quizzes = []
        self.best_score = 0
        self.load_state()

    def load_state(self):
        if not os.path.exists(self.state_file):
            self._create_default_quizzes()
        else:
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.best_score = data.get("best_score", 0)
                    self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading state: {e}")
                self._create_default_quizzes()

    def save_state(self):
        try:
            data = {
                "best_score": self.best_score,
                "quizzes": [q.to_dict() for q in self.quizzes],
            }
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving state: {e}")

    def _create_default_quizzes(self):
        default_quizzes = [
            {
                "id": 1,
                "question": "파이썬(Python)의 창시자는 누구일까요?",
                "options": ["Guido van Rossum", "Linus Torvalds", "James Gosling", "Bjarne Stroustrup"],
                "correct_answer": 1,
            },
            {
                "id": 2,
                "question": "파이썬에서 변경 불가능(Immutable)한 순서형 데이터 타입은?",
                "options": ["List", "Dictionary", "Tuple", "Set"],
                "correct_answer": 3,
            },
            {
                "id": 3,
                "question": "Git에서 현재 작업 영역을 저장소에 기록하는 명령어는?",
                "options": ["git add", "git commit", "git push", "git checkout"],
                "correct_answer": 2,
            },
            {
                "id": 4,
                "question": "JSON 표준 인코딩 방식은 무엇일까요?",
                "options": ["EUC-KR", "ASCII", "UTF-8", "UTF-16"],
                "correct_answer": 3,
            },
            {
                "id": 5,
                "question": "파이썬 클래스 인스턴스 자신을 가리키는 첫 번째 매개변수 이름은?",
                "options": ["this", "self", "cls", "super"],
                "correct_answer": 2,
            },
        ]
        self.quizzes = [Quiz.from_dict(q) for q in default_quizzes]
        self.best_score = 0
        self.save_state()

    def add_quiz(self, question, options, correct_answer):
        quiz_id = max([q.quiz_id for q in self.quizzes], default=0) + 1
        quiz = Quiz(quiz_id, question, options, correct_answer)
        self.quizzes.append(quiz)
        self.save_state()
        return quiz_id

    def get_quizzes(self):
        return self.quizzes

    def update_best_score(self, score):
        if score > self.best_score:
            self.best_score = score
            self.save_state()

    def get_best_score(self):
        return self.best_score
