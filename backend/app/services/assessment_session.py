from dataclasses import dataclass, field


@dataclass
class AssessmentSession:
    """
    Track the state of an adaptive assessment session.

    The session keeps assessment-specific state separate
    from the learner's long-term learner state.
    """

    user_id: int
    concept_id: int
    max_questions: int = 10
    questions_asked: int = 0
    correct_answers: int = 0
    question_ids: list[int] = field(default_factory=list)
    completed: bool = False

    @property
    def accuracy(self) -> float:
        """Return the current assessment accuracy."""

        if self.questions_asked == 0:
            return 0.0

        return self.correct_answers / self.questions_asked

    @property
    def progress(self) -> float:
        """Return assessment progress as a value between 0 and 1."""

        if self.max_questions <= 0:
            return 1.0

        return min(
            1.0,
            self.questions_asked / self.max_questions,
        )

    def record_question(
        self,
        question_id: int,
        is_correct: bool,
    ) -> None:
        """
        Record a completed question in the session.
        """

        if self.completed:
            raise ValueError(
                "assessment session is already completed"
            )

        if question_id in self.question_ids:
            raise ValueError(
                "question has already been recorded"
            )

        if self.questions_asked >= self.max_questions:
            self.completed = True
            raise ValueError(
                "assessment session has reached its question limit"
            )

        self.question_ids.append(question_id)
        self.questions_asked += 1

        if is_correct:
            self.correct_answers += 1

        if self.questions_asked >= self.max_questions:
            self.completed = True

    def remaining_questions(self) -> int:
        """Return the number of questions remaining."""

        return max(
            0,
            self.max_questions - self.questions_asked,
        )