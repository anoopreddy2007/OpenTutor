from app.ai.tutor import TutorService
from app.ai.providers import LLMProvider


class MockLLMProvider(LLMProvider):
    def generate(self, prompt: str, *, system_prompt: str | None = None) -> str:
        return f"Mock tutor response: {prompt}"


def test_tutor_service_generates_response():
    service = TutorService(provider=MockLLMProvider())

    class MockDB:
        def query(self, model):
            return self

        def filter(self, *args):
            return self

        def first(self):
            return None

    response = service.generate_response(
        db=MockDB(),
        user_id=1,
        concept_id=1,
        question="What is recursion?",
    )

    assert "Mock tutor response" in response
    assert "What is recursion?" in response
    assert "Learner mastery: 0.00" in response
    assert "Learner confidence: 0.00" in response