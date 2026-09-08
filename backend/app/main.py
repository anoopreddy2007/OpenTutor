from fastapi import FastAPI

from app.api.users import router as users_router
from app.api.courses import router as courses_router
from app.api.topics import router as topics_router
from app.api.concepts import router as concepts_router
from app.api.questions import router as questions_router
from app.api.attempts import router as attempts_router
from app.api.learner_states import router as learner_states_router
from app.api.recommendations import router as recommendations_router
app = FastAPI(
    title="OpenTutor API",
    description="Backend API for the OpenTutor personalized learning system.",
    version="0.1.0",
)

app.include_router(users_router)
app.include_router(courses_router)
app.include_router(topics_router)
app.include_router(concepts_router)
app.include_router(questions_router)
app.include_router(attempts_router)
app.include_router(learner_states_router)
app.include_router(recommendations_router)
@app.get("/")
def root():
    return {
        "name": "OpenTutor",
        "message": "OpenTutor API is running!",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}