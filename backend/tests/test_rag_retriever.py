import uuid

from app.database.connection import SessionLocal
from app.models.concept import Concept
from app.models.course import Course
from app.models.topic import Topic
from app.rag.retriever import ConceptRetriever


def test_retriever_returns_relevant_concept():
    db = SessionLocal()
    test_id = uuid.uuid4().hex[:8]

    try:
        course = Course(
            name=f"RAG Test Course {test_id}",
            description="Course for testing retrieval",
        )
        db.add(course)
        db.flush()

        topic = Topic(
            course_id=course.id,
            name=f"Python Fundamentals {test_id}",
            description="Fundamental Python programming concepts",
            order_index=1,
        )
        db.add(topic)
        db.flush()

        concept = Concept(
            topic_id=topic.id,
            name=f"Python Variables {test_id}",
            description="Variables store values in Python programs",
            difficulty=1,
        )
        db.add(concept)
        db.commit()

        retriever = ConceptRetriever()

        results = retriever.retrieve(
            db=db,
            query="How do Python variables work?",
            course_id=course.id,
        )

        assert len(results) > 0
        assert results[0]["concept_id"] == concept.id
        assert results[0]["concept_name"] == concept.name
        assert results[0]["topic_name"] == topic.name
        assert results[0]["score"] > 0

    finally:
        db.close()


def test_retriever_respects_result_limit():
    db = SessionLocal()
    test_id = uuid.uuid4().hex[:8]

    try:
        course = Course(
            name=f"RAG Limit Test Course {test_id}",
            description="Course for testing retrieval limits",
        )
        db.add(course)
        db.flush()

        topic = Topic(
            course_id=course.id,
            name=f"Programming Concepts {test_id}",
            description="Programming concepts",
            order_index=1,
        )
        db.add(topic)
        db.flush()

        for index in range(5):
            concept = Concept(
                topic_id=topic.id,
                name=f"Python Programming Concept {index} {test_id}",
                description="Python programming concept",
                difficulty=1,
            )
            db.add(concept)

        db.commit()

        retriever = ConceptRetriever()

        results = retriever.retrieve(
            db=db,
            query="Python programming concept",
            course_id=course.id,
            limit=3,
        )

        assert len(results) == 3

    finally:
        db.close()