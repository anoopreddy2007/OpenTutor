from sqlalchemy.orm import Session

from app.models.concept import Concept
from app.models.topic import Topic


class ConceptRetriever:
    """Retrieves relevant concepts for tutor context."""

    def retrieve(
        self,
        db: Session,
        query: str,
        *,
        course_id: int | None = None,
        limit: int = 3,
    ) -> list[dict]:
        query_terms = {
            term.lower()
            for term in query.split()
            if len(term.strip()) >= 3
        }

        query_builder = (
            db.query(Concept, Topic)
            .join(Topic, Concept.topic_id == Topic.id)
        )

        if course_id is not None:
            query_builder = query_builder.filter(
                Topic.course_id == course_id
            )

        candidates = query_builder.all()

        scored_results = []

        for concept, topic in candidates:
            searchable_text = " ".join(
                filter(
                    None,
                    [
                        concept.name,
                        concept.description,
                        topic.name,
                        topic.description,
                    ],
                )
            ).lower()

            score = sum(
                1
                for term in query_terms
                if term in searchable_text
            )

            if score > 0:
                scored_results.append(
                    {
                        "concept_id": concept.id,
                        "concept_name": concept.name,
                        "concept_description": concept.description,
                        "topic_name": topic.name,
                        "score": score,
                    }
                )

        scored_results.sort(
            key=lambda result: result["score"],
            reverse=True,
        )

        return scored_results[:limit]